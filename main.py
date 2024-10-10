from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import AsyncSessionLocal, engine
from sqlalchemy import text
from contextlib import asynccontextmanager
from fastapi_utils.tasks import repeat_every
from user.routers.user_routes import router as custom_user_routers
from fastapi_auth.auth import fastapi_users
from user.schemas.user_schemas import UserCreate, UserDB
from session.config import auth_backend
from repeated_task import cleanup_expired_tokens
from config import LIFETIME_SECONDS, DATABASE_PING
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


CORS_ALLOWED_ORIGINS = [
    "https://music-player-ui-ux.vercel.app",
    "http://127.0.0.1:60640",
    "https://osama11111.pythonanywhere.com",
    "https://osamaaslam.pythonanywhere.com",
    "https://web.postman.co",
    "https://diverse-intense-whippet.ngrok-free.app",
    "http://127.0.0.1:5500",
    "https://resume-builder-integrated-with-resume-api.vercel.app",
    "https://resume-builder-pwa.vercel.app/",
]


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    # expose_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup task: keep database connection alive
    logger.info("Starting up and initiating keep-alive task.")

    # Define the keep-alive task
    @repeat_every(seconds=int(DATABASE_PING))  # Runs every 5 seconds
    async def keep_db_alive():
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(text("SELECT 1"))
                logger.info("Keep-alive query executed successfully.")
        except Exception as e:
            logger.error(f"Error executing keep-alive query: {e}")

    @repeat_every(seconds=int(LIFETIME_SECONDS))
    async def scheduled_cleanup():
        logger.info("Running scheduled token cleanup.")
        async with AsyncSessionLocal() as session:
            await cleanup_expired_tokens(session)

    # Startup tasks before yielding control to the app
    await keep_db_alive()

    # Cleanup expire AccessTokens
    await scheduled_cleanup()

    yield

    # Shutdown tasks (if any)
    logger.info("Shutting down.")
    await engine.dispose()
    # Cleanup tasks go here if necessary


# Set lifespan context in the FastAPI app
app = FastAPI(lifespan=lifespan)


@app.get("/methods", tags=["debug"])
async def get_routes():
    return [
        {"path": route.path, "name": route.name, "methods": list(route.methods)}
        for route in app.routes
    ]


@app.get("/routes", tags=["debug"])
async def get_routes():
    return [
        {
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods),
            # Safely get dependencies if they exist, otherwise default to None
            "dependencies": getattr(route, "dependencies", None),
        }
        for route in app.routes
    ]


# Routes for authentication
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)


# Routes for registration
app.include_router(
    fastapi_users.get_register_router(UserDB, UserCreate),  # Provide the schemas
    prefix="/auth",
    tags=["auth"],
)


# Routes for user management
app.include_router(
    fastapi_users.get_users_router(UserDB, UserCreate),
    prefix="/users",
    tags=["users"],
)


# Include your custom user routes
app.include_router(
    custom_user_routers,
    prefix="/acount",  # Use the same prefix to keep it organized
    tags=["account"],
)

# Set the custom OpenAPI schema
# from openapi_schema import custom_openapi

# app.openapi = custom_openapi


# Protected route example
# @app.get("/protected-route", dependencies=[Depends(fastapi_users.current_user)])
# async def protected_route():
#     return {"message": "You are authenticated!"}


@app.get("/")
async def read_root():
    return {"Hello": "World"}
