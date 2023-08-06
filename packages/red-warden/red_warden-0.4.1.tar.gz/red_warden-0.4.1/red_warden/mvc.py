from abc import ABC
import sqlalchemy
import json
import pydantic
from typing import Optional
from cryptography.fernet import Fernet
from mako.lookup import TemplateLookup
from mako.exceptions import TemplateLookupException
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse
from red_warden.config import RWConfig
from red_warden.datalayer import RWDataLayer


# region --- Models -------------------------------------------------------------------------------------------------
# Database table definitions.
metadata = sqlalchemy.MetaData()


class RWMysqlModelMeta(type):
    table = None

    def __getattr__(self, item):
        return getattr(self.table, item)


class RWValidationModelBase(pydantic.BaseModel):
    class Config:
        extra = "forbid"


class RWOptionalValidationModelMetaclass(pydantic.main.ModelMetaclass):
    # https://stackoverflow.com/questions/67699451/make-every-fields-as-optional-with-pydantic
    def __new__(cls, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            annotations = {**annotations, **base.__annotations__}
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]
        namespaces["__annotations__"] = annotations
        return super().__new__(cls, name, bases, namespaces, **kwargs)


class RWMysqlModel(metaclass=RWMysqlModelMeta):
    table_name = None

    class ValidationModel(RWValidationModelBase):
        pass

    def __init_subclass__(cls):
        columns = [
            sqlalchemy.Column("id", sqlalchemy.Binary(16), primary_key=True),
        ] + cls.get_db_columns()
        cls.table = sqlalchemy.Table(cls.table_name, metadata, *columns)

    @staticmethod
    def get_db_columns():
        raise NotImplementedError

    @staticmethod
    def get_secret():
        return str(RWConfig["RW_DATABASE_SECRET"])

    @classmethod
    def get_special_columns(cls):
        return {"id": ["id"], "encrypted": [], "json": []}

    @classmethod
    def get_select_query(cls):
        return cls.select()

    @classmethod
    def _encrypt_columns(cls, row):
        sc = cls.get_special_columns()

        for ec in sc["encrypted"]:
            if ec in row.keys() and row[ec]:
                fernet = Fernet(cls.get_secret())
                row[ec] = fernet.encrypt(row[ec].encode()).decode("utf-8")

    @classmethod
    def _decrypt_columns(cls, row):
        sc = cls.get_special_columns()

        for ec in sc["encrypted"]:
            if ec in row.keys() and row[ec]:
                fernet = Fernet(cls.get_secret())
                row[ec] = fernet.decrypt(row[ec].encode("utf-8")).decode("utf-8")

    @classmethod
    def _convert_id_columns_to_string(cls, row):
        sc = cls.get_special_columns()

        for ic in sc["id"]:
            if ic in row.keys() and row[ic]:
                row[ic] = bytes.hex(row[ic]).upper()

    @classmethod
    def _convert_id_columns_to_byte_array(cls, row):
        sc = cls.get_special_columns()

        for ic in sc["id"]:
            if ic in row.keys() and row[ic]:
                row[ic] = bytes.fromhex(row[ic])

    @classmethod
    def _convert_json_columns_to_object(cls, row):
        sc = cls.get_special_columns()
        for jc in sc["json"]:
            if jc in row.keys() and row[jc]:
                row[jc] = json.loads(row[jc])

    @classmethod
    def _convert_json_columns_to_string(cls, row):
        sc = cls.get_special_columns()
        for jc in sc["json"]:
            if jc in row.keys() and row[jc] and not isinstance(row[jc], str):
                row[jc] = json.dumps(row[jc])

    @classmethod
    async def after_load(cls, db, row):
        row = dict(row)
        cls._decrypt_columns(row)
        cls._convert_id_columns_to_string(row)
        cls._convert_json_columns_to_object(row)
        return row

    @classmethod
    async def before_create(cls, db, row, skip_validation=False):
        row = dict(row)
        cls._convert_json_columns_to_string(row)

        if not skip_validation:
            row = cls.ValidationModel(**dict(row)).dict()

        row["id"] = await db.get_uuid()
        cls._convert_id_columns_to_byte_array(row)
        cls._encrypt_columns(row)
        return row

    @classmethod
    async def before_update(cls, db, row, skip_validation=False):
        row = dict(row)
        cls._convert_json_columns_to_string(row)

        # validates only the fields passed to the update method
        if not skip_validation:

            class ValidationModelUpdate(
                cls.ValidationModel, metaclass=RWOptionalValidationModelMetaclass
            ):
                pass

            validated_row = ValidationModelUpdate(**row).dict()
            for k in row.keys():
                row[k] = validated_row[k]

        cls._convert_id_columns_to_byte_array(row)
        cls._encrypt_columns(row)
        return row

    @classmethod
    async def after_create(cls, db, row):
        return row

    @classmethod
    async def after_update(cls, db, row):
        return row


# endregion ---------------------------------------------------------------------------------------------------------


# region --- Controllers --------------------------------------------------------------------------------------------
class RWController(ABC):
    @classmethod
    def get_routes(cls):
        raise NotImplementedError

    @staticmethod
    def _prepare_view_data(request, view_data=None):
        if not view_data:
            view_data = {}

        def url_for(route_name, locale=None, **path_params):
            if hasattr(request.state, "i18n") and not locale:
                locale = request.state.i18n.locale

            url = None
            if locale:
                try:
                    url = request.url_for("%s_%s" % (route_name, locale), **path_params)
                except:
                    pass

            if not url:
                url = request.url_for(route_name, **path_params)

            return url

        view_data.update(
            {
                "config": RWConfig,
                "url_for": url_for,
            }
        )

        if hasattr(request.state, "i18n"):
            view_data.update({"i18n": request.state.i18n})

        if hasattr(request.state, "session"):
            view_data.update({"session": request.state.session})

        if hasattr(request.state, "identity"):
            view_data.update({"identity": request.state.identity})

        return view_data

    @classmethod
    def render_view(cls, name, request, view_data=None):
        return HTMLResponse(
            RWView.render(name, cls._prepare_view_data(request, view_data))
        )


class RWRestController(RWController, ABC):
    model = None

    def __init_subclass__(cls, **kwargs):
        if not cls.model:
            raise Exception("[%s] Model cannot be empty" % cls.__name__)

    @classmethod
    async def load_by_id(cls, request):
        model_id = request.path_params.get("id", None)

        pagination = None
        data = await RWDataLayer.load_by_id(cls.model, model_id, request.state.identity)
        if not data:
            raise HTTPException(404)

        results = {"data": data}
        if pagination:
            results["pagination"] = pagination

        return results

    @classmethod
    async def load_all(cls, request):
        pagination = {
            "after": request.query_params.get("after", None),
            "before": request.query_params.get("before", None),
            "limit": request.query_params.get("limit", 0),
        }

        sort = request.query_params.get("sort", None)
        if sort:
            sort = sort.split(",")

        filters = request.query_params.get("filters", None)
        if filters:
            filters = filters.split(",")
        else:
            filters = []

        data, pagination = await RWDataLayer.load_all(
            cls.model, request.state.identity, pagination, sort, filters
        )

        results = {"data": data}
        if pagination:
            results["pagination"] = pagination

        return results

    @classmethod
    async def create(cls, request):
        return {
            "data": await RWDataLayer.save(
                cls.model, None, await request.form(), request.state.identity
            )
        }

    @classmethod
    async def update(cls, request):
        data = await RWDataLayer.save(
            cls.model,
            request.path_params.get("id", None),
            await request.form(),
            request.state.identity,
        )
        if data:
            return {"data": data}
        else:
            raise HTTPException(404)

    @classmethod
    async def delete(cls, request):
        model_id = request.path_params.get("id", None)
        data = await RWDataLayer.remove(cls.model, model_id, request.state.identity)
        if data:
            return {"data": data}
        else:
            raise HTTPException(404)


#
# class RWStaticFilesController(RWController):
#     project_dir = None
#     output_dir = None
#
#     # TODO setup fields
#     # def __init__(self, project_dir, output_dir):
#     #     self.project_dir = project_dir
#     #     self.output_dir = output_dir
#
#     @classmethod
#     def get_routes(cls):
#         return [
#             Mount(
#                 cls.output_dir,
#                 app=StaticFiles(directory=cls.project_dir),
#                 name="static",
#             )
#         ]
#
#
# class RWGraphQLController(RWController):
#     _prefix = None
#     _schema = None
#
#     # TODO setup fields
#     # def __init__(self, query, mutation, prefix="/api"):
#     #     self._prefix = prefix
#     #     self._schema = graphene.Schema(query, mutation, auto_camelcase=False)
#     #     super().__init__()
#
#     @classmethod
#     def get_routes(cls):
#         routes = [
#             Route(
#                 cls._prefix,
#                 GraphQLApp(schema=cls._schema, executor_class=AsyncioExecutor),
#                 methods=["POST"],
#                 name="graphql",
#             ),
#         ]
#
#         return routes


# endregion ------------------------------------------------------------------------------------------------------------


# region --- Views --------------------------------------------------------------------------------------------------
class RWView:
    template_lookup = None

    @classmethod
    def render(cls, name, data=None):
        if not cls.template_lookup:
            dirs = RWConfig["RW_VIEWS_TEMPLATE_DIR"]
            if isinstance(dirs, str):
                dirs = dirs.split(",")

            cls.template_lookup = TemplateLookup(directories=[*dirs])

        try:
            mytemplate = cls.template_lookup.get_template("%s.mako" % name)
        except:
            if "i18n" in data.keys():
                mytemplate = cls.template_lookup.get_template(
                    "%s/%s.mako" % (data["i18n"].locale, name)
                )
            else:
                raise TemplateLookupException("View %s not found" % name)

        return mytemplate.render(**(data or {}))


# endregion ------------------------------------------------------------------------------------------------------------
