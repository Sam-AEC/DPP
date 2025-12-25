"""Restricted artifact metadata endpoints."""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import get_current_org
from ..database import get_db

router = APIRouter(prefix="/api/artifacts", tags=["artifacts"])


@router.post("", response_model=schemas.RestrictedArtifactRead, status_code=status.HTTP_201_CREATED)
def create_artifact(payload: schemas.RestrictedArtifactCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    passport = db.get(models.BatteryPassport, payload.passport_id)
    if not passport:
        raise HTTPException(status_code=404, detail="Passport not found")
    if passport.org_id and passport.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Passport not found")
    record = models.RestrictedArtifact(org_id=str(org.id), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("", response_model=List[schemas.RestrictedArtifactRead])
def list_artifacts(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.RestrictedArtifact)
        .join(models.BatteryPassport, models.RestrictedArtifact.passport_id == models.BatteryPassport.id)
        .filter(models.BatteryPassport.org_id == str(org.id))
        .order_by(models.RestrictedArtifact.created_at.desc())
        .all()
    )


@router.post("/upload-url")
def get_upload_url(filename: str, org=Depends(get_current_org)):
    # Placeholder: return a fake URL where a file could be uploaded; replace with real storage integration.
    return {"upload_url": f"https://storage.example.com/{org.id}/{filename}", "public_url": f"https://storage.example.com/{org.id}/{filename}"}


@router.get("/passport/{passport_id}", response_model=List[schemas.RestrictedArtifactRead])
def list_by_passport(passport_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    passport = db.get(models.BatteryPassport, passport_id)
    if not passport or (passport.org_id and passport.org_id != str(org.id)):
        raise HTTPException(status_code=404, detail="Passport not found")
    return (
        db.query(models.RestrictedArtifact)
        .filter(models.RestrictedArtifact.passport_id == passport_id)
        .order_by(models.RestrictedArtifact.created_at.desc())
        .all()
    )
