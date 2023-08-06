import graphene
from red_warden.graphql import (
    RWGraphQLConnection,
    RWGraphQLStringFilter,
    RWGraphQLYesNoField,
    RWGraphQLNode,
    RWGraphQLObjectType,
)
from red_warden.datazones.RWManager.models import BackendModel

# TODO from red_warden.datazones.graphql.datapath.connections import DatapathConnection


class BackendTypeField(graphene.Enum):
    Mysql = "mysql"
    MongoDB = "mongodb"
    Redis = "redis"


class Backend(RWGraphQLObjectType):
    @classmethod
    async def check_permissions(cls, info, node):
        return node

    model = BackendModel

    class Meta:
        interfaces = (RWGraphQLNode,)

    name = graphene.String(description="The backend name")
    type = BackendTypeField(description="The backend type")
    params = graphene.JSONString(description="A dictionary of parameters")
    endpoints = graphene.String(description="A comma separated list of endpoints")
    enabled = RWGraphQLYesNoField(description="Is backend enabled?")
    # TODO datapaths = DatapathConnection.create_field("all_by_backend")


class CreateBackend(graphene.ClientIDMutation):
    backend = graphene.Field(Backend, required=True)

    class Input:
        name = graphene.String(required=True)
        type = BackendTypeField(required=True)
        enabled = RWGraphQLYesNoField(required=True)
        endpoints = graphene.List(graphene.String, required=True)
        params = graphene.JSONString()

    @classmethod
    async def mutate_and_get_payload(cls, root, info, **kwargs):
        db = BackendModel.get_datazone_db(info)

        async with db.transaction():
            kwargs["id"] = await db.get_uuid()

            params = kwargs.get("params", None)
            if not params:
                kwargs["params"] = {}

            await db.execute(BackendModel.insert().values(kwargs))
            return cls(backend=Backend(**kwargs))


class BackendConnection(RWGraphQLConnection):
    class Meta:
        node = Backend
        filters = {
            "default": {
                "name": RWGraphQLStringFilter(),
                "type": BackendTypeField(),
                "enabled": RWGraphQLYesNoField(),
                "endpoints": RWGraphQLStringFilter(),
            }
        }

    @staticmethod
    def resolve_all(_, info, **args):
        return BackendModel.select()
