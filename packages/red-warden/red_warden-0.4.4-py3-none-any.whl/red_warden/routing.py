import typing
from functools import wraps
from starlette.routing import Route
from red_warden.auth import auth_from_bearer_token, auth_from_session, required_scope
from red_warden.sessions import session_from_cookie
from red_warden.i18n import RWMemoryI18n
from red_warden.responses import RWJSONResponse


class RWRoutingException(Exception):
    pass


def api(_func=None):
    def decorator_api(func):
        @wraps(func)
        async def wrapper_api(request):
            request.state.api = True
            return RWJSONResponse(await func(request))

        return wrapper_api

    if _func is None:
        return decorator_api
    else:
        return decorator_api(_func)


class RWApiRoute(Route):
    def __init__(
        self,
        path: str,
        endpoint: typing.Callable,
        scopes=None,
        methods: typing.List[str] = None,
        include_in_schema: bool = True,
    ) -> None:
        name = "%s_%s" % (endpoint.__self__.__name__, endpoint.__name__)
        required_scope[name] = scopes

        super().__init__(
            path,
            api(auth_from_bearer_token(endpoint)),
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )


class RWRoute(Route):
    def __init__(
        self,
        path: str,
        endpoint: typing.Callable,
        scope=None,
        methods: typing.List[str] = None,
        include_in_schema: bool = True,
        name=None,
    ) -> None:

        if not name:
            name = "%s_%s" % (
                endpoint.__self__.__name__,
                endpoint.__name__,
            )

        required_scope[name] = scope

        super().__init__(
            path,
            session_from_cookie(auth_from_session(endpoint)),
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )

    @staticmethod
    def translate(endpoint, methods=None):
        routes = []
        route_name = "%s_%s" % (
            endpoint.__self__.__name__,
            endpoint.__name__,
        )

        translated = RWMemoryI18n.all(route_name)

        for locale, route_path in translated.items():
            if not route_path.startswith("/"):
                raise RWRoutingException(
                    "Check route path translations for route %s" % route_name
                )

            routes.append(
                RWRoute(
                    route_path,
                    endpoint,
                    name="%s_%s" % (route_name, locale),
                    methods=methods,
                )
            )
        return routes
