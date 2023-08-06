import graphene
from red_warden.graphql import (
    RWGraphQLNode,
    RWGraphQLConnection,
    RWGraphQLObjectType,
    RWGraphQLYesNoField,
)
from red_warden.datazones.RWManager import TenantModel


class Tenant(RWGraphQLObjectType):
    """A tenant, used to manage the accessed data"""

    @classmethod
    async def check_permissions(cls, info, node):
        return node

    model = TenantModel

    class Meta:
        interfaces = (RWGraphQLNode,)

    name = graphene.String(description="The tenant name")
    parent_id = graphene.String(description="The tenant parent id")
    password = graphene.String(description="The tenant password, encrypted")
    params = graphene.JSONString(description="The tenant params")
    enabled = RWGraphQLYesNoField(description="Is tenant enabled?")
    level = graphene.Int(description="The tenant nesting level")
    children = graphene.List("schemas.tenant.types.Tenant")
    # datapaths = RWGraphQLConnection.create_field_from_import(
    #     "schemas.link_tenant_datapath.connections.TenantDatapathsConnection.all"
    # )
    # keys = RWGraphQLConnection.create_field_from_import(
    #     "schemas.link_tenant_key.connections.TenantKeysConnection.all"
    # )

    @staticmethod
    async def resolve_children(parent, info, **args):
        db = TenantModel.get_datazone_db(info)
        return await db.fetch_all(
            TenantModel.select().where(TenantModel.c.parent_id == parent.id)
        )
