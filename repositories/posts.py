from typing import List
from db.user import user
from domains.posts import PostIn, Post
from db.post import post
from domains.user import UserCount
from .base import BaseRepository
from datetime import datetime


class PostRepository(BaseRepository):

    async def create(self, user_id: int, p: PostIn) -> Post:
        post_dict = Post(
            id=0,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            title=p.title,
            description=p.description,
            is_private=p.is_private,
        )
        values = {**post_dict.dict()}
        values.pop("id", None)
        query = post.insert().values(**values)
        post_dict.id = await self.database.execute(query=query)
        return post_dict

    async def update(self, id: int, user_id: int, p: PostIn) -> Post:
        post_dict = Post(
            id=id,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            title=p.title,
            description=p.description,
            is_private=p.is_private,
        )
        values = {**post_dict.dict()}
        values.pop("id", None)
        values.pop("created_at", None)
        query = post.update().where(post.c.id == id).values(**values)
        await self.database.execute(query=query)
        return post_dict

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Post]:
        query = post.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def delete(self, id: int):
        query = post.delete().where(post.c.id == id)
        return await self.database.execute(query=query)

    async def get_by_id(self, id: int) -> Post:
        query = post.select().where(post.c.id == id)
        post_response = await self.database.fetch_one(query=query)
        return Post.parse_obj(post_response)

