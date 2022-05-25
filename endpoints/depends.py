from fastapi import Depends, HTTPException, status
from core.security import JWTBearer, decode_access_token
from domains.user import User
from domains.posts import Post
from repositories.users import UserRepository
from repositories.posts import PostRepository
from db.base import database


def get_user_repository() -> UserRepository:
    return UserRepository(database)

def get_post_repository() -> PostRepository:
    return PostRepository(database)

async def get_current_user(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer())
) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await users.get_by_email(email=email)
    if user is None:
        raise cred_exception
    return user