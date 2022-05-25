from .user import user
from .post import post
from .base import metadata, engine

metadata.create_all(bind=engine)