# from main import app
from fastapi_users import FastAPIUsers
from user.user_manager import get_user_manager
from session.config import auth_backend
from user.models.user_models import User
import uuid
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FastAPI Users instance
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

get_current_active_user = fastapi_users.current_user(active=True)
