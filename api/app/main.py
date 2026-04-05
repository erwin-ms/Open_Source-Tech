"""FastAPI application entry-point."""

from fastapi import FastAPI

from .routers import features, items

app = FastAPI(
    title="Open Source Tech API",
    description=(
        "REST API for provisioning items and feature flags. "
        "Deployed via Podman."
    ),
    version="1.0.0",
)

app.include_router(items.router)
app.include_router(features.router)


@app.get("/", tags=["health"])
async def root():
    """Health-check / landing endpoint."""
    return {
        "status": "ok",
        "service": "Open Source Tech API",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health():
    """Lightweight health probe for container orchestration."""
    return {"status": "healthy"}
