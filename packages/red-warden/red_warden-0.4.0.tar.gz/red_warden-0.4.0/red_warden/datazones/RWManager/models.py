import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey
from datetime import datetime
import pyotp
import sqlalchemy
from red_warden.config import RWConfig
from red_warden.mvc import RWMysqlModel, RWValidationModelBase
from red_warden.enums import (
    RWBackendTypeEnum,
    RWBackendDestinationEnum,
    RWYesNoEnum,
)
from typing import Optional


class RWBackendModel(RWMysqlModel):
    table_name = "backend"

    class ValidationModel(RWValidationModelBase):
        name: str
        type: RWBackendTypeEnum
        destination: RWBackendDestinationEnum
        params: Optional[str]
        endpoints: str
        enabled: RWYesNoEnum

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column("name", sqlalchemy.String(length=250), nullable=False),
            sqlalchemy.Column(
                "type",
                sqlalchemy.Enum("mysql", "mongodb", "redis"),
                nullable=False,
            ),
            sqlalchemy.Column(
                "destination",
                sqlalchemy.Enum("global", "tenants_available", "tenants_full"),
                nullable=False,
            ),
            sqlalchemy.Column("params", sqlalchemy.String(length=250), nullable=False),
            sqlalchemy.Column(
                "endpoints", sqlalchemy.String(length=250), nullable=False
            ),
            sqlalchemy.Column(
                "enabled", sqlalchemy.Enum("Y", "N"), default="N", nullable=False
            ),
        ]

    @classmethod
    def get_special_columns(cls):
        sc = super().get_special_columns()
        sc["encrypted"].append("params")
        sc["json"].append("params")
        return sc


class RWSessionModel(RWMysqlModel):
    table_name = "session"

    class ValidationModel(RWValidationModelBase):
        key: str
        value: str
        expires_at: datetime

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column("key", sqlalchemy.String(length=50), nullable=False),
            sqlalchemy.Column("value", sqlalchemy.String(length=2048), nullable=False),
            sqlalchemy.Column("expires_at", sqlalchemy.DateTime(), nullable=False),
        ]

    @staticmethod
    def get_secret():
        return str(RWConfig["RW_SESSIONS_SECRET"])

    @classmethod
    def get_special_columns(cls):
        sc = super().get_special_columns()
        sc["encrypted"].append("value")
        sc["json"].append("value")
        return sc


class RWTenantModel(RWMysqlModel):
    table_name = "tenant"

    class ValidationModel(RWValidationModelBase):
        name: str
        params: Optional[str]
        enabled: RWYesNoEnum

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column("name", sqlalchemy.String(length=250), nullable=False),
            sqlalchemy.Column("params", sqlalchemy.String(length=250), nullable=False),
            sqlalchemy.Column(
                "enabled", sqlalchemy.Enum("Y", "N"), default="N", nullable=False
            ),
        ]

    @classmethod
    def get_special_columns(cls):
        sc = super().get_special_columns()
        sc["encrypted"].append("params")
        sc["json"].append("params")
        return sc


class RWDatapathModel(RWMysqlModel):
    table_name = "datapath"

    class ValidationModel(RWValidationModelBase):
        tenant_id: Optional[str]
        datazone: str
        backend_id: str
        db_name: Optional[str]
        version: int

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column(
                "tenant_id",
                sqlalchemy.Binary(16),
                sqlalchemy.ForeignKey("tenant.id"),
                nullable=False,
            ),
            sqlalchemy.Column(
                "datazone", sqlalchemy.String(length=250), nullable=False
            ),
            sqlalchemy.Column(
                "backend_id",
                sqlalchemy.Binary(16),
                sqlalchemy.ForeignKey("backend.id"),
                nullable=False,
            ),
            sqlalchemy.Column(
                "db_name",
                sqlalchemy.String(length=100),
            ),
            sqlalchemy.Column("version", sqlalchemy.BigInteger(), nullable=False),
        ]

    @classmethod
    def get_special_columns(cls):
        sc = super().get_special_columns()
        sc["id"].extend(["backend_id", "tenant_id"])
        return sc


class RWKeyModel(RWMysqlModel):
    table_name = "key"

    class ValidationModel(RWValidationModelBase):
        login: str
        enabled: RWYesNoEnum
        password: str

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column("login", sqlalchemy.String(length=250), nullable=False),
            sqlalchemy.Column(
                "password_hash", sqlalchemy.String(length=250), nullable=False
            ),
            sqlalchemy.Column("enabled", sqlalchemy.Enum("Y", "N"), nullable=False),
            sqlalchemy.Column("mfa_enabled", sqlalchemy.Enum("Y", "N"), nullable=False),
            sqlalchemy.Column("mfa_secret", sqlalchemy.String(length=250)),
        ]

    @classmethod
    def get_special_columns(cls):
        sc = super().get_special_columns()
        sc["encrypted"].append("mfa_secret")
        return sc

    @classmethod
    def _create_password_hash(cls, row):
        password = row.pop("password", None)
        if password:
            salt = os.urandom(32)
            kdf = Scrypt(
                salt=salt, length=32, n=2 ** 14, r=8, p=1, backend=default_backend()
            )
            b = kdf.derive(password.encode())
            row["password_hash"] = "%s.%s" % (salt.hex(), b.hex())
        return row

    @classmethod
    async def before_create(cls, db, row, skip_validation=False):
        row = await super().before_create(db, row, skip_validation)
        row = cls._create_password_hash(row)
        return row

    @classmethod
    async def before_update(cls, db, row, skip_validation=False):
        row = await super().before_update(db, row, skip_validation)
        row = cls._create_password_hash(row)
        return row

    @staticmethod
    def check_password(password_hash, password):
        try:
            salt, key = password_hash.split(".")
            kdf = Scrypt(
                salt=bytes.fromhex(salt),
                length=32,
                n=2 ** 14,
                r=8,
                p=1,
                backend=default_backend(),
            )
            kdf.verify(password.encode(), bytes.fromhex(key))
            return True

        except InvalidKey:
            return False

    @staticmethod
    def toggle_mfa(mfa_enabled, enabled):
        if enabled == RWYesNoEnum.YES:
            if mfa_enabled == RWYesNoEnum.YES:
                raise ValueError("MFA already enabled")

            return {"mfa_enabled": RWYesNoEnum.YES, "mfa_secret": pyotp.random_base32()}

        elif enabled == RWYesNoEnum.NO:
            if mfa_enabled == RWYesNoEnum.NO:
                raise ValueError("MFA already disabled")

            return {"mfa_enabled": RWYesNoEnum.NO, "mfa_secret": None}

    @staticmethod
    def check_otp(mfa_secret, otp_code):
        totp = pyotp.TOTP(mfa_secret)
        return totp.verify(otp_code)


class RWOAuth2ClientModel(RWMysqlModel):
    table_name = "oauth2_client"

    class ValidationModel(RWValidationModelBase):
        name: str
        secret: str
        grant_types: str
        response_types: str
        redirect_uris: str
        scope: Optional[str]

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column("name", sqlalchemy.String(length=250), nullable=False),
            sqlalchemy.Column("secret", sqlalchemy.String(length=150), nullable=False),
            sqlalchemy.Column(
                "grant_types", sqlalchemy.String(length=150), nullable=False
            ),
            sqlalchemy.Column(
                "response_types", sqlalchemy.String(length=150), nullable=False
            ),
            sqlalchemy.Column(
                "redirect_uris", sqlalchemy.String(length=500), nullable=False
            ),
            sqlalchemy.Column("scope", sqlalchemy.String(length=150)),
        ]

    @classmethod
    def get_special_columns(cls):
        sc = super().get_special_columns()
        sc["encrypted"].append("secret")
        return sc


class RWOAuth2AuthorizationCodeModel(RWMysqlModel):
    table_name = "oauth2_authorization_code"

    class ValidationModel(RWValidationModelBase):
        code: str
        oauth2_client_id: str
        key_id: str
        redirect_uri: str
        response_type: str
        scope: Optional[str]
        auth_time: datetime
        expires_in: int
        nonce: Optional[str]
        code_challenge: str
        code_challenge_method: str

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column("code", sqlalchemy.String(length=250), nullable=False),
            sqlalchemy.Column(
                "oauth2_client_id",
                sqlalchemy.Binary(16),
                sqlalchemy.ForeignKey("oauth2_client.id"),
                nullable=False,
            ),
            sqlalchemy.Column(
                "key_id",
                sqlalchemy.Binary(16),
                sqlalchemy.ForeignKey("key.id"),
                nullable=False,
            ),
            sqlalchemy.Column(
                "redirect_uri", sqlalchemy.String(length=150), nullable=False
            ),
            sqlalchemy.Column(
                "response_type", sqlalchemy.String(length=150), nullable=False
            ),
            sqlalchemy.Column("scope", sqlalchemy.String(length=150), nullable=False),
            sqlalchemy.Column("auth_time", sqlalchemy.DateTime(), nullable=False),
            sqlalchemy.Column("expires_in", sqlalchemy.Integer(), nullable=False),
            sqlalchemy.Column("nonce", sqlalchemy.String(length=150)),
            sqlalchemy.Column(
                "code_challenge", sqlalchemy.String(length=150), nullable=False
            ),
            sqlalchemy.Column(
                "code_challenge_method", sqlalchemy.String(length=10), nullable=False
            ),
        ]

    @classmethod
    def get_special_columns(cls):
        sc = super().get_special_columns()
        sc["id"].extend(["oauth2_client_id", "key_id"])
        return sc


class RWOAuth2TokenModel(RWMysqlModel):
    table_name = "oauth2_token"

    class ValidationModel(RWValidationModelBase):
        access_token: str
        refresh_token: Optional[str]
        scope: Optional[str]
        issued_at: datetime
        access_token_expires_in: int
        refresh_token_expires_in: int
        oauth2_client_id: str
        key_id: str
        token_type: str = "Bearer"
        revoked: RWYesNoEnum = RWYesNoEnum.NO

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column(
                "access_token", sqlalchemy.String(length=250), nullable=False
            ),
            sqlalchemy.Column("refresh_token", sqlalchemy.String(length=250)),
            sqlalchemy.Column("scope", sqlalchemy.String(length=250)),
            sqlalchemy.Column("issued_at", sqlalchemy.DateTime(), nullable=False),
            sqlalchemy.Column(
                "access_token_expires_in", sqlalchemy.Integer(), nullable=False
            ),
            sqlalchemy.Column(
                "refresh_token_expires_in", sqlalchemy.Integer(), nullable=False
            ),
            sqlalchemy.Column(
                "oauth2_client_id",
                sqlalchemy.Binary(16),
                sqlalchemy.ForeignKey("oauth2_client.id"),
                nullable=False,
            ),
            sqlalchemy.Column(
                "key_id", sqlalchemy.Binary(16), sqlalchemy.ForeignKey("key.id")
            ),
            sqlalchemy.Column(
                "token_type", sqlalchemy.String(length=250), nullable=False
            ),
            sqlalchemy.Column(
                "revoked", sqlalchemy.Enum("Y", "N"), default="N", nullable=False
            ),
        ]

    @classmethod
    def get_special_columns(cls):
        sc = super().get_special_columns()
        sc["id"].extend(["oauth2_client_id", "key_id"])
        return sc


class RWAclRoleModel(RWMysqlModel):
    table_name = "acl_role"

    class ValidationModel(RWValidationModelBase):
        name: str

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column("name", sqlalchemy.String(length=250), nullable=False),
        ]


class RWAclPermissionModel(RWMysqlModel):
    table_name = "acl_permission"

    class ValidationModel(RWValidationModelBase):
        name: str

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column("name", sqlalchemy.String(length=250), nullable=False),
        ]


class RWAclRolePermissionLinkModel(RWMysqlModel):
    table_name = "acl_role_permission_link"

    class ValidationModel(RWValidationModelBase):
        acl_role_id: str
        acl_permission_id: str

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column(
                "acl_role_id",
                sqlalchemy.Binary(16),
                sqlalchemy.ForeignKey("acl_role.id"),
                nullable=False,
            ),
            sqlalchemy.Column(
                "acl_permission_id",
                sqlalchemy.Binary(16),
                sqlalchemy.ForeignKey("acl_permission.id"),
                nullable=False,
            ),
        ]

    @classmethod
    def get_special_columns(cls):
        sc = super().get_special_columns()
        sc["id"].extend(["acl_role_id", "acl_permission_id"])
        return sc

    @classmethod
    def get_select_query(cls):
        fields = [cls.c.id]
        for c in RWAclRoleModel.c:
            fields.append(c.label(str(c).replace(".", "_")))
        for c in RWAclPermissionModel.c:
            fields.append(c.label(str(c).replace(".", "_")))

        return sqlalchemy.select(fields).select_from(cls.select().alias())


class RWAclRoleKeyLinkModel(RWMysqlModel):
    table_name = "acl_role_key_link"

    class ValidationModel(RWValidationModelBase):
        acl_role_id: str
        acl_key_id: str

    @staticmethod
    def get_db_columns():
        return [
            sqlalchemy.Column(
                "acl_role_id",
                sqlalchemy.Binary(16),
                sqlalchemy.ForeignKey("acl_role.id"),
                nullable=False,
            ),
            sqlalchemy.Column(
                "acl_key_id",
                sqlalchemy.Binary(16),
                sqlalchemy.ForeignKey("acl_key.id"),
                nullable=False,
            ),
        ]

    @classmethod
    def get_special_columns(cls):
        sc = super().get_special_columns()
        sc["id"].extend(["acl_role_id", "acl_key_id"])
        return sc
