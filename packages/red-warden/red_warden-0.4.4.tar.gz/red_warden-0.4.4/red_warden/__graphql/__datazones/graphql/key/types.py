import graphene
from red_warden.graphql import (
    RWGraphQLNode,
    RWGraphQLObjectType,
    RWGraphQLYesNoField,
    RWGraphQLConnection,
)
from red_warden.datazones.RWManager import KeyModel


class Key(RWGraphQLObjectType):
    """A key used for authentication"""

    @classmethod
    async def check_permissions(cls, info, node):
        return node

    model = KeyModel

    class Meta:
        interfaces = (RWGraphQLNode,)

    login = graphene.String(description="The key name")
    enabled = RWGraphQLYesNoField(description="Is key enabled?")
    mfa_enabled = RWGraphQLYesNoField(
        description="Is multifactor authentication enabled?"
    )
    # tenants = RWGraphQLConnection.create_field_from_import(
    #     "schemas.link_tenant_key.connections.KeyTenantsConnection.all"
    # )
