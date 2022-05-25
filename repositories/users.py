from typing import List, Optional
from datetime import datetime
import sqlalchemy as sa

from core.security import hash_password
from db.user import user
from db.post import post
from domains.user import User, UserIn, UserCount
from .base import BaseRepository


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = user.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[User]:
        query = user.select().where(user.c.id == id)
        user_response = await self.database.fetch_one(query)
        if user_response is None:
            return None
        return User.parse_obj(user_response)

    async def create(self, u: UserIn) -> User:
        user_dict = User(
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        values = {**user_dict.dict()}
        values.pop("id", None)
        query = user.insert().values(**values)
        user_dict.id = await self.database.execute(query)
        return user_dict

    async def update(self, id: int, u: UserIn) -> User:
        user_dict = User(
            id=id,
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        values = {**user_dict.dict()}
        values.pop("id", None)
        values.pop("created_at", None)
        query = user.update().where(user.c.id == id).values(**values)
        user_dict.id = await self.database.execute(query)
        return user_dict

    async def get_by_email(self, email: str) -> Optional[User]:
        query = user.select().where(user.c.email == email)
        user_response = await self.database.fetch_one(query)
        if user_response is None:
            return None
        return User.parse_obj(user_response)

    async def get_post_count(self, id: int) -> UserCount:
        query = sa.select([sa.func.count(post.c.title).label('post_count')]).where(post.c.user_id == id)
        post_count_response = await self.database.fetch_one(query)
        if post_count_response is None:
            return None
        return UserCount.parse_obj(post_count_response)