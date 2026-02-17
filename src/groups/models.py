from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, func, MetaData, Boolean

from src.auth.models import User, user

metadata = MetaData()

group = Table(
    "group",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("endpoint", String, nullable=False),
    Column("active", Boolean, default=True),
    Column("description", String, nullable=True),
    Column("user_id", Integer, ForeignKey(user.c.id)),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now())
)