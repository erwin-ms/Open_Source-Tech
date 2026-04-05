"""CRUD API endpoints for Feature flags / toggles."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Feature
from ..schemas import FeatureCreate, FeatureOut, FeatureUpdate

router = APIRouter(prefix="/api/features", tags=["features"])


@router.get("/", response_model=list[FeatureOut])
async def list_features(
    skip: int = 0,
    limit: int = Query(default=100, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """Return a paginated list of feature flags."""
    result = await db.execute(select(Feature).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=FeatureOut, status_code=status.HTTP_201_CREATED)
async def create_feature(payload: FeatureCreate, db: AsyncSession = Depends(get_db)):
    """Provision a new feature flag."""
    feature = Feature(
        name=payload.name,
        enabled=payload.enabled,
        description=payload.description,
        config=payload.config,
    )
    db.add(feature)
    await db.commit()
    await db.refresh(feature)
    return feature


@router.get("/{feature_id}", response_model=FeatureOut)
async def get_feature(feature_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single feature by ID."""
    result = await db.execute(select(Feature).where(Feature.id == feature_id))
    feature = result.scalar_one_or_none()
    if feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature


@router.patch("/{feature_id}", response_model=FeatureOut)
async def update_feature(
    feature_id: int,
    payload: FeatureUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a feature flag (e.g. enable/disable, change config)."""
    result = await db.execute(select(Feature).where(Feature.id == feature_id))
    feature = result.scalar_one_or_none()
    if feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(feature, key, value)

    await db.commit()
    await db.refresh(feature)
    return feature


@router.delete("/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feature(feature_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a feature flag by ID."""
    result = await db.execute(select(Feature).where(Feature.id == feature_id))
    feature = result.scalar_one_or_none()
    if feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    await db.delete(feature)
    await db.commit()
