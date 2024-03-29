from sqlalchemy import Column, ForeignKey, Table

from app.db.base_class import Base


tag_assign = Table(
    "tag_assign",
    Base.metadata,
    Column("snippet_id", ForeignKey("snippet.id")),
    Column("tag_id", ForeignKey("tag.id")),
)
