import uvicorn
from fastapi import FastAPI

from db.base import database
from endpoints import users, auth, posts

app = FastAPI(title="Twitterio")

app.include_router(users.router, prefix="/user", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/post", tags=["posts"])


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.on_event('startup')
async def startup():
    await database.connect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
