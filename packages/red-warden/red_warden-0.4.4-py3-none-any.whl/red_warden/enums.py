from enum import Enum


class RWMultiTenancyEnum(str, Enum):
    GLOBAL = "global"
    TENANT = "tenant"


class RWBackendTypeEnum(str, Enum):
    MYSQL = "mysql"
    MONGODB = "mongodb"
    REDIS = "redis"


class RWBackendDestinationEnum(str, Enum):
    GLOBAL = "global"
    TENANTS_AVAILABLE = "tenants_available"
    TENANTS_FULL = "tenants_full"


class RWYesNoEnum(str, Enum):
    YES = "Y"
    NO = "N"
