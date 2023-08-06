import sqlalchemy
from red_warden.graphql import (
    RWGraphQLConnection,
    RWGraphQLStringFilter,
    RWGraphQLYesNoField,
)
from red_warden.datazones.RWManager import TenantModel
from red_warden.datazones.graphql.tenant.types import Tenant


class TenantConnection(RWGraphQLConnection):
    class Meta:
        node = Tenant
        filters = {
            "default": {
                "name": RWGraphQLStringFilter(),
                "enabled": RWGraphQLYesNoField(),
            }
        }

    @staticmethod
    def resolve_all(_, info, **args):
        cte_non_recursive = (
            sqlalchemy.select(
                [
                    TenantModel.c.id,
                    TenantModel.c.name,
                    TenantModel.c.params,
                    TenantModel.c.enabled,
                    TenantModel.c.parent_id,
                    sqlalchemy.literal(1).label("level"),
                    TenantModel.c.name.label("path"),
                ]
            )
            .where(TenantModel.c.parent_id == None)
            .cte("trees", recursive=True)
        )

        cte_recursive = sqlalchemy.select(
            [
                TenantModel.c.id,
                TenantModel.c.name,
                TenantModel.c.params,
                TenantModel.c.enabled,
                TenantModel.c.parent_id,
                cte_non_recursive.c.level + 1,
                cte_non_recursive.c.path
                + sqlalchemy.literal(" > ")
                + TenantModel.c.name,
            ]
        ).where(TenantModel.c.parent_id == cte_non_recursive.c.id)

        return cte_non_recursive.union_all(cte_recursive).select()
