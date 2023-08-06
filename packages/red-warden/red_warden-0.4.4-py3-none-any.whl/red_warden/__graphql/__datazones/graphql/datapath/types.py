import graphene
from red_warden.graphql import (
    RWGraphQLNode,
    RWGraphQLConnection,
    RWGraphQLObjectType,
)
from models import DatapathModel, BackendModel

# --- Nodes -------------------------------------------------------------------
class Datapath(RWGraphQLObjectType):
    model = DatapathModel

    class Meta:
        interfaces = (RWGraphQLNode,)

    backend = graphene.Field("schemas.backend.types.Backend")
    name = graphene.String(description="The datapath name")
    params = graphene.JSONString(description="A dictionary of parameters")
    tenants = RWGraphQLConnection.create_field_from_import(
        "schemas.link_tenant_datapath.connections.DatapathTenantsConnection.all"
    )

    @staticmethod
    async def resolve_backend(parent, info, **args):
        db = BackendModel.get_datazone_db(info)
        return await db.fetch_one(
            BackendModel.select().where(BackendModel.c.id == parent.backend_id)
        )
