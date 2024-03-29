# refer https://jordanisaacs.github.io/fastapi-sessions/guide/getting_started/
from typing import Any, Dict
from uuid import UUID, uuid4

from fastapi import HTTPException, Request, Depends
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from fastapi_sessions.session_verifier import SessionVerifier
from pydantic import BaseModel
from starlette.responses import JSONResponse

from common.app_settings import app_settings


class SessionData(BaseModel):
    username: str


cookie_params = CookieParameters()
cookie = SessionCookie(
    cookie_name=app_settings.SESSION_COOKIE_NAME,
    identifier="general_verifier",
    auto_error=True,
    secret_key=app_settings.SESSION_SECRET_KEY,
    cookie_params=cookie_params,
)
backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)


async def create_session_for_user(user_email: str):
    session = uuid4()
    data = SessionData(username=user_email)
    await backend.create(session, data)
    return session


async def delete_session_for_user(session_id: UUID):
    response = JSONResponse(content={"success": True, "msg": "You are now logged out!"})
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return response


async def get_user_email_from_request(request: Request):
    cookie(request)
    session_data = await verifier(request=request)
    return session_data
