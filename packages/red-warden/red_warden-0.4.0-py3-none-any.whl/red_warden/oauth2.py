import json
from datetime import datetime
from time import time
from typing import Optional
from aioauth.server import AuthorizationServer
from aioauth.storage import BaseStorage
from aioauth.models import Token, AuthorizationCode, Client
from cryptography.fernet import Fernet
from red_warden.config import RWConfig
from red_warden.enums import RWYesNoEnum
from red_warden.helpers import import_string
from red_warden.datalayer import RWDataLayer
from red_warden.datazones.RWManager.logic import RWSessionLogic


class _Storage(BaseStorage):
    def __init__(self):
        self.fernet = Fernet(str(RWConfig["RW_DATABASE_SECRET"]))

    async def get_client(
        self, request, client_id: str, client_secret: Optional[str] = None
    ) -> Optional[Client]:
        """Get client record from the database by provided request from user.

        Returns:
            `Client` instance if client exists in db.
            `None` if no client in db.
        """
        model = import_string("red_warden.datazones.RWManager.RWOAuth2ClientModel")
        client = await RWDataLayer.load_one(model, filters=["name:eq:%s" % client_id])
        if not client:
            return None

        if client_secret:
            # TODO verify the client secret!!
            pass

        return Client(
            client_id=client["id"],
            client_secret=client["secret"],
            grant_types=client["grant_types"].split(","),
            response_types=client["response_types"].split(","),
            redirect_uris=client["redirect_uris"] or [],
            scope=client["scope"] or "",
        )

    async def create_authorization_code(
        self,
        request,
        client_id: str,
        scope: str,
        response_type: str,
        redirect_uri: str,
        code_challenge_method: Optional[str],
        code_challenge: Optional[str],
    ) -> AuthorizationCode:
        """Generates an authorization token and stores it in the database.
        Warning:
            Generated authorization token *must* be stored in the database.
        Note:
            This must is used by the response type
            :py:class:`aioauth.respose_type.ResponseTypeAuthorizationCode`.
        Args:
            request: An :py:class:`aioauth.requests.Request`.
            client_id: A user client ID.
            scope: The scopes for the token.
            response_type: An :py:class:`aioauth.types.ResponseType`.
            redirect_uri: The redirect URI.
            code_challenge_method: An :py:class:`aioauth.types.CodeChallengeMethod`.
            code_challenge: Code challenge string.
        Returns:
            An :py:class:`aioauth.models.AuthorizationCode` object.
        """

        # generate an authorization token
        code = self.fernet.encrypt(
            json.dumps({"key_id": request.user, "scope": scope}).encode()
        ).decode("utf-8")

        authorization_code = AuthorizationCode(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri,
            response_type=response_type,
            scope=scope,
            auth_time=int(time()),
            code_challenge_method=code_challenge_method,
            code_challenge=code_challenge,
            expires_in=request.settings.AUTHORIZATION_CODE_EXPIRES_IN,
        )

        # saves the Authorization Code to the db
        model = import_string(
            "red_warden.datazones.RWManager.RWOAuth2AuthorizationCodeModel"
        )
        await RWDataLayer.save(
            model,
            None,
            {
                "code": authorization_code.code,
                "oauth2_client_id": authorization_code.client_id,
                "key_id": request.user,
                "redirect_uri": authorization_code.redirect_uri,
                "response_type": authorization_code.response_type,
                "scope": authorization_code.scope,
                "auth_time": datetime.utcfromtimestamp(authorization_code.auth_time),
                "expires_in": authorization_code.expires_in,
                "nonce": authorization_code.nonce,
                "code_challenge": authorization_code.code_challenge,
                "code_challenge_method": authorization_code.code_challenge_method,
            },
        )
        return authorization_code

    @staticmethod
    async def _get_authorization_code_from_db(client_id, code):
        model = import_string(
            "red_warden.datazones.RWManager.RWOAuth2AuthorizationCodeModel"
        )
        auth_code = await RWDataLayer.load_one(
            model, filters=["code:eq:%s" % code, "oauth2_client_id:eq:%s" % client_id]
        )
        if not auth_code:
            return None

        return auth_code

    async def get_authorization_code(
        self, request, client_id: str, code: str
    ) -> Optional[AuthorizationCode]:

        auth_code = await self._get_authorization_code_from_db(client_id, code)
        if not auth_code:
            return None

        return AuthorizationCode(
            code=auth_code["code"],
            client_id=auth_code["oauth2_client_id"],
            redirect_uri=auth_code["redirect_uri"],
            response_type=auth_code["response_type"],
            scope=auth_code["scope"],
            auth_time=auth_code["auth_time"].timestamp(),
            expires_in=auth_code["expires_in"],
            code_challenge=auth_code["code_challenge"],
            code_challenge_method=auth_code["code_challenge_method"],
            nonce=auth_code["nonce"],
        )

    async def delete_authorization_code(
        self, request, client_id: str, code: str
    ) -> None:
        auth_code = await self._get_authorization_code_from_db(client_id, code)
        if auth_code:
            model = import_string(
                "red_warden.datazones.RWManager.RWOAuth2AuthorizationCodeModel"
            )
            await RWDataLayer.remove(model, auth_code["id"])

    async def create_token(self, request, client_id: str, scope: str) -> Token:
        token = await super().create_token(request, client_id, scope)
        print("scope", scope)

        # saves the Token to the db
        if request.post.code:
            data = self.fernet.decrypt(request.post.code.encode("utf-8")).decode(
                "utf-8"
            )
            data = json.loads(data)
            key_id = data["key_id"]
            # scope = data["scope"]
        else:
            model = import_string("red_warden.datazones.RWManager.RWKeyModel")
            key = await RWDataLayer.load_one(
                model, filters=["login:eq:%s" % request.post.username]
            )
            key_id = key["id"]
            # scope = scope

        model = import_string("red_warden.datazones.RWManager.RWOAuth2TokenModel")
        await RWDataLayer.save(
            model,
            None,
            {
                "access_token": token.access_token,
                "refresh_token": token.refresh_token,
                "scope": token.scope,
                "issued_at": datetime.utcfromtimestamp(token.issued_at),
                "access_token_expires_in": token.expires_in,
                "refresh_token_expires_in": token.refresh_token_expires_in,
                "oauth2_client_id": token.client_id,
                "key_id": key_id,
                "token_type": token.token_type,
                "revoked": RWYesNoEnum.YES if token.revoked else RWYesNoEnum.NO,
            },
        )

        return token

    async def get_token(
        self,
        request,
        client_id: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
    ) -> Optional[Token]:
        model = import_string("red_warden.datazones.RWManager.RWOAuth2TokenModel")

        filters = ["oauth2_client_id:eq:%s" % client_id]
        if access_token:
            filters.append("access_token:eq:%s" % access_token)
        elif refresh_token:
            filters.append("refresh_token:eq:%s" % refresh_token)
        else:
            raise Exception("Please specify an access token or a refresh token")

        token = await RWDataLayer.load_one(model, filters=filters)
        if not token:
            return None

        return Token(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            scope=token["scope"],
            issued_at=token["issued_at"].timestamp(),
            expires_in=token["access_token_expires_in"],
            refresh_token_expires_in=token["refresh_token_expires_in"],
            client_id=token["oauth2_client_id"],
            token_type=token["token_type"],
            revoked=True if token["revoked"] == RWYesNoEnum.YES else False,
            user=token["key_id"],
        )

    async def revoke_token(self, request, token):
        """Revokes an existing token. The `revoked`

        Flag of the Token must be set to True
        """
        token_record = ...
        token_record.revoked = True
        token_record.save()

    async def authenticate(self, request) -> bool:
        if await RWSessionLogic.authenticate(
            username=request.post.username, password=request.post.password
        ):
            return True


RWOAuth2Server = AuthorizationServer(storage=_Storage())


#
# class Flow:
#
#     @classmethod
#
#
#     @staticmethod
#     async def introspect(request):
#         """Endpoint returns information about a token.
#
#         See Section 2.1: https://tools.ietf.org/html/rfc7662#section-2.1
#         """
#         # oauth2_request: OAuth2Request = await to_oauth2_request(request)
#         # oauth2_response: OAuth2Response = await server.create_token_introspection_response(
#         #     oauth2_request
#         # )
#         #
#         # return await to_fastapi_response(oauth2_response)
#         pass
