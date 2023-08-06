import os
import logging
from random import choice
from starlette.config import Config as StarletteConfig
from starlette.datastructures import CommaSeparatedStrings, Secret
from starlette.middleware import Middleware
from enum import Enum


class _Config(dict):
    def __init__(self):
        super().__init__()

        self._cfg = StarletteConfig()

        # --- APP Config ---
        # APP_NAME must be unique for all the application modules
        self.env_string("RW_NAME")
        self.env_string("RW_BACKEND_ENDPOINTS")
        self.env_string("RW_BACKEND_USERNAME")
        self.env_string("RW_BACKEND_PASSWORD")
        self.env_string("RW_BACKEND_DB_NAME")
        self.env_string("RW_BACKEND_PARAMS", "{}")
        self.env_secret("RW_SIGNER_SECRET")
        self.env_int("RW_SIGNER_TIMEOUT", 60)

        self.env_string("RW_PATH", default=os.getcwd())
        self.env_string("RW_ENV", default="production")
        self.env_bool("RW_DEBUG")
        self.env_string("RW_LOG_LEVEL", default="INFO")
        self.env_string(
            "RW_LOG_FORMAT",
            default=(
                "%(levelname) -8s %(asctime)s [ %(lineno) -5d] %(pathname) -50s: %(message)s"
            ),
        )  # %(thread)d for thread ID

        # --- VIEWS Config
        self["RW_VIEWS_TEMPLATE_DIR"] = os.getcwd() + "/views"

    def env_string(self, name, default=None):
        self[name] = self._cfg(name, default=default)

    def env_string_list(self, name, default=None):
        self[name] = self._cfg(name, cast=CommaSeparatedStrings, default=default or [])

    def env_bool(self, name, default=False):
        self[name] = self._cfg(name, cast=bool, default=default)

    def env_int(self, name, default=0):
        self[name] = self._cfg(name, cast=int, default=default)

    def env_secret(self, name):
        self[name] = self._cfg(name, cast=Secret, default=None)


RWConfig = _Config()

Logger = logging.getLogger(RWConfig["RW_NAME"])
Logger.setLevel(RWConfig["RW_LOG_LEVEL"])
_logger_handler = logging.StreamHandler()
Logger.addHandler(_logger_handler)
_logger_handler.setFormatter(logging.Formatter(RWConfig["RW_LOG_FORMAT"]))


if not RWConfig["RW_SIGNER_SECRET"]:
    raise Exception(
        """
Missing SIGNER secret key (env: RW_SIGNER_SECRET). Try with one of these:
%s
%s
%s
        """
        % (
            os.urandom(16).hex(),
            os.urandom(16).hex(),
            os.urandom(16).hex(),
        )
    )


class RedWardens:
    _red_wardens = {}

    @classmethod
    def get_endpoint(cls, red_warden_module_name, raise_if_missing=True):
        rw = cls._red_wardens.get(red_warden_module_name, None)
        if not rw:
            if raise_if_missing:
                raise Exception(
                    "RedWarden module %s does not exist" % red_warden_module_name
                )
            return None

        return choice(rw)

    @classmethod
    def add(cls, red_warden_module_name, endpoints):
        if not endpoints:
            raise Exception(
                "No endpoints specified for RedWarden module %s"
                % red_warden_module_name
            )
        if isinstance(endpoints, str):
            endpoints = endpoints.split(",")
        elif not isinstance(endpoints, list):
            endpoints = [endpoints]

        rw = cls._red_wardens.get(red_warden_module_name, None)
        if rw:
            raise Exception(
                "RedWarden module %s already exists" % red_warden_module_name
            )

        cls._red_wardens[red_warden_module_name] = endpoints


class Engines:
    _engines = {}

    @classmethod
    def get_all(cls):
        return cls._engines

    @classmethod
    def get(cls, engine_name, raise_if_missing=True):
        engine = cls._engines.get(engine_name, None)
        if raise_if_missing and not engine:
            raise Exception("Engine %s does not exist" % engine_name)
        return engine

    @classmethod
    def add(cls, engine_name, engine):
        cls._engines[engine_name] = engine


class Middlewares:
    _middlewares = []

    @classmethod
    def get_all(cls):
        return cls._middlewares

    @classmethod
    def insert(cls, position, middleware, **options):
        cls._middlewares.insert(position, Middleware(middleware, **options))

    @classmethod
    def add(cls, middleware, **options):
        cls._middlewares.append(Middleware(middleware, **options))
