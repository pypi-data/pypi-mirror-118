import os
import asyncio
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from red_warden.config import RWConfig, Logger, Engines, Middlewares
from red_warden.datalayer import RWDataLayer, RWDataLayerException
from red_warden.responses import RWJSONResponse
from red_warden.helpers import exception_as_dict, ViteHelper
from red_warden.mvc import RWStaticFilesController, RWController
from red_warden.datazones.RWManager import RWManager

__version__ = "0.4.3"
Logger.info("Initializing RedWarden %s" % RWConfig["RW_NAME"])


class RedWarden:
    frontend_exception_handlers = {
        401: None,
        403: None,
        404: None,
        500: None,
    }
    _app = None
    _routes = []

    @classmethod
    def add_datazones(cls, datazones):
        for datazone in datazones:
            RWDataLayer.add_datazone(
                datazone.__name__,
                datazone.models,
                datazone.controllers,
                datazone.multi_tenancy,
                datazone.schema_path,
            )

            # datazone_permissions = set()
            for controller in datazone.controllers:
                cls._routes.extend(controller.get_routes())

            #     for route in controller.get_routes():
            #         if isinstance(route, Mount):
            #             for _route in route.routes:
            #                 if _route.permissions:
            #                     datazone_permissions |= set(_route.permissions)
            #         else:
            #             if route.permissions:
            #                 datazone_permissions |= set(route.permissions)
            #
            # acl.add({datazone.__name__: datazone_permissions})

    @classmethod
    def add_static_files_controller(cls, project_dir, output_dir):
        ctrl = RWStaticFilesController(project_dir, output_dir)
        cls._routes.extend(ctrl.get_routes())

    @classmethod
    def add_vite_support(cls, manifest_file, entry):
        RWController.add_custom_view_data(
            ViteHelper.get_js_and_css(manifest_file, entry)
        )

    # def add_graphql_controller(self, queries, mutations, prefix="/api"):
    #     self.add_controllers(
    #         RWGraphQLController(
    #             create_query_container(queries),
    #             create_mutation_container(mutations),
    #             prefix,
    #         )
    #     )

    @staticmethod
    def handle_loop_exception(loop, context):
        # context["message"] will always be there; but context["exception"] may not
        msg = context.get("exception", context["message"])
        Logger.error(f"Asyncio loop exception: {msg}")

    @classmethod
    async def _401_default_handler(cls, request, ex):
        if hasattr(request.state, "api") and request.state.api:
            return RWJSONResponse({"error": "Unauthorized"}, status_code=401)
        elif cls.frontend_exception_handlers[401]:
            return await cls.frontend_exception_handlers[401](request, ex)
        else:
            return HTMLResponse("<h1>UNAUTHORIZED :((</h1>", status_code=401)

    @classmethod
    async def _403_default_handler(cls, request, ex):
        if hasattr(request.state, "api") and request.state.api:
            return RWJSONResponse({"error": "Forbidden"}, status_code=403)
        elif cls.frontend_exception_handlers[403]:
            return await cls.frontend_exception_handlers[403](request, ex)
        else:
            return HTMLResponse("<h1>FORBIDDEN :((</h1>", status_code=403)

    @classmethod
    async def _404_default_handler(cls, request, ex):
        if hasattr(request.state, "api") and request.state.api:
            return RWJSONResponse({"error": "Not found"}, status_code=404)
        elif cls.frontend_exception_handlers[404]:
            return await cls.frontend_exception_handlers[404](request, ex)
        else:
            return HTMLResponse("<h1>NOT FOUND :((</h1>", status_code=404)

    @classmethod
    async def _500_default_handler(cls, request, ex):
        dict_ex = exception_as_dict(ex)
        if hasattr(request.state, "api") and request.state.api:
            return RWJSONResponse({"error": dict_ex}, status_code=500)
        elif cls.frontend_exception_handlers[500]:
            return await cls.frontend_exception_handlers[500](request, ex)
        else:
            return HTMLResponse("<pre>Error: %s</pre>" % str(dict_ex), status_code=500)

    @classmethod
    def start(cls):
        exception_handlers = {
            401: cls._401_default_handler,
            403: cls._403_default_handler,
            404: cls._404_default_handler,
            500: cls._500_default_handler,
        }

        cls.add_datazones([RWManager])

        # if RWConfig["RW_DEBUG"]:
        #     for r in cls._routes:
        #         if isinstance(r, Mount):
        #             for _r in r.routes:
        #                 Logger.info(_r.name)
        #         else:
        #             Logger.info(r.name)

        cls._app = Starlette(
            routes=cls._routes,
            middleware=Middlewares.get_all(),
            on_startup=[cls.on_startup],
            on_shutdown=[cls.on_shutdown],
            exception_handlers=exception_handlers,
        )

        asyncio.get_event_loop().set_exception_handler(cls.handle_loop_exception)
        return cls._app

    @classmethod
    async def on_startup(cls):
        Logger.info("Starting RedWarden %s" % RWConfig["RW_NAME"])

        await RWDataLayer.upgrade_manager_datapath_schema()

        for name, engine in Engines.get_all().items():
            asyncio.create_task(engine.run())

    @classmethod
    async def on_shutdown(cls):
        Logger.info("Terminating Red Warden...")
        for name, engine in Engines.get_all().items():
            await engine.stop()
