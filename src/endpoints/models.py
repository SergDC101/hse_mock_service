from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, func, MetaData

from src.groups.models import group

metadata = MetaData()

endpoint = Table(
    "endpoint",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("path", String, nullable=False),
    Column("method", String, nullable=False),
    Column("group_id", Integer, ForeignKey(group.c.id)),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now())
)