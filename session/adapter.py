from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from datetime import datetime, timezone, timedelta
from session.models.session_models import AccessToken
from config import LIFETIME_SECONDS


class AccessTokenDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_token(
        self, token: str, max_age: Optional[datetime] = None
    ) -> Optional[AccessToken]:
        query = select(AccessToken).where(AccessToken.token == token)
        if max_age:
            query = query.where(AccessToken.created_at >= max_age)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(
        self, access_token_dict: dict, lifetime_seconds: Optional[int] = None
    ) -> AccessToken:
        # Calculate the expiration time dynamically based on lifetime_seconds
        if lifetime_seconds:
            expires_at = datetime.now(timezone.utc) + timedelta(
                seconds=lifetime_seconds
            )
        else:
            # The default value set by fastapi_users library
            expires_at = datetime.now(timezone.utc) + timedelta(
                seconds=int(LIFETIME_SECONDS)
            )

        # Add the expiration time to the access_token_dict
        access_token_dict["expires_at"] = expires_at

        access_token = AccessToken(**access_token_dict)
        self.session.add(access_token)
        await self.session.commit()
        await self.session.refresh(access_token)
        return access_token

    async def delete(self, access_token: AccessToken) -> None:
        await self.session.delete(access_token)
        await self.session.commit()
