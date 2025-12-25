"""FastAPI entrypoint for the DPP backend."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import Base, engine
from .routers import passports, catalog, artifacts, orgs, keys, audit, jobs, cbam

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


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(passports.router)
app.include_router(catalog.router)
app.include_router(artifacts.router)
app.include_router(orgs.router)
app.include_router(keys.router)
app.include_router(audit.router)
app.include_router(jobs.router)
app.include_router(cbam.router)
