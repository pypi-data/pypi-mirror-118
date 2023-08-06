from abc import ABC
import os
import base64
import aioredis
import inspect
import importlib.util
import databases
import random
import json
import copy
from cryptography.fernet import Fernet
import sqlalchemy
from red_warden.config import RWConfig
from red_warden.helpers import get_random_element
from red_warden.enums import (
    RWMultiTenancyEnum,
    RWBackendTypeEnum,
    RWBackendDestinationEnum,
)
from red_warden.helpers import import_string


class RWDataLayerException(Exception):
    pass


RWConfig.env_secret("RW_DATABASE_SECRET")
RWConfig.env_bool("RW_DATABASE_DEBUG", False)
if not RWConfig["RW_DATABASE_SECRET"]:
    raise RWDataLayerException(
        """
Missing DATABASE secret key (env: RW_DATABASE_SECRET). Try with one of these:
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


# region --- Backend Classes ---
class RWMysqlBackend(databases.Database):
    def __init__(self, endpoints, params):
        if isinstance(endpoints, str):
            self.endpoints = endpoints.split(",")
        elif not isinstance(endpoints, list):
            self.endpoints = [endpoints]
        else:
            self.endpoints = endpoints

        self.params = params

        username = self.params.get("username", None)
        password = self.params.get("password", None)
        url = "mysql://"
        if username or password:
            url += "%s:%s" % (username, password)

        url += "@%s" % get_random_element(self.endpoints)

        db_name = self.params.get("db_name", None)
        if db_name:
            url += "/%s" % db_name

        self.server_code = self.params.get("server_code", "0")
        super().__init__(url, echo=RWConfig["RW_DATABASE_DEBUG"])

    async def get_uuid(self):
        uuid = await self.fetch_val("SELECT UUID() as uuid")
        if self.server_code is not None:
            uuid = uuid[0:24] + str(self.server_code).zfill(4) + uuid[28:]

        uuid_rev = uuid[24:] + uuid[19:23] + uuid[14:18] + uuid[9:13] + uuid[:8]
        return uuid_rev.upper()


class RWRedisBackend:
    _redis = None

    def __init__(self, endpoints, params):
        if isinstance(endpoints, str):
            endpoints = endpoints.split(",")
        elif not isinstance(endpoints, list):
            endpoints = [endpoints]

        self._url = "redis://%s/%s" % (
            get_random_element(endpoints),
            params.get("db", 0),
        )

    async def __aenter__(self):
        await self.connect()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        self._redis = await aioredis.create_redis(self._url, encoding="utf-8")

    async def disconnect(self):
        if self._redis:
            self._redis.close()
            await self._redis.wait_closed()
            self._redis = None

    @property
    def is_connected(self):
        return True if self._redis else False

    def __getattr__(self, item):
        if not self._redis:
            raise Exception("Redis is not connected")

        return getattr(self._redis, item)


# endregion

# region --- Datazone classes ---
class RWDatazone(ABC):
    models = []
    controllers = []
    multi_tenancy = RWMultiTenancyEnum.GLOBAL
    schema_path = None

    def __init_subclass__(cls, **kwargs):
        cls.schema_path = os.path.join(
            os.path.dirname(os.path.realpath(inspect.getmodule(cls).__file__)),
            "migrations",
        )


# endregion


class RWDataLayer:
    _backends = {}
    _datazones = {}
    _models = {}

    # region --- Backend Methods ---
    @classmethod
    def add_backend(
        cls,
        backend_type,
        backend_id,
        backend_name,
        backend_destination,
        endpoints,
        params,
    ):
        if backend_name in cls._backends.keys():
            raise RWDataLayerException("Backend %s already exists" % backend_name)

        if not endpoints:
            raise RWDataLayerException(
                "No endpoints specified for backend %s" % backend_name
            )

        if isinstance(endpoints, str):
            endpoints = endpoints.split(",")
        elif not isinstance(endpoints, list):
            endpoints = [endpoints]

        if backend_type == RWBackendTypeEnum.MYSQL:
            backend_class = RWMysqlBackend
        elif backend_type == RWBackendTypeEnum.REDIS:
            backend_class = RWRedisBackend
        else:
            raise NotImplementedError

        cls._backends[backend_name] = {
            "id": backend_id,
            "name": backend_name,
            "type": backend_type,
            "destination": backend_destination,
            "class": backend_class,
            "endpoints": endpoints,
            "params": params or {},
        }

    # endregion

    # region --- Datazone Methods ---
    @classmethod
    def get_datazones(cls):
        return cls._datazones

    @classmethod
    def add_datazone(
        cls,
        datazone_name,
        models,
        controllers,
        multi_tenancy,
        schema_path=None,
    ):
        if datazone_name not in cls._datazones.keys():
            cls._datazones[datazone_name] = {
                "multi_tenancy": multi_tenancy,
                "schema_path": schema_path,
                "controllers": controllers,
            }

        for model in models:
            cls._models[model.__name__] = datazone_name

    @classmethod
    def get_datazone_from_model(cls, model):
        datazone = cls._models.get(model.__name__, None)
        if not datazone:
            raise Exception("No datazone for model %s" % model.__name__)
        return datazone

    # @classmethod
    # def get_datazone_tenant_params(cls, datazone_name, tenant_id):
    #     if datazone_name not in cls._datazones.keys():
    #         raise Exception("Datazone %s does not exists." % datazone_name)
    #
    #     if tenant_id not in cls._datazones[datazone_name]["tenants"]:
    #         raise Exception(
    #             "Configuration %s for datazone %s does not exists."
    #             % (tenant_id, datazone_name)
    #         )
    #
    #     return cls._datazones[datazone_name]["tenants"][tenant_id]
    #
    # @classmethod
    # def set_datazone_tenant_params(cls, datazone_name, tenant_id, tenant_params):
    #     tenant_id = tenant_id or "GLOBAL"
    #     if datazone_name not in cls._datazones.keys():
    #         raise Exception("Datazone %s does not exists." % datazone_name)
    #
    #     cls._datazones[datazone_name][tenant_id] = tenant_params
    # endregion

    @classmethod
    async def _get_datapath(cls, datazone_name, tenant_id):
        """
        # TODO write this better: datazone and tenant_id are UNIQUE as a pair
        """
        if isinstance(tenant_id, str):
            tenant_id = bytes.fromhex(tenant_id)

        params = {
            "username": RWConfig["RW_BACKEND_USERNAME"],
            "password": RWConfig["RW_BACKEND_PASSWORD"],
            "db_name": RWConfig["RW_BACKEND_DB_NAME"],
        }
        params.update(json.loads(RWConfig["RW_BACKEND_PARAMS"]))
        async with RWMysqlBackend(RWConfig["RW_BACKEND_ENDPOINTS"], params) as db:
            model = import_string("red_warden.datazones.RWManager.RWDatapathModel")
            datapath = await db.fetch_one(
                model.select().where(
                    sqlalchemy.and_(
                        model.c.datazone == datazone_name,
                        model.c.tenant_id == tenant_id,
                    )
                )
            )

            if not datapath:
                return None
            else:
                datapath = await model.after_load(db, datapath)
                datapath["backend"] = next(
                    (
                        backend
                        for backend_name, backend in cls._backends.items()
                        if backend["id"] == datapath["backend_id"]
                    ),
                    None,
                )

                if datapath["backend"] and tenant_id:
                    model = import_string(
                        "red_warden.datazones.RWManager.RWTenantModel"
                    )
                    tenant = await db.fetch_one(
                        model.select().where(
                            model.c.id == bytes.fromhex(datapath["tenant_id"])
                        )
                    )
                    if tenant:
                        tenant = await model.after_load(db, tenant)
                        datapath["backend"]["params"].update(tenant["params"])

                return datapath

    @classmethod
    async def _set_datapath(cls, datazone, tenant_id, backend_name, version):
        params = {
            "username": RWConfig["RW_BACKEND_USERNAME"],
            "password": RWConfig["RW_BACKEND_PASSWORD"],
            "db_name": RWConfig["RW_BACKEND_DB_NAME"],
        }
        params.update(json.loads(RWConfig["RW_BACKEND_PARAMS"]))
        async with RWMysqlBackend(RWConfig["RW_BACKEND_ENDPOINTS"], params) as db:
            model = import_string("red_warden.datazones.RWManager.RWBackendModel")
            backend = await db.fetch_one(
                model.select().where(model.c.name == backend_name)
            )

            model = import_string("red_warden.datazones.RWManager.RWDatapathModel")
            datapath = await db.fetch_one(
                model.select().where(
                    sqlalchemy.and_(
                        model.c.datazone == datazone, model.c.tenant_id == tenant_id
                    )
                )
            )

            data = {
                "datazone": datazone,
                "backend_id": bytes.hex(backend["id"]),
                "tenant_id": tenant_id,
                "version": version,
            }
            if not datapath:
                data = await model.before_create(db, data, True)
                await db.execute(model.insert().values(data))
            else:
                data = await model.before_update(db, data, True)
                await db.execute(
                    model.update().where(model.c.id == datapath["id"]).values(data)
                )

    @classmethod
    async def _execute_datapath_schema_migrations(cls, datazone, actual_version, db):
        version = actual_version
        datazone_path = cls._datazones[datazone]["schema_path"]
        if os.path.exists(datazone_path):
            files = os.listdir(datazone_path)
            files.sort()

            for file in files:
                name, ext = os.path.splitext(file)
                if ext == ".py" and int(name) > version:
                    version = int(name)
                    spec = importlib.util.spec_from_file_location(
                        "migration", os.path.join(datazone_path, file)
                    )
                    migration = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(migration)
                    await migration.upgrade(db)

        return version

    @classmethod
    async def upgrade_manager_datapath_schema(cls):
        endpoints = RWConfig["RW_BACKEND_ENDPOINTS"]
        params = {
            "username": RWConfig["RW_BACKEND_USERNAME"],
            "password": RWConfig["RW_BACKEND_PASSWORD"],
            "db_name": RWConfig["RW_BACKEND_DB_NAME"],
        }
        params.update(json.loads(RWConfig["RW_BACKEND_PARAMS"]))

        datapath = None
        db = RWMysqlBackend(endpoints, params)
        try:
            async with db:
                datapath_table_exists = await db.fetch_all(
                    "SHOW TABLES LIKE 'datapath'"
                )
                if datapath_table_exists:
                    datapath = await cls._get_datapath("RWManager", None)
        except:
            pass

        new_version = await cls._execute_datapath_schema_migrations(
            "RWManager", datapath["version"] if datapath else 0, db
        )

        if not datapath or (datapath["version"] != new_version and new_version > 0):
            await cls._set_datapath("RWManager", None, "rw_global", new_version)

        await cls.reload_backends()

    @classmethod
    async def _create_mysql_db_and_upgrade_datapath_migrations(
        cls, datazone_name, tenant_id
    ):
        datapath = await cls._get_datapath(datazone_name, tenant_id)

        if datapath:
            backend = datapath["backend"]
            if tenant_id:
                backend["params"]["db_name"] = tenant_id

        elif tenant_id:
            # we have a tenant_id, but no backend configured.
            # Let's choose a random one from the TENANT_AVAILABLE backends
            tenant_backends = list(
                backend
                for backend_name, backend in cls._backends.items()
                if backend["type"] == RWBackendTypeEnum.MYSQL
                and backend["destination"] == RWBackendDestinationEnum.TENANTS_AVAILABLE
            )
            if not tenant_backends:
                raise RWDataLayerException("No backend available for tenant creation")

            backend = random.choice(tenant_backends)
            backend["params"]["db_name"] = tenant_id
        else:
            # we have no datapath and no tenant, so we need a global backend.
            backend = cls._backends["rw_global"]

        # creates the designated database, if not present
        async with RWMysqlBackend(
            backend["endpoints"],
            {
                "username": backend["params"].get("username", None),
                "password": backend["params"].get("password", None),
            },
        ) as db:
            # check if database exists, else creates it
            db_exists = await db.fetch_val(
                "SHOW DATABASES LIKE :db_name",
                {"db_name": backend["params"].get("db_name", None)},
            )
            if not db_exists:
                await db.execute(
                    "CREATE DATABASE %s DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci"
                    % backend["params"].get("db_name", None)
                )

                # ensure all grants are set for this user to the Manager database and tables
                await db.execute(
                    "GRANT ALL ON %s.* TO :username@'%%'"
                    % backend["params"].get("db_name", None),
                    {"username": backend["params"].get("username", None)},
                )

        old_version = datapath["version"] if datapath else 0
        async with RWMysqlBackend(backend["endpoints"], backend["params"]) as db:
            new_version = await cls._execute_datapath_schema_migrations(
                datazone_name, old_version, db
            )
        if not datapath or (datapath["version"] != new_version and new_version > 0):
            await cls._set_datapath(
                datazone_name, tenant_id, backend["name"], new_version
            )

        if old_version != new_version:
            return {
                "datazone": datazone_name,
                "tenant": tenant_id,
                "old_version": datapath["version"] if datapath else 0,
                "new_version": new_version,
            }
        else:
            return None

    @classmethod
    async def upgrade_other_datapaths_migrations(cls, tenant_id=None):
        results = []

        for datazone_name, datazone in cls._datazones.items():
            if datazone_name != "RWManager":
                if datazone["multi_tenancy"] == RWMultiTenancyEnum.GLOBAL:
                    result = await cls._create_mysql_db_and_upgrade_datapath_migrations(
                        datazone_name, None
                    )
                    if result:
                        results.append(result)

                else:  # multi_tenancy = RWMultiTenancyEnum.TENANT
                    params = {
                        "username": RWConfig["RW_BACKEND_USERNAME"],
                        "password": RWConfig["RW_BACKEND_PASSWORD"],
                        "db_name": RWConfig["RW_BACKEND_DB_NAME"],
                    }
                    params.update(json.loads(RWConfig["RW_BACKEND_PARAMS"]))
                    async with RWMysqlBackend(
                        RWConfig["RW_BACKEND_ENDPOINTS"], params
                    ) as db:
                        if tenant_id:
                            result = await cls._create_mysql_db_and_upgrade_datapath_migrations(
                                datazone_name, tenant_id
                            )
                            if result:
                                results.append(result)
                        else:
                            model = import_string(
                                "red_warden.datazones.RWManager.RWTenantModel"
                            )
                            tenants = await db.fetch_all(model.select())
                            for t in tenants:
                                t = await model.after_load(db, t)
                                result = await cls._create_mysql_db_and_upgrade_datapath_migrations(
                                    datazone_name, t["id"]
                                )
                                if result:
                                    results.append(result)

        return results

    @classmethod
    async def reload_backends(cls):
        cls._backends = {}

        # check for datapath table, it manages the schema versioning
        params = {
            "username": RWConfig["RW_BACKEND_USERNAME"],
            "password": RWConfig["RW_BACKEND_PASSWORD"],
            "db_name": RWConfig["RW_BACKEND_DB_NAME"],
        }
        params.update(json.loads(RWConfig["RW_BACKEND_PARAMS"]))
        async with RWMysqlBackend(RWConfig["RW_BACKEND_ENDPOINTS"], params) as db:
            model = import_string("red_warden.datazones.RWManager.RWBackendModel")
            backends = await db.fetch_all(model.select().where(model.c.enabled == "Y"))
            for b in backends:
                b = await model.after_load(db, b)
                if b["type"] == "mysql":
                    backend_type = RWBackendTypeEnum.MYSQL
                # elif b.type == "mongodb":  TODO add mongodb support
                #    backend_class = RWMongoDbBackend
                elif b["type"] == "redis":
                    backend_type = RWBackendTypeEnum.REDIS

                cls.add_backend(
                    backend_type,
                    b["id"],
                    b["name"],
                    b["destination"],
                    b["endpoints"],
                    b["params"],
                )

    @classmethod
    async def get_backend_from_datapath(cls, datazone_name, tenant_id=None):
        if datazone_name not in cls._datazones.keys():
            raise RWDataLayerException("Datazone %s does not exist" % datazone_name)

        datapath = await cls._get_datapath(datazone_name, tenant_id)
        new_backend = copy.deepcopy(datapath["backend"])
        return new_backend

        # try:
        #     tenant_params = cls.get_datazone_tenant_params(datazone_name, tenant_id)
        # except:
        #     pass
        #
        # backend = cls._backends.get(backend_name, None)
        # if not backend:
        #     raise RWBackendException("Backend %s does not exist" % backend_name)
        #
        # endpoint = endpoint or choice(backend["endpoints"])
        # params = backend["params"]
        # if additional_params:
        #     params.update(additional_params)
        #
        # if not hasattr(request.state, "backends"):
        #     request.state.backends = {}
        #
        # instance_hash = cls._calc_instance_hash(endpoint, params)
        # if instance_hash not in request.state.backends.keys():
        #     request.state.backends[instance_hash] = backend["class"](endpoint, params)
        #
        # return request.state.backends[instance_hash]

    @staticmethod
    def get_sort_columns(table, sort_args):
        if isinstance(sort_args, str):
            sort_args = [sort_args]

        sort = []
        for s in sort_args:
            if s:
                if s[0] == "-":
                    s = s[1:]
                    desc = True
                else:
                    desc = False

                if not hasattr(table.c, s):
                    raise Exception("Wrong sort field: %s" % s)
                if desc:
                    sort.append(table.c[s].desc())
                else:
                    sort.append(table.c[s])

        if not sort:
            sort = [table.primary_key[0]]

        return sort

    @staticmethod
    def get_filters(model, table, filters_args):
        filters = []
        special_columns = model.get_special_columns()
        for f in filters_args:
            k_op_v = f.split(":")
            if len(k_op_v) == 2:
                k = k_op_v[0]
                op = "eq"
                v = k_op_v[1]
            elif len(k_op_v) == 3:
                k, op, v = k_op_v
            else:
                raise RWDataLayerException("Wrong filter definition: %s" % f)

            if not hasattr(table.c, k):
                raise RWDataLayerException("Wrong filter field: %s" % k)

            if v == "None":
                v = None
            elif k in special_columns["id"]:
                v = bytes.fromhex(v)

            if op == "eq":
                filters.append(table.c[k] == v)
            elif op == "ne":
                filters.append(table.c[k] != v)
            elif op == "lt":
                filters.append(table.c[k] < v)
            elif op == "lte":
                filters.append(table.c[k] <= v)
            elif op == "gt":
                filters.append(table.c[k] > v)
            elif op == "gte":
                filters.append(table.c[k] >= v)
            elif op == "like":
                filters.append(table.c[k].like("%" + v + "%"))
            elif op == "ilike":
                filters.append(table.c[k].ilike("%" + v + "%"))
            elif op == "not_like":
                filters.append(~table.c[k].like("%" + v + "%"))
            elif op == "not_ilike":
                filters.append(~table.c[k].ilike("%" + v + "%"))
            elif op == "in":
                filters.append(table.c[k].in_(v.split("|")))
            elif op == "not_in":
                filters.append(~table.c[k].in_(v.split("|")))
            else:
                raise RWDataLayerException("Wrong filter operator: %s" % op)

        return filters

    @classmethod
    async def load_by_id(cls, model, model_id, identity=None):
        tenant_id = identity.get("tenant_id", None) if identity else None

        if isinstance(model_id, str):
            try:
                int(model_id, 16)
                model_id = bytes.fromhex(model_id)
            except ValueError:
                raise RWDataLayerException("Malformed ID")

        datazone = cls.get_datazone_from_model(model)
        backend = await cls.get_backend_from_datapath(datazone, tenant_id)
        async with backend["class"](backend["endpoints"], backend["params"]) as db:
            query = model.get_select_query()

            row = await db.fetch_one(query.where(model.c.id == model_id))
            if row:
                return await model.after_load(db, row)
            else:
                return None

    @classmethod
    async def load_one(cls, model, identity=None, filters=None):
        filters = filters or []
        tenant_id = identity.get("tenant_id", None) if identity else None
        if isinstance(model, str):
            model = import_string(model)

        datazone = cls.get_datazone_from_model(model)
        backend = await cls.get_backend_from_datapath(datazone, tenant_id)
        async with backend["class"](backend["endpoints"], backend["params"]) as db:
            query = model.get_select_query().cte("resolved")
            filter_columns = cls.get_filters(model, query, filters)
            cte = (
                sqlalchemy.select(
                    [
                        *query.c,
                    ]
                )
                .where(sqlalchemy.and_(*filter_columns))
                .cte("ordered")
            )
            row = await db.fetch_one(cte.select())
            if row:
                return await model.after_load(db, row)
            else:
                return None

    @classmethod
    async def load_all(
        cls, model, identity=None, pagination=None, sort=None, filters=None
    ):
        sort = sort or []
        filters = filters or []
        pagination = pagination or {"after": None, "before": None, "limit": 25}
        tenant_id = identity.get("tenant_id", None) if identity else None

        if isinstance(model, str):
            model = import_string(model)

        datazone = cls.get_datazone_from_model(model)
        backend = await cls.get_backend_from_datapath(datazone, tenant_id)
        async with backend["class"](backend["endpoints"], backend["params"]) as db:
            query = model.get_select_query()

            cte_resolved = query.cte("resolved")

            try:
                limit = int(pagination["limit"]) or 25
                if limit > 500:
                    limit = 500
            except ValueError:
                limit = 25

            cursor_hint = pagination["after"] or pagination["before"]
            if cursor_hint:
                try:
                    cursor = json.loads(base64.b64decode(cursor_hint.encode()).decode())
                except Exception:
                    raise RWDataLayerException("Wrong cursor format")

                sort_columns = cls.get_sort_columns(cte_resolved, cursor["sort"])
                filter_columns = cls.get_filters(model, cte_resolved, cursor["filters"])
            else:
                cursor = None
                sort_columns = cls.get_sort_columns(cte_resolved, sort)
                filter_columns = cls.get_filters(model, cte_resolved, filters)

            cte_ordered = (
                sqlalchemy.select(
                    [
                        sqlalchemy.func.row_number()
                        .over(order_by=sort_columns)
                        .label("n"),
                        *cte_resolved.c,
                    ]
                )
                .where(sqlalchemy.and_(*filter_columns))
                .cte("ordered")
            )

            q = cte_ordered.select()
            total_count = await db.fetch_one(
                sqlalchemy.select([sqlalchemy.func.count().label("total")]).select_from(
                    q.alias("ordered")
                )
            )
            total_count = total_count["total"]

            if cursor:
                cte_id_check = (
                    sqlalchemy.select([cte_ordered.c.n]).where(
                        cte_ordered.c.id == bytes.fromhex(cursor["id"])
                    )
                ).cte("id_check")

                if pagination["after"]:
                    q = q.where(
                        cte_ordered.c.n
                        > sqlalchemy.sql.func.ifnull(cte_id_check.c.n, 0)
                    )
                elif pagination["before"]:
                    q = q.where(
                        cte_ordered.c.n
                        > sqlalchemy.sql.func.ifnull(cte_id_check.c.n, 0) - limit
                    )

            if limit:
                q = q.limit(limit)

            def encode_cursor(row):
                _cursor = {
                    "id": "".join("{:02x}".format(b) for b in row.id),
                }
                if cursor:
                    _cursor["filters"] = cursor.get("filters", {})
                    _cursor["sort"] = cursor.get("sort", {})
                else:
                    _cursor["filters"] = filters
                    _cursor["sort"] = sort
                return base64.b64encode(json.dumps(_cursor).encode()).decode()

            data = await db.fetch_all(q)

            if len(data):
                start_cursor = encode_cursor(data[0])
                end_cursor = encode_cursor(data[-1])
                has_previous_page = data[0].n > 1
                has_next_page = data[-1].n < total_count

            else:
                start_cursor = None
                end_cursor = None
                if pagination["after"]:
                    has_previous_page = total_count > 0
                    has_next_page = False
                elif pagination["before"]:
                    has_previous_page = False
                    has_next_page = total_count > 0
                else:
                    has_previous_page = False
                    has_next_page = False

            return [await model.after_load(db, row) for row in data], {
                "count": len(data),
                "total": total_count,
                "start": start_cursor,
                "end": end_cursor,
                "prev": has_previous_page,
                "next": has_next_page,
            }

    @classmethod
    async def save(cls, model, model_id, data, identity=None, skip_validation=False):
        tenant_id = identity.get("tenant_id", None) if identity else None

        if isinstance(model, str):
            model = import_string(model)

        datazone = cls.get_datazone_from_model(model)
        backend = await cls.get_backend_from_datapath(datazone, tenant_id)
        async with backend["class"](backend["endpoints"], backend["params"]) as db:
            if model_id:
                data = await model.before_update(db, data, skip_validation)
                await db.execute(
                    model.update()
                    .where(model.c.id == bytes.fromhex(model_id))
                    .values(data)
                )
            else:
                data = await model.before_create(db, data, skip_validation)
                await db.execute(model.insert().values(data))
                model_id = data["id"]

            return await cls.load_by_id(model, model_id, identity)

    @classmethod
    async def remove(cls, model, model_id, identity=None):
        tenant_id = identity.get("tenant_id", None) if identity else None

        if isinstance(model, str):
            model = import_string(model)

        datazone = cls.get_datazone_from_model(model)
        backend = await cls.get_backend_from_datapath(datazone, tenant_id)
        async with backend["class"](backend["endpoints"], backend["params"]) as db:
            row_count = await db.execute(
                model.delete().where(model.c.id == bytes.fromhex(model_id))
            )
            if row_count == 0:
                return None
            else:
                return model_id
