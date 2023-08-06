from red_warden.graphql import (
    RWGraphQLConnection,
    RWGraphQLStringFilter,
)
from models import DatapathModel
from schemas.datapath.types import Datapath


class DatapathConnection(RWGraphQLConnection):
    class Meta:
        node = Datapath
        filters = {"default": {"name": RWGraphQLStringFilter()}}

    @staticmethod
    def resolve_all(_, info, **args):
        return DatapathModel.select()

    @staticmethod
    async def resolve_all_by_backend(parent, info, **args):
        return DatapathModel.select().where(DatapathModel.c.backend_id == parent.id)
