from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication.strategy import DatabaseStrategy
from session.adapter import AccessTokenDatabase
from database import AsyncSessionLocal
from config import LIFETIME_SECONDS

# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import Depends
# from session.session_backend import get_postgres_session_backend


# Cookie transport for session management
cookie_transport = CookieTransport(
    cookie_max_age=int(LIFETIME_SECONDS),
    cookie_name="sessionid",
    cookie_path="/",
    cookie_domain=None,
    cookie_secure=True,
    # Whether to only send the cookie to the server via SSL request.
    cookie_httponly=True,
    # Whether to prevent access to the cookie via JavaScript.
    cookie_samesite="strict",
)


# Define the authentication strategy
async def auth_strategy():
    async with AsyncSessionLocal() as session:
        access_token_db = AccessTokenDatabase(session)
        # lifetime_seconds will be used in get_by_token not in create method of adapter
        return DatabaseStrategy(
            database=access_token_db, lifetime_seconds=int(LIFETIME_SECONDS)
        )


# Create the AuthBackend that combines the transport and strategy
auth_backend = AuthenticationBackend(
    name="session cookie",
    transport=cookie_transport,
    get_strategy=auth_strategy,
)


# async def auth_strategy() -> DatabaseStrategy:
#     # Get the session backend instance using the `get_postgres_session_backend` dependency
#     session_backend = await get_postgres_session_backend()
#     return DatabaseStrategy(session_backend)
