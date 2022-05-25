from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
from datetime import datetime

from .base import metadata

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("email", String, unique=True),
    Column("name", String),
    Column("hashed_password", String),
    Column("is_active", Boolean, default=True),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow),
)