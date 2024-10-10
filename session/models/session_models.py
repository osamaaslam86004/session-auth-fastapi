from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta

# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select


class AccessToken(Base):
    __tablename__ = "access_tokens"

    token = Column(String, primary_key=True, index=True, unique=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    expires_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="access_tokens")


# # Session table model
# class Session(Base):
#     __tablename__ = "sessions"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     session_token = Column(String, unique=True, nullable=False)
#     user_id = Column(UUID(as_uuid=True), nullable=False)
#     expires_at = Column(DateTime, nullable=False)

#     def is_expired(self) -> bool:
#         """Check if the session is expired."""
#         return datetime.now(timezone.utc) > self.expires_at


# # Function to create session data
# async def create_session(
#     user_id: uuid.UUID, session_token: str, session: AsyncSession
# ) -> Session:
#     expires_at = datetime.now() + timedelta(hours=1)  # 1-hour session expiration

#     new_session = Session(
#         session_token=session_token, user_id=user_id, expires_at=expires_at
#     )
#     session.add(new_session)
#     await session.commit()
#     await session.refresh(new_session)  # Refresh to retrieve ID after commit
#     return new_session


# # Function to retrieve session data
# async def get_session(session_token: str, session: AsyncSession) -> Session | None:
#     result = await session.execute(
#         select(Session).filter_by(session_token=session_token)
#     )
#     session_data = result.scalar_one_or_none()
#     if session_data and not session_data.is_expired():
#         return session_data
#     return None  # Return None if the session is expired or not found


# # Function to delete session data
# async def delete_session(session_token: str, session: AsyncSession) -> bool:
#     result = await session.execute(
#         select(Session).filter_by(session_token=session_token)
#     )
#     session_data = result.scalar_one_or_none()
#     if session_data:
#         await session.delete(session_data)
#         await session.commit()
#         return True
#     return False  # Return False if no session is found
