from sqlalchemy import select
from backend.app.data.db import get_session
from backend.app.data.db_requests.base import BaseRequests


class UserRequests(BaseRequests):

    async def get_by_email(self, email: str):
        async with get_session() as session:
            return await session.scalar(select(self.User).where(self.User.email == email))

    async def get_by_id(self, user_id: int):
        async with get_session() as session:
            return await session.scalar(select(self.User).where(self.User.id == user_id))

    async def create(self, email: str, hashed_password: str):
        async with get_session() as session:
            user = self.User(email=email, hashed_password=hashed_password)
            session.add(user)
            await session.flush()
            await session.refresh(user)
            return user


user_requests = UserRequests()
