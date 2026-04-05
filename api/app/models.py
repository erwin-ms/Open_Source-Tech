"""SQLAlchemy ORM models."""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    metadata_ = Column("metadata", JSONB, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    enabled = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    config = Column(JSONB, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
