"""Application settings."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field


class Settings(BaseModel):
    database_url: str = Field(default="sqlite:///./dev.db")
    base_public_url: str = Field(default="http://localhost:3000/scan")
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    cbam_certificate_price_per_tonne: float = Field(default=50.0)
    enforce_org_policies: bool = Field(default=False)
    storage_path: str = Field(default="storage")


@lru_cache
def get_settings() -> Settings:
    raw_origins = os.getenv("CORS_ORIGINS", "")
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return Settings(
        database_url=os.getenv("DATABASE_URL", Settings.model_fields["database_url"].default),
        base_public_url=os.getenv("BASE_PUBLIC_URL", Settings.model_fields["base_public_url"].default),
        cors_origins=origins or Settings.model_fields["cors_origins"].default_factory(),
        cbam_certificate_price_per_tonne=float(
            os.getenv(
                "CBAM_CERTIFICATE_PRICE_PER_TONNE",
                Settings.model_fields["cbam_certificate_price_per_tonne"].default,
            )
        ),
        enforce_org_policies=os.getenv("ENFORCE_ORG_POLICIES", "false").lower() == "true",
        storage_path=os.getenv("STORAGE_PATH", Settings.model_fields["storage_path"].default),
    )
