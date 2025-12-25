"""API key issuance and listing (simple, no hashing for brevity)."""

from __future__ import annotations

import secrets
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import hash_key
from ..database import get_db

router = APIRouter(prefix="/api/keys", tags=["api-keys"])


def generate_key() -> str:
    return secrets.token_urlsafe(32)


@router.post("", response_model=schemas.ApiKeyRead, status_code=status.HTTP_201_CREATED)
def create_key(payload: schemas.ApiKeyCreate, db: Session = Depends(get_db)):
    org = db.get(models.Organization, payload.org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    key_value = generate_key()
    record = models.ApiKey(
        org_id=payload.org_id,
        name=payload.name,
        key=hash_key(key_value),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    # Return the raw key once; it is not stored in plaintext.
    return schemas.ApiKeyRead(
        id=record.id,
        org_id=record.org_id,
        name=record.name,
        key=key_value,
        created_at=record.created_at,
        revoked=record.revoked,
    )


@router.get("", response_model=List[schemas.ApiKeyRead])
def list_keys(org_id: UUID | None = None, db: Session = Depends(get_db)):
    query = db.query(models.ApiKey).order_by(models.ApiKey.created_at.desc())
    if org_id:
        query = query.filter(models.ApiKey.org_id == org_id)
    return query.all()


@router.post("/{key_id}/revoke", response_model=schemas.ApiKeyRead)
def revoke_key(key_id: UUID, db: Session = Depends(get_db)):
    record = db.get(models.ApiKey, key_id)
    if not record:
        raise HTTPException(status_code=404, detail="API key not found")
    record.revoked = record.revoked or record.created_at
    db.commit()
    db.refresh(record)
    return record
