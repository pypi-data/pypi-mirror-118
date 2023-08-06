import graphene
from red_warden.graphql import RWGraphQLNode, RWGraphQLYesNoField
from red_warden.datazones.RWManager import TenantModel
from red_warden.datazones.graphql.tenant.types import Tenant


class CreateTenant(graphene.ClientIDMutation):
    tenant = graphene.Field(Tenant, required=True)

    class Input:
        parent_id = graphene.String()
        name = graphene.String(required=True)
        password = graphene.String(required=True)
        params = graphene.JSONString(required=False)
        enabled = RWGraphQLYesNoField(required=True)

    @classmethod
    async def mutate_and_get_payload(cls, root, info, **kwargs):
        db = TenantModel.get_datazone_db(info)

        async with db.transaction():
            kwargs["id"] = await db.get_uuid()

            parent_id = kwargs.pop("parent_id", None)
            if parent_id:
                node = await RWGraphQLNode.get_node_from_global_id(
                    info, parent_id, "Tenant", ignore_permissions=True
                )
                kwargs["parent_id"] = node.id

            await db.execute(TenantModel.insert().values(kwargs))
            kwargs.pop("parent_id", None)
            return cls(tenant=Tenant(**kwargs))
