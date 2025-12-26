"""FastAPI entrypoint for the DPP backend."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .config import get_settings
from .database import Base, engine
from .security import ensure_rls_policies
from .routers import passports, catalog, artifacts, orgs, keys, audit, jobs, cbam, dop, compliance

settings = get_settings()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Digital Product Passport API",
    description="Battery passport MVP with QR code generation and public view.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded artifacts (local storage) - replace with real storage/CDN in production.
if not settings.use_s3:
    storage_dir = Path(settings.storage_path)
    storage_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/storage", StaticFiles(directory=storage_dir), name="storage")


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    if settings.enforce_org_policies:
        ensure_rls_policies(engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> dict[str, str]:
    # Placeholder metrics endpoint; integrate real monitoring later.
    return {"metrics": "pending"}


app.include_router(passports.router)
app.include_router(catalog.router)
app.include_router(artifacts.router)
app.include_router(orgs.router)
app.include_router(keys.router)
app.include_router(audit.router)
app.include_router(jobs.router)
app.include_router(cbam.router)
app.include_router(dop.router)
app.include_router(compliance.router)
