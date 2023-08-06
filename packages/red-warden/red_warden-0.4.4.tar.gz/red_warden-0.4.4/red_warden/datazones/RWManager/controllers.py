import json
from typing import Optional
from aioauth.types import RequestMethod
from aioauth.requests import (
    Query,
    Post,
    Request as OAuth2Request,
)
from aioauth.config import Settings
from aioauth.collections import HTTPHeaderDict
from starlette.routing import Mount
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from red_warden.config import RWConfig
from red_warden.datalayer import RWDataLayer
from red_warden.helpers import import_string
from red_warden.mvc import (
    RWValidationModelBase,
    RWRestController,
    RWController,
)
from red_warden.oauth2 import RWOAuth2Server
from red_warden.routing import RWApiRoute, RWRoute
from .models import (
    RWBackendModel,
    RWTenantModel,
    RWKeyModel,
    RWSessionModel,
    RWOAuth2ClientModel,
    RWOAuth2AuthorizationCodeModel,
    RWOAuth2TokenModel,
    RWAclRoleModel,
    RWAclPermissionModel,
    RWAclRolePermissionLinkModel,
    RWAclRoleKeyLinkModel,
)
from .logic import RWSessionLogic


class RWBackendController(RWRestController):
    model = RWBackendModel

    @classmethod
    def get_routes(cls):
        return [
            Mount(
                "/backends",
                routes=[
                    RWApiRoute("/", cls.load_all, ["manager"]),
                    RWApiRoute("/{id}", cls.load_by_id, ["manager"]),
                    RWApiRoute("/", cls.create, ["manager"], methods=["POST"]),
                    RWApiRoute("/{id}", cls.update, ["manager"], methods=["PUT"]),
                    RWApiRoute("/{id}", cls.delete, ["manager"], methods=["DELETE"]),
                    RWApiRoute(
                        "/upgrade-schemas",
                        cls.upgrade_schemas,
                        [],
                        methods=["POST"],
                    ),
                ],
            )
        ]

    @classmethod
    async def upgrade_schemas(cls, request):
        class ValidationModel(RWValidationModelBase):
            tenant_id: Optional[str]

        data = await request.form()
        data = ValidationModel(**data).dict()
        return {
            "data": await RWDataLayer.upgrade_other_datapaths_migrations(
                tenant_id=data.get("tenant_id", None)
            )
        }

    @classmethod
    async def create(cls, request):
        results = await super().create(request)
        await RWDataLayer.reload_backends()
        return results

    @classmethod
    async def update(cls, request):
        results = await super().update(request)
        await RWDataLayer.reload_backends()
        return results

    @classmethod
    async def delete(cls, request):
        results = await super().delete(request)
        await RWDataLayer.reload_backends()
        return results


class RWTenantController(RWRestController):
    model = RWTenantModel

    @classmethod
    def get_routes(cls):
        return [
            Mount(
                "/tenants",
                routes=[
                    RWApiRoute("/", cls.load_all, ["manager"]),
                    RWApiRoute("/{id}", cls.load_by_id, ["manager"]),
                    RWApiRoute("/", cls.create, ["manager"], methods=["POST"]),
                    RWApiRoute("/{id}", cls.update, ["manager"], methods=["PUT"]),
                    RWApiRoute("/{id}", cls.delete, ["manager"], methods=["DELETE"]),
                ],
            )
        ]


class RWKeyController(RWRestController):
    model = RWKeyModel

    @classmethod
    def get_routes(cls):
        return [
            Mount(
                "/keys",
                routes=[
                    RWApiRoute("/", cls.load_all, ["manager"]),
                    RWApiRoute("/{id}", cls.load_by_id, ["manager"]),
                    RWApiRoute("/", cls.create, ["manager"], methods=["POST"]),
                    RWApiRoute("/{id}", cls.update, ["manager"], methods=["PUT"]),
                    RWApiRoute("/{id}", cls.delete, ["manager"], methods=["DELETE"]),
                    RWApiRoute(
                        "/authenticate",
                        cls.authenticate,
                        ["manager"],
                        methods=["POST"],
                    ),
                    RWApiRoute(
                        "/{id}/mfa",
                        cls.toggle_mfa,
                        ["manager"],
                        methods=["POST"],
                    ),
                    RWApiRoute(
                        "/{id}/otp",
                        cls.check_otp,
                        ["manager"],
                        methods=["POST"],
                    ),
                ],
            )
        ]

    @classmethod
    async def check_otp(cls, request):
        data = await request.form()
        data["key_id"] = request.path_params.get("id", None)
        result = RWSessionLogic.check_otp(**data)

        if result is None:
            raise HTTPException(HTTP_404_NOT_FOUND)
        else:
            return result

    @classmethod
    async def toggle_mfa(cls, request):
        data = await request.form()
        data["key_id"] = request.path_params.get("id", None)
        result = RWSessionLogic.toggle_mfa(**data)

        if result is None:
            raise HTTPException(HTTP_404_NOT_FOUND)
        else:
            return result

    @classmethod
    async def authenticate(cls, request):
        """
        Used to re-check the password for an already logged in user.
        This is not the "login" method, as this is an API that should be asked
        before dangerous operations are made in frontend.

        This is not the "login" method also because it's not asking for MFA.
        """
        result = await RWSessionLogic.authenticate(**await request.form())

        if result is None:
            raise HTTPException(HTTP_404_NOT_FOUND)
        elif not result:
            raise HTTPException(HTTP_401_UNAUTHORIZED)
        else:
            return result


class RWSessionController(RWRestController):
    model = RWSessionModel

    @classmethod
    def get_routes(cls):
        return [
            Mount(
                "/sessions",
                routes=[
                    RWApiRoute("/", cls.load_all, ["manager"]),
                    RWApiRoute("/{id}", cls.load_by_id, ["manager"]),
                    RWApiRoute("/", cls.create, ["manager"], methods=["POST"]),
                    RWApiRoute("/{id}", cls.update, ["manager"], methods=["PUT"]),
                    RWApiRoute("/{id}", cls.delete, ["manager"], methods=["DELETE"]),
                ],
            )
        ]


class RWOAuth2ClientController(RWRestController):
    model = RWOAuth2ClientModel

    @classmethod
    def get_routes(cls):
        return [
            Mount(
                "/oauth2-clients",
                routes=[
                    RWApiRoute("/", cls.load_all, ["manager"]),
                    RWApiRoute("/{id}", cls.load_by_id, ["manager"]),
                    RWApiRoute("/", cls.create, ["manager"], methods=["POST"]),
                    RWApiRoute("/{id}", cls.update, ["manager"], methods=["PUT"]),
                    RWApiRoute("/{id}", cls.delete, ["manager"], methods=["DELETE"]),
                ],
            )
        ]


class RWOAuth2AuthorizationCodeController(RWRestController):
    model = RWOAuth2AuthorizationCodeModel

    @classmethod
    def get_routes(cls):
        return [
            Mount(
                "/oauth2-authorization-codes",
                routes=[
                    RWApiRoute("/", cls.load_all, ["manager"]),
                    RWApiRoute("/{id}", cls.load_by_id, ["manager"]),
                    RWApiRoute("/", cls.create, ["manager"], methods=["POST"]),
                    RWApiRoute("/{id}", cls.update, ["manager"], methods=["PUT"]),
                    RWApiRoute("/{id}", cls.delete, ["manager"], methods=["DELETE"]),
                ],
            )
        ]


class RWOAuth2TokenController(RWRestController):
    model = RWOAuth2TokenModel

    @classmethod
    def get_routes(cls):
        return [
            Mount(
                "/oauth2-tokens",
                routes=[
                    RWApiRoute("/", cls.load_all, ["manager"]),
                    RWApiRoute("/{id}", cls.load_by_id, ["manager"]),
                    RWApiRoute("/", cls.create, ["manager"], methods=["POST"]),
                    RWApiRoute("/{id}", cls.update, ["manager"], methods=["PUT"]),
                    RWApiRoute("/{id}", cls.delete, ["manager"], methods=["DELETE"]),
                ],
            )
        ]


class RWOAuth2FlowController(RWController):
    settings = Settings(INSECURE_TRANSPORT=RWConfig["RW_ENV"] == "local")

    @classmethod
    def get_routes(cls):
        return [
            RWRoute("/oauth2/authorize", cls.authorize, scope=["logged_in"]),
            RWRoute("/oauth2/token", cls.token, methods=["POST"]),
        ]

    @classmethod
    async def authorize(cls, request):
        """
        Endpoint to interact with the resource owner and obtain an authorization grant.

        See Section 4.1.1: https://tools.ietf.org/html/rfc6749#section-4.1.1
        """
        return await cls._to_starlette_response(
            await RWOAuth2Server.create_authorization_response(
                await cls._to_oauth2_request(request)
            )
        )

    @classmethod
    async def token(cls, request):
        """
        Endpoint to obtain an access and/or ID token by presenting an authorization grant or refresh token.

        See Section 4.1.3: https://tools.ietf.org/html/rfc6749#section-4.1.3
        """
        oauth2_request = await cls._to_oauth2_request(request)
        oauth2_response = await RWOAuth2Server.create_token_response(oauth2_request)
        return await cls._to_starlette_response(oauth2_response)

    @classmethod
    async def _to_oauth2_request(cls, request):
        """Converts Starlette Request instance to OAuth2Request instance"""
        form = await request.form()

        post = dict(form)
        query_params = dict(request.query_params)
        method = request.method
        headers = HTTPHeaderDict(**request.headers)
        url = str(request.url)
        return OAuth2Request(
            settings=cls.settings,
            method=RequestMethod[method],
            headers=headers,
            post=Post(**post),
            query=Query(**query_params),
            url=url,
            user=request.state.identity.get("key_id", None),
        )

    @staticmethod
    async def _to_starlette_response(oauth2_response):
        """Converts OAuth2Response instance to Starlette Response instance"""
        response_content = (
            oauth2_response.content if oauth2_response.content is not None else {}
        )
        headers = dict(oauth2_response.headers)
        status_code = oauth2_response.status_code
        content = json.dumps(response_content)

        return Response(content=content, headers=headers, status_code=status_code)


class RWAclRoleController(RWRestController):
    model = RWAclRoleModel
    role_permission_link_model = import_string(
        "red_warden.datazones.RWManager.RWAclRolePermissionLinkModel"
    )
    # TODO role_key_link_model = import_string("red_warden.datazones.RWManager.RWAclRoleKeyLinkModel")

    @classmethod
    def get_routes(cls):
        return [
            Mount(
                "/acl-roles",
                routes=[
                    RWApiRoute("/", cls.load_all, ["manager"]),
                    RWApiRoute("/{id}", cls.load_by_id, ["manager"]),
                    RWApiRoute("/", cls.create, ["manager"], methods=["POST"]),
                    RWApiRoute("/{id}", cls.update, ["manager"], methods=["PUT"]),
                    RWApiRoute("/{id}", cls.delete, ["manager"], methods=["DELETE"]),
                    RWApiRoute(
                        "/{id}/permissions", cls.load_role_permissions, ["manager"]
                    ),
                    RWApiRoute(
                        "/{id}/permissions/{permission_id}",
                        cls.create_role_permission,
                        ["manager"],
                        methods=["POST"],
                    ),
                    RWApiRoute(
                        "/{id}/permissions/{permission_id}",
                        cls.delete_role_permission,
                        ["manager"],
                        methods=["DELETE"],
                    ),
                ],
            )
        ]

    @classmethod
    async def load_role_permissions(cls, request):
        model_id = request.path_params.get("id", None)

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
        filters.append("acl_role_id:eq:%s" % model_id)

        data, pagination = await RWDataLayer.load_all(
            cls.role_permission_link_model,
            request.state.identity,
            pagination,
            sort,
            filters,
        )

        results = {"data": data}
        if pagination:
            results["pagination"] = pagination

        return results

    @classmethod
    async def _load_role_permission(cls, request, acl_role_id, acl_permission_id):
        return await RWDataLayer.load_one(
            cls.role_permission_link_model,
            request.state.identity,
            filters=[
                "acl_role_id:eq:%s" % acl_role_id,
                "acl_permission_id:eq:%s" % acl_permission_id,
            ],
        )

    @classmethod
    async def create_role_permission(cls, request):
        acl_role_id = request.path_params.get("id", None)
        acl_permission_id = request.path_params.get("permission_id", None)

        role_permission = await cls._load_role_permission(
            request, acl_role_id, acl_permission_id
        )
        if role_permission:
            await RWDataLayer.remove(
                cls.role_permission_link_model,
                role_permission["id"],
                request.state.identity,
            )

        body = {
            "acl_role_id": acl_role_id,
            "acl_permission_id": acl_permission_id,
        }
        return {
            "data": await RWDataLayer.save(
                cls.role_permission_link_model, None, body, request.state.identity
            )
        }

    @classmethod
    async def delete_role_permission(cls, request):
        acl_role_id = request.path_params.get("id", None)
        acl_permission_id = request.path_params.get("permission_id", None)

        role_permission = await cls._load_role_permission(
            request, acl_role_id, acl_permission_id
        )
        if role_permission:
            data = await RWDataLayer.remove(
                cls.role_permission_link_model,
                role_permission["id"],
                request.state.identity,
            )
            return {"data": data}


class RWAclPermissionController(RWRestController):
    model = RWAclPermissionModel

    @classmethod
    def get_routes(cls):
        return [
            Mount(
                "/acl-permissions",
                routes=[
                    RWApiRoute("/", cls.load_all, ["manager"]),
                    RWApiRoute("/{id}", cls.load_by_id, ["manager"]),
                    RWApiRoute("/", cls.create, ["manager"], methods=["POST"]),
                    RWApiRoute("/{id}", cls.update, ["manager"], methods=["PUT"]),
                    RWApiRoute("/{id}", cls.delete, ["manager"], methods=["DELETE"]),
                ],
            )
        ]
