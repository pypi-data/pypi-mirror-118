import graphene
from red_warden.graphql import (
    RWGraphQLConnection,
    RWGraphQLStringFilter,
    RWGraphQLYesNoField,
)
from red_warden.datazones.RWManager import KeyModel
from red_warden.datazones.graphql.key.types import Key


class KeyConnection(RWGraphQLConnection):
    class Meta:
        node = Key
        filters = {
            "default": {
                "login": RWGraphQLStringFilter(),
                "enabled": RWGraphQLYesNoField(),
            }
        }

    @staticmethod
    def resolve_all(_, info, **args):
        return KeyModel.select()


class TenantKeyByTenantConnectionFilters(graphene.InputObjectType):
    tenant_id = RWGraphQLStringFilter(required=True)
