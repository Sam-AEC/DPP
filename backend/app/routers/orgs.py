"""Organization and user management (lightweight, no auth provider attached yet)."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/orgs", tags=["orgs"])


@router.post("", response_model=schemas.OrgRead, status_code=status.HTTP_201_CREATED)
def create_org(payload: schemas.OrgCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Organization).filter(models.Organization.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")
    record = models.Organization(name=payload.name)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("", response_model=List[schemas.OrgRead])
def list_orgs(db: Session = Depends(get_db)):
    return db.query(models.Organization).order_by(models.Organization.created_at.desc()).all()


@router.post("/{org_id}/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(org_id: str, payload: schemas.UserCreate, db: Session = Depends(get_db)):
    org = db.get(models.Organization, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    record = models.User(email=payload.email, role=payload.role, org_id=org.id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{org_id}/users", response_model=List[schemas.UserRead])
def list_users(org_id: str, db: Session = Depends(get_db)):
    org = db.get(models.Organization, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return (
        db.query(models.User)
        .filter(models.User.org_id == org.id)
        .order_by(models.User.created_at.desc())
        .all()
    )
