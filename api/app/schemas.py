"""Pydantic schemas for request/response validation."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ---------- Items ----------

class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    metadata: dict[str, Any] = {}


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    metadata: dict[str, Any] | None = None


class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    metadata: dict[str, Any] = Field(validation_alias="metadata_")
    created_at: datetime
    updated_at: datetime


# ---------- Features ----------

class FeatureCreate(BaseModel):
    name: str
    enabled: bool = False
    description: str | None = None
    config: dict[str, Any] = {}


class FeatureUpdate(BaseModel):
    enabled: bool | None = None
    description: str | None = None
    config: dict[str, Any] | None = None


class FeatureOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    enabled: bool
    description: str | None
    config: dict[str, Any]
    created_at: datetime
    updated_at: datetime
