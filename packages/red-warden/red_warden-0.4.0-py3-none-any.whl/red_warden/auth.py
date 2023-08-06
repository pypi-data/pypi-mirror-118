from functools import wraps
from starlette.exceptions import HTTPException
from red_warden.helpers import import_string
from red_warden.datalayer import RWDataLayer


required_scope = {}


def _check_authorization(func, identity):
    func_name = "%s_%s" % (func.__self__.__name__, func.__name__)
    global required_scope
    if func_name in required_scope.keys():
        func_scopes = required_scope[func_name]
        if func_scopes:
            if not identity:
                raise HTTPException(401)

            user_scopes = identity.get("scope", [])

            # Check if any of the method scopes are verified.
            # the logic is:
            #
            # [ "scope_01", "scope_02" ]
            # needs BOTH scopes to be verified
            #
            # [ [ "scope_03" ], [ "scope_04", "scope_05" ]
            # is verified when user has "scope_03" OR both "scope_04" AND "scope_05"

            if isinstance(func_scopes, str):
                # single scope, make a list
                func_scopes = [func_scopes]

            oks = [True] * len(func_scopes)
            for i, func_scope in enumerate(func_scopes):
                if isinstance(func_scope, str):
                    func_scope = [func_scope]

                for fs in func_scope:
                    if fs not in user_scopes:
                        oks[i] = False
                        break

            if not any(oks):
                # at least one is True, no need to check them all
                raise HTTPException(403)


def auth_from_session(_func=None):
    def decorator_auth(func):
        @wraps(func)
        async def wrapper_auth(request):
            request.state.identity = request.state.session.get("identity", {})

            _check_authorization(func, request.state.identity)

            return await func(request)

        return wrapper_auth

    if _func is None:
        return decorator_auth
    else:
        return decorator_auth(_func)


def auth_from_bearer_token(_func=None):
    def decorator_auth(func):
        @wraps(func)
        async def wrapper_auth(*args):
            request = args[0]
            request.state.identity = {}

            auth_header = request.headers.get("authorization", None)
            if auth_header:
                try:
                    bearer, access_token = auth_header.split()
                    if bearer != "Bearer":
                        raise ValueError()

                    model = import_string(
                        "red_warden.datazones.RWManager.RWOAuth2TokenModel"
                    )
                    token = await RWDataLayer.load_one(
                        model, filters=["access_token:eq:%s" % access_token]
                    )
                    if token:
                        request.state.identity["key_id"] = token["key_id"]
                        request.state.identity["scope"] = token["scope"]

                except ValueError:
                    pass

            _check_authorization(func, request.state.identity)
            return await func(request)

        return wrapper_auth

    if _func is None:
        return decorator_auth
    else:
        return decorator_auth(_func)
