"""Import and export job scaffolding."""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import get_current_org
from ..database import get_db
router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("/imports", response_model=schemas.ImportJobRead, status_code=status.HTTP_201_CREATED)
def create_import_job(payload: schemas.ImportJobCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.ImportJob(org_id=str(org.id), kind=payload.kind, payload=payload.payload or {}, status="pending")
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/imports", response_model=List[schemas.ImportJobRead])
def list_import_jobs(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.ImportJob)
        .filter(models.ImportJob.org_id == str(org.id))
        .order_by(models.ImportJob.created_at.desc())
        .all()
    )


@router.get("/imports/{job_id}", response_model=schemas.ImportJobRead)
def get_import_job(job_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = db.get(models.ImportJob, job_id)
    if not record or record.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Import job not found")
    return record


@router.post("/imports/{job_id}/run", response_model=schemas.ImportJobRead)
def run_import_job(job_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = db.get(models.ImportJob, job_id)
    if not record or record.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Import job not found")
    if record.status not in {"pending", "failed"}:
        return record

    payload = record.payload or {}
    records = payload.get("records") or []
    created = 0
    errors: List[str] = []

    try:
        if record.kind == "components":
            for item in records:
                model = models.Component(org_id=str(org.id), **item)
                db.add(model)
                created += 1
        elif record.kind == "templates":
            for item in records:
                model = models.ProductTemplate(org_id=str(org.id), **item)
                db.add(model)
                created += 1
        elif record.kind == "passports":
            for item in records:
                model = models.BatteryPassport(org_id=str(org.id), **item)
                db.add(model)
                created += 1
        else:
            errors.append(f"Unsupported import kind: {record.kind}")
        db.commit()
        record.status = "completed" if not errors else "failed"
        record.result = {"created": created}
        record.error = "; ".join(errors) if errors else None
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        record.status = "failed"
        record.error = str(exc)
    db.commit()
    db.refresh(record)
    return record


@router.post("/exports", response_model=schemas.ExportJobRead, status_code=status.HTTP_201_CREATED)
def create_export_job(payload: schemas.ExportJobCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.ExportJob(org_id=str(org.id), kind=payload.kind, payload=payload.payload or {}, status="pending")
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/exports", response_model=List[schemas.ExportJobRead])
def list_export_jobs(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.ExportJob)
        .filter(models.ExportJob.org_id == str(org.id))
        .order_by(models.ExportJob.created_at.desc())
        .all()
    )


@router.get("/exports/{job_id}", response_model=schemas.ExportJobRead)
def get_export_job(job_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = db.get(models.ExportJob, job_id)
    if not record or record.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Export job not found")
    return record


@router.post("/exports/{job_id}/run", response_model=schemas.ExportJobRead)
def run_export_job(job_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = db.get(models.ExportJob, job_id)
    if not record or record.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Export job not found")
    if record.status not in {"pending", "failed"}:
        return record

    try:
        if record.kind == "passports":
            passports = (
                db.query(models.BatteryPassport)
                .filter(models.BatteryPassport.org_id == str(org.id))
                .order_by(models.BatteryPassport.created_at.desc())
                .all()
            )
            headers = [
                "id",
                "battery_model",
                "gtin",
                "serial_number",
                "battery_category",
                "battery_weight_kg",
                "rated_capacity_kwh",
                "carbon_footprint_kg_per_kwh",
            ]
            lines = [",".join(headers)]
            for p in passports:
                lines.append(
                    ",".join(
                        [
                            str(p.id),
                            (p.battery_model or "").replace(",", " "),
                            p.gtin,
                            p.serial_number,
                            p.battery_category,
                            str(p.battery_weight_kg),
                            str(p.rated_capacity_kwh),
                            str(p.carbon_footprint_kg_per_kwh),
                        ]
                    )
                )
            record.result = {"csv": "\n".join(lines)}
            record.status = "completed"
        elif record.kind == "cbam":
            declarations = (
                db.query(models.CbamDeclaration)
                .filter(models.CbamDeclaration.org_id == str(org.id))
                .order_by(models.CbamDeclaration.created_at.desc())
                .all()
            )
            payloads = []
            for decl in declarations:
                items = db.query(models.CbamItem).filter(models.CbamItem.declaration_id == decl.id).all()
                payloads.append(
                    {
                        "id": str(decl.id),
                        "period": decl.period,
                        "status": decl.status,
                        "total_emissions": decl.total_emissions,
                        "items": [
                            {
                                "cn_code": i.cn_code,
                                "quantity_tonnes": i.quantity_tonnes,
                                "calculated_emissions": i.calculated_emissions,
                            }
                            for i in items
                        ],
                    }
                )
            record.result = {"json": payloads}
            record.status = "completed"
        else:
            record.status = "failed"
            record.error = f"Unsupported export kind: {record.kind}"
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        record.status = "failed"
        record.error = str(exc)
    db.commit()
    db.refresh(record)
    return record
