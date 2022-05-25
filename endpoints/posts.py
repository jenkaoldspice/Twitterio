from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from domains.posts import Post, PostIn
from domains.user import User
from .depends import get_post_repository, get_current_user
from repositories.posts import PostRepository

router = APIRouter()


@router.get("/all", response_model=List[Post])
async def read_posts(
        posts: PostRepository = Depends(get_post_repository),
        limit: int = 100,
        skip: int = 100):
    return await posts.get_all(limit=limit, skip=0)


@router.post("/create")
async def create(
        p: PostIn,
        posts: PostRepository = Depends(get_post_repository),
        current_user: User = Depends(get_current_user)) -> Post:
    return await posts.create(user_id=current_user.id, p=p)


@router.put("/update", response_model=Post)
async def update(
        id: int,
        p: PostIn,
        posts: PostRepository = Depends(get_post_repository),
        current_user: User = Depends(get_current_user)) -> Post:
    old_post = await posts.get_by_id(id=id)
    if old_post is None or old_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return await posts.update(id=id, user_id=current_user.id, p=p)


@router.delete("/delete")
async def delete(
        id: int,
        posts: PostRepository = Depends(get_post_repository),
        current_user: User = Depends(get_current_user)) -> Post:
    nf_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post = await posts.get_by_id(id=id)
    if post is None or post.user_id != current_user.id:
        raise nf_exception
    result = await posts.delete(id=id)
    if result is None:
        raise nf_exception
    return {"status": True}
