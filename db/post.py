from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime

from .base import metadata

post = Table(
    "post",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("user_id", Integer, ForeignKey('user.id'), nullable=False),
    Column("title", String),
    Column("description", String),
    Column("is_private", Boolean),
    Column("is_deleted", Boolean),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow),
)
