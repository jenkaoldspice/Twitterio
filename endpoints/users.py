from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from domains.user import User, UserIn
from .depends import get_user_repository, get_current_user
from repositories.users import UserRepository
router = APIRouter()

@router.get("/all")
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        skip: int = 100):
    return await users.get_all(limit=limit, skip=0)


@router.post("/sign-up", response_model=User)
async def create(user: UserIn, users: UserRepository = Depends(get_user_repository)):
    return await users.create(u=user)

@router.get("/post-count")
async def post_count(id: int,
                     users: UserRepository = Depends(get_user_repository)):
    return await users.get_post_count(id=id)

@router.put('/update')
async def update(id: int,
                 user: UserIn,
                 users: UserRepository = Depends(get_user_repository),
                 current_user: User = Depends(get_current_user)):
    old_user = await users.get_by_id(id=id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    return await users.update(id=id, u=user)
