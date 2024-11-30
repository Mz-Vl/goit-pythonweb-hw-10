from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas.user import UserCreate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, body: UserCreate, hashed_password: str) -> User:
        user = User(username=body.username, email=body.email, password=hashed_password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).filter_by(email=email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()