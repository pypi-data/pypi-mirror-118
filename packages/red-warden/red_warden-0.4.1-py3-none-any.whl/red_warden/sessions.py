from enum import Enum
import json
from functools import wraps
import datetime
from red_warden.helpers import import_string
import random
from cryptography.fernet import Fernet, InvalidToken
from red_warden.config import RWConfig
from red_warden.helpers import RWCustomJsonEncoder
from red_warden.datalayer import RWDataLayer, RWRedisBackend, RWMysqlBackend


RWConfig.env_string("RW_SESSIONS_TYPE", "cookie")
RWConfig.env_string("RW_SESSIONS_BACKEND_NAME")
RWConfig.env_string("RW_SESSIONS_NAME", "rws")
RWConfig.env_string("RW_SESSIONS_DOMAIN")
RWConfig.env_string("RW_SESSIONS_SAME_SITE", "lax")
RWConfig.env_bool("RW_SESSIONS_HTTPS_ONLY", True)
RWConfig.env_secret("RW_SESSIONS_SECRET")
RWConfig.env_int(
    "RW_SESSIONS_TIMEOUT", 14 * 24 * 60 * 60
)  # two weeks default expiration

if not RWConfig["RW_SESSIONS_SECRET"]:
    raise Exception(
        """
Missing SESSION secret key (env: RW_SESSIONS_SECRET). Try with one of these:
%s
%s
%s
"""
        % (
            str(Fernet.generate_key()),
            str(Fernet.generate_key()),
            str(Fernet.generate_key()),
        )
    )


class RWSessionTypeEnum(str, Enum):
    REDIS = "redis"
    MYSQL = "mysql"
    COOKIE = "cookie"


class RWMysqlSessionBackend:
    def __init__(self):
        if not RWConfig["RW_SESSIONS_BACKEND_NAME"]:
            raise KeyError("Mysql session backend not configured")

        backend = RWDataLayer._backends.get(RWConfig["RW_SESSIONS_BACKEND_NAME"], None)
        if not backend:
            raise KeyError(
                "Mysql session backend %s doesn't exists"
                % RWConfig["RW_SESSIONS_BACKEND_NAME"]
            )

        self.model = import_string("red_warden.datazones.RWManager.RWSessionModel")
        self.mysql = RWMysqlBackend(backend["endpoints"], backend["params"])

    async def connect(self):
        await self.mysql.connect()

    async def disconnect(self):
        await self.mysql.disconnect()

    async def get(self, key):

        row = await self.mysql.fetch_one(
            self.model.select().where(self.model.c.key == key)
        )
        if not row:
            return None
        else:
            row = await self.model.after_load(self.mysql, row)
            return row["value"]

    async def set(self, key, value, expires_at):
        # 30% chance to rotate key key, to avoid session fixation
        rotate_key = True if random.choice([0, 10]) < 3 else False
        if rotate_key:
            # let's create another key, delete the old one if exists
            if key:
                await self.delete(key)

            key = None

        if not key:
            key = Fernet.generate_key().decode()

        data = {
            "key": key,
            "value": value,
            "expires_at": datetime.datetime.now() + datetime.timedelta(0, expires_at),
        }

        should_create = True
        if key:
            updated_row = await self.mysql.execute(
                self.model.update()
                .where(self.model.c.key == key)
                .values(await self.model.before_update(self.mysql, data))
            )
            if updated_row > 0:
                should_create = False

        if should_create:
            data = await self.model.before_create(self.mysql, data)
            await self.mysql.execute(self.model.insert().values(data))

        return key

    async def delete(self, key):
        await self.mysql.execute(self.model.delete().where(self.model.c.key == key))


class RWRedisSessionBackend:
    def __init__(self):
        if not RWConfig["RW_SESSIONS_BACKEND_NAME"]:
            raise KeyError("Redis session backend not configured")

        backend = RWDataLayer._backends.get(RWConfig["RW_SESSIONS_BACKEND_NAME"], None)
        if not backend:
            raise KeyError(
                "Redis session backend %s doesn't exists"
                % RWConfig["RW_SESSIONS_BACKEND_NAME"]
            )

        self.redis = RWRedisBackend(backend["endpoints"], backend["params"])
        self.fernet = Fernet(str(RWConfig["RW_SESSIONS_SECRET"]))

    async def connect(self):
        await self.redis.connect()

    async def disconnect(self):
        await self.redis.disconnect()

    async def get(self, key):
        encrypted = await self.redis.get(key)
        if not encrypted:
            return None
        return json.loads(self.fernet.decrypt(encrypted.encode("utf-8")))

    async def set(self, key, value, expires_at):
        rotate_key = True if random.choice([0, 10]) < 3 else False
        if rotate_key:
            # let's create another key, delete the old one if exists
            if key:
                await self.delete(key)
            key = None

        if not key:
            key = "sessions:%s" % Fernet.generate_key().decode()

        s = json.dumps(value, cls=RWCustomJsonEncoder)
        await self.redis.set(key, self.fernet.encrypt(s.encode()), expire=expires_at)
        return key

    async def delete(self, key):
        await self.redis.delete(key)


async def _wrap_with_session(func, request):
    if RWConfig["RW_SESSIONS_TYPE"] == RWSessionTypeEnum.REDIS:
        backend = RWRedisSessionBackend()
    elif RWConfig["RW_SESSIONS_TYPE"] == RWSessionTypeEnum.MYSQL:
        backend = RWMysqlSessionBackend()
    else:
        backend = None

    if backend:
        await backend.connect()

    max_age = RWConfig["RW_SESSIONS_TIMEOUT"]
    fernet = Fernet(str(RWConfig["RW_SESSIONS_SECRET"]))
    initial_session_was_empty = True
    cookie = request.cookies.get(RWConfig["RW_SESSIONS_NAME"])
    if cookie:
        try:
            data = fernet.decrypt(cookie.encode("utf-8"), max_age).decode("utf-8")

            if RWConfig["RW_SESSIONS_TYPE"] == RWSessionTypeEnum.COOKIE:
                request.state.session = json.loads(data)
                initial_session_was_empty = False
            else:
                session_key = json.loads(data).get("sid")
                request.state.session = await backend.get(session_key.encode("utf-8"))
                if not request.state.session:
                    request.state.session = {}
                    initial_session_was_empty = True

                request.state.session_key = session_key

            initial_session_was_empty = False
        except InvalidToken:
            request.state.session = {}
    else:
        request.state.session = {}

    response = await func(request)

    session_key = getattr(request.state, "session_key", None)
    if request.state.session:
        if RWConfig["RW_SESSIONS_TYPE"] == RWSessionTypeEnum.COOKIE:
            cookie_data = request.state.session
        else:
            session_key = await backend.set(session_key, request.state.session, max_age)
            cookie_data = {"sid": session_key}

        data = fernet.encrypt(json.dumps(cookie_data).encode("utf-8")).decode("utf-8")

        response.set_cookie(
            key=RWConfig["RW_SESSIONS_NAME"],
            value=data,
            secure=RWConfig["RW_SESSIONS_HTTPS_ONLY"],
            max_age=max_age,
            samesite=RWConfig["RW_SESSIONS_SAME_SITE"],
            httponly=True,
            domain=RWConfig["RW_SESSIONS_DOMAIN"],
        )

    elif not initial_session_was_empty:
        if backend:
            await backend.delete(session_key)

        response.set_cookie(
            key=RWConfig["RW_SESSIONS_NAME"],
            value="",
            secure=RWConfig["RW_SESSIONS_HTTPS_ONLY"],
            expires=0,
            samesite=RWConfig["RW_SESSIONS_SAME_SITE"],
            httponly=True,
            domain=RWConfig["RW_SESSIONS_DOMAIN"],
        )

    if backend:
        await backend.disconnect()

    return response


def session_from_cookie(_func=None):
    def decorator_use_session(func):
        @wraps(func)
        async def wrapper_use_session(request):
            return await _wrap_with_session(func, request)

        return wrapper_use_session

    if _func is None:
        return decorator_use_session
    else:
        return decorator_use_session(_func)
