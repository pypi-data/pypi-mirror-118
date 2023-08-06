import graphene
from red_warden.graphql import RWGraphQLNode
from models import DatapathModel
from schemas.datapath.types import Datapath


class CreateDatapath(graphene.ClientIDMutation):
    datapath = graphene.Field(Datapath, required=True)

    class Input:
        backend_id = graphene.String()
        name = graphene.String(required=True)
        params = graphene.JSONString()

    @classmethod
    async def mutate_and_get_payload(cls, root, info, **kwargs):
        db = DatapathModel.get_datazone_db(info)

        async with db.transaction():
            kwargs["id"] = await db.get_uuid()

            backend_id = kwargs.pop("backend_id", None)
            if backend_id:
                node = await RWGraphQLNode.get_node_from_global_id(
                    info, backend_id, "Backend", ignore_permissions=True
                )
                kwargs["backend_id"] = node.id

            params = kwargs.get("params", None)
            if not params:
                kwargs["params"] = {}

            await db.execute(DatapathModel.insert().values(kwargs))

            kwargs.pop("backend_id", None)
            return cls(datapath=Datapath(**kwargs))
