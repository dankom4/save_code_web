import typing

import fastapi
import starlette
from pydantic import BaseModel
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException


class Token(BaseModel):
    access_token: str
    token_type: str


class OAuth2PasswordBearerWithCookieOnly(OAuth2):

    __hash__ = lambda obj: id(obj)

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        self.auto_error = auto_error
        if not scopes:
            scopes = {}
        flows = fastapi.openapi.models.OAuthFlows(
            password={"tokenUrl": tokenUrl, "scopes": scopes}
        )
        self.auto_error = auto_error
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(
        self, request: starlette.requests.Request
    ) -> typing.Optional[str]:
        cookie_authorization: str = request.cookies.get("Authorization")
        cookie_scheme, cookie_param = fastapi.security.utils.get_authorization_scheme_param(
            cookie_authorization
        )

        if cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param
        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=starlette.status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param
