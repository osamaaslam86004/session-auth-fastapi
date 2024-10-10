from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid


class User(SQLAlchemyBaseUserTable, Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    access_tokens = relationship(
        "AccessToken", back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4()
