from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from session.models.session_models import create_session, get_session, delete_session
from database import AsyncSessionLocal


# Custom PostgreSQL backend for session management
class PostgresSessionBackend:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: uuid.UUID) -> str:
        # Ensure user_id is an integer
        print(f"############################### {user_id}")

        if user_id is None:
            raise ValueError("user_id cannot be None")
        else:
            user_id = user_id.get("user_id")
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {user_id}")
        # Generate a session token (can be a JWT, UUID, or any unique identifier)
        session_token = (
            generate_session_token()
        )  # You can use a function to generate this
        await create_session(user_id, session_token, self.session)
        return {"token": session_token}

    async def validate(self, session_token: str) -> Optional[uuid.UUID]:
        # Retrieve session data and check if it's valid (e.g., not expired)
        session_data = await get_session(session_token, self.session)
        if session_data and not session_data.is_expired():
            return session_data.user_id
        return None

    async def delete(self, session_token: str):
        await delete_session(session_token, self.session)


async def get_postgres_session_backend() -> PostgresSessionBackend:
    async with AsyncSessionLocal() as session:
        return PostgresSessionBackend(session)


def generate_session_token() -> str:
    return str(uuid.uuid4())
