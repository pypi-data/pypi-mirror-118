from red_warden.datalayer import RWDatazone
from .models import (
    RWBackendModel,
    RWTenantModel,
    RWDatapathModel,
    RWKeyModel,
    RWSessionModel,
    RWOAuth2ClientModel,
    RWOAuth2AuthorizationCodeModel,
    RWOAuth2TokenModel,
    RWAclRoleModel,
    RWAclPermissionModel,
    RWAclRolePermissionLinkModel,
)
from .controllers import (
    RWBackendController,
    RWTenantController,
    RWKeyController,
    RWSessionController,
    RWOAuth2ClientController,
    RWOAuth2AuthorizationCodeController,
    RWOAuth2TokenController,
    RWOAuth2FlowController,
    RWAclRoleController,
    RWAclPermissionController,
)


class RWManager(RWDatazone):
    models = [
        RWBackendModel,
        RWTenantModel,
        RWDatapathModel,
        RWKeyModel,
        RWSessionModel,
        RWOAuth2ClientModel,
        RWOAuth2AuthorizationCodeModel,
        RWOAuth2TokenModel,
        RWAclRoleModel,
        RWAclPermissionModel,
        RWAclRolePermissionLinkModel,
    ]
    controllers = [
        RWBackendController,
        RWTenantController,
        # RWDatapathController,
        RWKeyController,
        RWSessionController,
        RWOAuth2ClientController,
        RWOAuth2AuthorizationCodeController,
        RWOAuth2TokenController,
        RWOAuth2FlowController,
        RWAclRoleController,
        RWAclPermissionController,
    ]


# class RWMysqlHistoryModel(RWMysqlModel):
#     datazone = "history"
#
#     @staticmethod
#     def get_db_columns():
#         return [
#             sqlalchemy.Column(
#                 "table_record_id", sqlalchemy.String(length=250), nullable=False
#             ),
#             sqlalchemy.Column("who", sqlalchemy.String(length=250), nullable=False),
#             sqlalchemy.Column(
#                 "why", sqlalchemy.Enum("INSERT", "UPDATE", "DELETE"), nullable=False
#             ),
#             sqlalchemy.Column("what", sqlalchemy.JSON(), nullable=False),
#             sqlalchemy.Column("when", sqlalchemy.DateTime(), nullable=False),
#             sqlalchemy.Column("description", sqlalchemy.String(length=500)),
#         ]
