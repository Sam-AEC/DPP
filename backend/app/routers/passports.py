"""Passport CRUD and QR endpoints."""

from __future__ import annotations

from io import BytesIO
from typing import List
from uuid import UUID

import segno
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..config import get_settings
from ..database import get_db

router = APIRouter(prefix="/api/passports", tags=["passports"])
settings = get_settings()


@router.post("", response_model=schemas.BatteryPassportRead, status_code=status.HTTP_201_CREATED)
def create_passport(
    passport: schemas.BatteryPassportCreate,
    db: Session = Depends(get_db),
):
    record = models.BatteryPassport(**passport.model_dump())
    db.add(record)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Serial number must be unique") from exc
    db.refresh(record)
    return record


@router.get("", response_model=List[schemas.BatteryPassportRead])
def list_passports(db: Session = Depends(get_db)):
    return db.query(models.BatteryPassport).order_by(models.BatteryPassport.created_at.desc()).all()


@router.get("/{passport_id}", response_model=schemas.BatteryPassportRead)
def get_passport(passport_id: UUID, db: Session = Depends(get_db)):
    record = db.get(models.BatteryPassport, passport_id)
    if not record:
        raise HTTPException(status_code=404, detail="Passport not found")
    return record


@router.patch("/{passport_id}", response_model=schemas.BatteryPassportRead)
def update_passport(
    passport_id: UUID,
    updates: schemas.BatteryPassportUpdate,
    db: Session = Depends(get_db),
):
    record = db.get(models.BatteryPassport, passport_id)
    if not record:
        raise HTTPException(status_code=404, detail="Passport not found")
    for key, value in updates.model_dump(exclude_none=True).items():
        setattr(record, key, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Serial number must be unique") from exc
    db.refresh(record)
    return record


@router.get("/{passport_id}/public", response_model=schemas.BatteryPassportPublic)
def get_public(passport_id: UUID, db: Session = Depends(get_db)):
    record = db.get(models.BatteryPassport, passport_id)
    if not record:
        raise HTTPException(status_code=404, detail="Passport not found")
    return record


@router.get(
    "/{passport_id}/qr",
    responses={200: {"content": {"image/png": {}}}},
    response_class=StreamingResponse,
)
def get_qr(passport_id: UUID):
    target_url = f"{settings.base_public_url}/{passport_id}"
    qr = segno.make(target_url, micro=False)
    buffer = BytesIO()
    qr.save(buffer, kind="png", scale=6)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")
