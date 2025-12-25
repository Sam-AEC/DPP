"""Audit log endpoints (read-only, org-scoped)."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import get_current_org
from ..database import get_db

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("", response_model=List[schemas.AuditLogRead])
def list_logs(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.AuditLog)
        .filter(models.AuditLog.org_id == str(org.id))
        .order_by(models.AuditLog.created_at.desc())
        .limit(200)
        .all()
    )
