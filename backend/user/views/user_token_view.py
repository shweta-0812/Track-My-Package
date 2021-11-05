# refer https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
# refer https://jordanisaacs.github.io/fastapi-sessions/

from enum import Enum
from typing import Union

from fastapi import APIRouter, Request
from fastapi_sessions.frontends.implementations import cookie
from fastapi.responses import JSONResponse, RedirectResponse

from common.app_settings import app_settings
from services import auth_session_service
from services.auth_session_service import SessionData, cookie, backend, verifier

router: APIRouter = APIRouter()

from google.oauth2 import id_token
from google.auth.transport import requests

from fastapi import Response, Depends
from uuid import UUID, uuid4

# For DEV only APIs
# @router.post("/create_session/{name}")
# async def create_session(name: str, response: Response):
#     session = uuid4()
#     data = SessionData(username=name)
#     await backend.create(session, data)
#     cookie.attach_to_response(response, session)
#     return f"created session for {name}"
#
#
# @router.get("/whoami", dependencies=[Depends(cookie)])
# async def whoami(session_data: SessionData = Depends(verifier)):
#     return session_data
#
#
# @router.post("/delete_session")
# async def del_session(response: Response, session_id: UUID = Depends(cookie)):
#     await backend.delete(session_id)
#     cookie.delete_from_response(response)
#     return "deleted session"



@router.post("/google-login-test")
async def test_google_login(request: Request):
    req = await request.json()
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        id_info = id_token.verify_oauth2_token(
            req["id_token"],
            requests.Request(),
            app_settings.GOOGLE_API_CLIENT_ID,
        )

        # ID token is valid. Get the user's Google Account ID from the decoded token. and create user if not exists
        user_email = id_info["email"]
        # create a session and redirect with the cookie
        response: Union[RedirectResponse, JSONResponse]
        response = RedirectResponse(url="/")
        # #starlette response by default have code 307, which preserves the method during the redirection, hence the post request. I solved this by adding response.status_code = 302 before returning the response.
        response.status_code = 302

        session_key = await auth_session_service.create_session_key_from_user_email(user_email=user_email)
        cookie.attach_to_response(response, session_key)

        # response.set_cookie(
        #     key="fakeshwetasession",
        #     value="fake-cookie-session-value",
        #     max_age=60 * 60 * 24,
        #     domain="localhost:8080",
        #     path="/",
        #     httponly=True,
        #     samesite=None,
        #     secure=True,
        # )

        # if redirect_url:
        #     response = RedirectResponse(redirect_url)
        # else:
        #     response = JSONResponse(
        #         content={"success": True, "msg": "You are now logged in!"})
        return response
    except ValueError:
        # Invalid token
        pass
