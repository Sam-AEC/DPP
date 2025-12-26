"""Very light API key guard (header-based). Replace with real auth later."""

from __future__ import annotations

import hashlib

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from . import models
from .database import get_db


def hash_key(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def get_current_org(
    x_api_key: str | None = Header(default=None, convert_underscores=True),
    db: Session = Depends(get_db),
):
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key required")
    hashed = hash_key(x_api_key)
    record = db.query(models.ApiKey).filter(models.ApiKey.key == hashed).first()
    if not record or record.revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    org = db.get(models.Organization, record.org_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Org not found for key")
    try:
        if db.bind and db.bind.dialect.name == "postgresql":
            db.execute(text("SET LOCAL dpp.org_id = :org_id"), {"org_id": str(org.id)})
    except Exception:
        # RLS is best-effort; avoid blocking request if SET LOCAL fails.
        pass
    return org
