import json
import base64
import graphene
import httpx
import sqlalchemy
import inspect
import functools
from graphene.utils.module_loading import import_string

_nodes = {}


class RWGraphQLClient:
    _endpoint = None

    def __init__(self, endpoint, **kwargs):
        self._endpoint = endpoint
        super().__init__(**kwargs)

    async def execute(self, payload, **kwargs):
        max_retries = kwargs.pop("max_retries", 5)

        retries = 0
        last_error = None
        while retries < max_retries:
            async with httpx.AsyncClient() as client:
                try:
                    r = await client.post(
                        self._endpoint,
                        json=payload,
                        **kwargs,
                    )
                    r.raise_for_status()
                    return r.json()

                except (httpx.ReadTimeout, httpx.ReadTimeout) as error:
                    last_error = error
                    retries += 1

        raise Exception("Cannot execute query: %s" % last_error)


class RWGraphQLYesNoField(graphene.Enum):
    Yes = "Y"
    No = "N"


class RWGraphQLConnection(graphene.Connection):
    filters = None
    count = graphene.Int()
    total_count = graphene.Int()

    @classmethod
    def __init_subclass_with_meta__(cls, node=None, name=None, **options):
        if isinstance(node, str):
            node = import_string(node)
        setattr(cls, "filters", options.pop("filters", None))
        super().__init_subclass_with_meta__(node=node, name=name, options=options)

    class Meta:
        abstract = True

    @staticmethod
    def resolve_count(root, info, **kwargs):
        return len(root.edges)

    @staticmethod
    def create_field_from_import(class_and_method, filters=None, **kwargs):
        class_path, method_name = class_and_method.rsplit(".", 1)
        connection_class = lambda: import_string(class_path)
        method_name = "resolve_" + method_name
        return RWGraphQLMysqlConnectionField(
            connection_type=connection_class,
            resolver=method_name,
            filters=filters,
            **kwargs,
        )

    @classmethod
    def create_field(cls, method_name, filters=None, **kwargs):
        if not filters and cls.filters:
            filters = cls.filters.get(method_name, None)

        method_name = "resolve_" + method_name
        method = getattr(cls, method_name)
        if not method:
            raise Exception("Unknown method for connection field: %s" % method_name)

        if filters:
            method_filters_class = cls.__name__ + "_" + method_name + "_filters"
            filters_class = type(
                method_filters_class, (graphene.InputObjectType,), filters
            )
            filters = filters_class()

        return RWGraphQLMysqlConnectionField(
            cls, resolver=method, filters=filters, **kwargs
        )


class RWGraphQLNumberFilter(graphene.InputObjectType):
    eq = graphene.Float()
    ne = graphene.Float()
    gt = graphene.Float()
    gte = graphene.Float()
    lt = graphene.Float()
    lte = graphene.Float()
    one_of = graphene.List(graphene.Float)
    not_one_of = graphene.List(graphene.Float)


class RWGraphQLStringFilter(graphene.InputObjectType):
    eq = graphene.String()
    ne = graphene.String()
    like = graphene.String()
    ilike = graphene.String()
    not_like = graphene.String()
    not_ilike = graphene.String()
    one_of = graphene.List(graphene.String)
    not_one_of = graphene.List(graphene.String)


class RWGraphQLMysqlConnectionField(graphene.ConnectionField):
    def __init__(self, connection_type, *args, **kwargs):
        if "args" not in kwargs:
            kwargs["args"] = {}

        resolver = kwargs["resolver"]
        resolver_name = resolver if isinstance(resolver, str) else resolver.__name__
        filters = kwargs.pop("filters", None)
        if not filters and not (
            inspect.isfunction(connection_type)
            or isinstance(connection_type, functools.partial)
        ):
            filters = connection_type.filters.get(resolver_name, None)
            if not filters:
                filters = connection_type.filters.get("default", None)

        if filters:
            method_filters_class = (
                connection_type.__name__ + "_" + resolver_name + "_filters"
            )
            filters_class = type(
                method_filters_class, (graphene.InputObjectType,), filters
            )
            filters = filters_class()
            kwargs["args"]["filters"] = filters

        kwargs["args"]["sort"] = graphene.List(graphene.String)
        super().__init__(connection_type, *args, **kwargs)

    @classmethod
    async def connection_resolver(cls, resolver, connection_type, root, info, **args):
        if isinstance(resolver, str):
            resolver = getattr(connection_type, resolver)

        # the db connection used depends on the datazone of the node's model
        new_args = {
            "db": connection_type._meta.node.model.get_datazone_db(info),
            "filters": args.pop("filters", {}),
            "sort": args.pop("sort", []),
            "pagination": {
                "after": args.pop("after", None),
                "before": args.pop("before", None),
                "first": args.pop("first", 0),
                "last": args.pop("last", 0),
            },
        }

        return super().connection_resolver(
            resolver, connection_type, root, info, **new_args
        )

    @staticmethod
    def get_sort_columns(table, sort_args):
        sort = []
        for s in sort_args:
            if s[0] == "-":
                s = s[1:]
                desc = True
            else:
                desc = False

            if not hasattr(table.c, s):
                raise Exception("Wrong sort field: %s" % s)
            if desc:
                sort.append(table.c[s].desc())
            else:
                sort.append(table.c[s])
        if not sort:
            sort = [table.c.id]
        return sort

    @staticmethod
    def get_filters(table, filters_args):
        filters = []
        for k, v in filters_args.items():
            if not hasattr(table.c, k):
                raise Exception("Wrong filter field: %s" % k)

            if isinstance(v, dict):
                eq = v.get("eq", None)
                ne = v.get("ne", None)
                gt = v.get("gt", None)
                gte = v.get("gte", None)
                lt = v.get("lt", None)
                lte = v.get("lte", None)
                like = v.get("like", None)
                ilike = v.get("ilike", None)
                not_like = v.get("not_like", None)
                not_ilike = v.get("not_ilike", None)
                one_of = v.get("one_of", None)
                not_one_of = v.get("not_one_of", None)

                if eq:
                    filters.append(table.c[k] == eq)
                if ne:
                    filters.append(table.c[k] != ne)
                if lt:
                    filters.append(table.c[k] < lt)
                if lte:
                    filters.append(table.c[k] <= lte)
                if gt:
                    filters.append(table.c[k] > gt)
                if gte:
                    filters.append(table.c[k] >= gte)
                if like:
                    filters.append(table.c[k].like("%" + like + "%"))
                if ilike:
                    filters.append(table.c[k].ilike("%" + ilike + "%"))
                if not_like:
                    filters.append(~table.c[k].like("%" + not_like + "%"))
                if not_ilike:
                    filters.append(~table.c[k].ilike("%" + not_ilike + "%"))
                if one_of:
                    filters.append(table.c[k].in_(one_of))
                if not_one_of:
                    filters.append(~table.c[k].in_(not_one_of))
            else:
                filters.append(table.c[k] == v)

        return filters

    @classmethod
    async def resolve_connection(cls, connection_type, args, resolved):
        pagination = args["pagination"]

        cte_resolved = resolved.cte("resolved")

        limit = int(pagination["first"]) or int(pagination["last"]) or 25
        cursor_hint = pagination["after"] or pagination["before"]
        if cursor_hint:
            try:
                cursor = json.loads(base64.b64decode(cursor_hint.encode()).decode())

            except Exception:
                raise Exception("Wrong cursor format")
            sort = cls.get_sort_columns(cte_resolved, cursor["sort"])
            filters = cls.get_filters(cte_resolved, cursor["filters"])
        else:
            cursor = None
            sort = cls.get_sort_columns(cte_resolved, args["sort"])
            filters = cls.get_filters(cte_resolved, args["filters"])

        cte_ordered = (
            sqlalchemy.select(
                [
                    sqlalchemy.func.row_number().over(order_by=sort).label("n"),
                    *cte_resolved.c,
                ]
            )
            .where(sqlalchemy.and_(*filters))
            .cte("ordered")
        )

        q = cte_ordered.select()
        total_count = await args["db"].fetch_one(
            sqlalchemy.select([sqlalchemy.func.count().label("total")]).select_from(
                q.alias("ordered")
            )
        )

        if cursor:
            cte_id_check = (
                sqlalchemy.select([cte_ordered.c.n]).where(
                    cte_ordered.c.id == bytes.fromhex(cursor["id"])
                )
            ).cte("id_check")

            if pagination["after"]:
                q = q.where(
                    cte_ordered.c.n > sqlalchemy.sql.func.ifnull(cte_id_check.c.n, 0)
                )
            elif pagination["before"]:
                q = q.where(
                    cte_ordered.c.n
                    > sqlalchemy.sql.func.ifnull(
                        sqlalchemy.cast(cte_id_check.c.n, sqlalchemy.BIGINT)
                        - limit
                        - 1,
                        0,
                    )
                )

        if limit:
            q = q.limit(limit + 1)

        def encode_cursor(_node):
            _cursor = {
                "id": "".join("{:02x}".format(b) for b in _node.id),
            }
            if cursor:
                _cursor["filters"] = cursor["filters"]
                _cursor["sort"] = cursor["sort"]
            else:
                _cursor["filters"] = args["filters"]
                _cursor["sort"] = args["sort"]
            return base64.b64encode(json.dumps(_cursor).encode()).decode()

        node_not_included = None
        edges = []
        for index, node in enumerate(await args["db"].fetch_all(q)):
            if index < limit:
                edges.append(
                    connection_type.Edge(node=node, cursor=encode_cursor(node))
                )
            else:
                node_not_included = node

        if edges:
            start_cursor = edges[0].cursor
            end_cursor = edges[-1].cursor
            has_previous_page = edges[0].node.n > 1
            has_next_page = node_not_included is not None
        else:
            start_cursor = None
            end_cursor = None
            has_previous_page = False
            has_next_page = False

        return connection_type(
            total_count=total_count["total"],
            edges=edges,
            page_info=graphene.PageInfo(
                start_cursor=start_cursor,
                end_cursor=end_cursor,
                has_previous_page=has_previous_page,
                has_next_page=has_next_page,
            ),
        )


class RWGraphQLNode(graphene.Node):
    class Meta:
        name = "Node"

    @classmethod
    def to_global_id(cls, _type, _id):
        str_id = "".join("{:02x}".format(b) for b in _id)
        return base64.b64encode(f"{_type + ':' + str_id}".encode()).decode()

    @classmethod
    async def get_node_from_global_id(
        cls, info, global_id, only_type=None, ignore_permissions=False
    ):
        _type, _id = base64.b64decode(global_id.encode()).decode().split(":")
        if only_type:
            # We assure that the node type that we want to retrieve
            # is the same that was indicated in the field type
            if not isinstance(only_type, str):
                only_type = only_type._meta.name

            if _type != only_type:
                raise Exception("Received not compatible node.")

        node_class = _nodes.get(_type, None)
        if not node_class:
            raise Exception("Node type %s does not have an associated class" % _type)
        return await node_class.get_node(info, bytes.fromhex(_id), ignore_permissions)


class RWGraphQLObjectType(graphene.ObjectType):
    model = None

    def __init_subclass__(cls, **kwargs):
        _nodes[cls.__name__] = cls
        super().__init_subclass__(**kwargs)

    @classmethod
    async def check_permissions(cls, info, node):
        raise NotImplementedError("ERROR_PERMISSIONS_NOT_SET_FOR_OBJECT")

    @classmethod
    async def get_node(cls, info, _id, ignore_permissions=False):
        if not cls.model:
            raise Exception("Missing model information for %s" % cls.__name__)

        db = cls.model.get_datazone_db(info)
        data = await db.fetch_one(cls.model.select().where(cls.model.c.id == _id))
        if data:
            node = cls()
            for k, v in data.items():
                if k in node._meta.fields.keys():
                    setattr(node, k, v)

            if ignore_permissions:
                return node
            else:
                return await cls.check_permissions(info, node)


def create_query_container(query_containers):
    if not isinstance(query_containers, list):
        query_containers = [query_containers]

    queries = {}
    for qc in query_containers:
        queries.update(qc)
    queries["node"] = RWGraphQLNode.Field()

    class_name = "graphql_query"
    the_class = type(class_name, (graphene.ObjectType,), queries)
    return the_class


def create_mutation_container(mutation_containers):
    if not isinstance(mutation_containers, list):
        mutation_containers = [mutation_containers]

    mutations = {}
    for mc in mutation_containers:
        mutations.update(mc)
    class_name = "graphql_mutation"
    the_class = type(class_name, (graphene.ObjectType,), mutations)
    return the_class
