"""Scaffolds for CRA, EUDR, AI Act, EPD, NIS2-lite."""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import get_current_org
from ..database import get_db

router = APIRouter(prefix="/api/compliance", tags=["compliance"])


def _org_check(record_org: str | None, org_id: str):
    if record_org and record_org != org_id:
        raise HTTPException(status_code=404, detail="Not found")


# CRA
@router.post("/cra/products", response_model=schemas.CraProductRead, status_code=status.HTTP_201_CREATED)
def create_cra_product(payload: schemas.CraProductCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.CraProduct(org_id=str(org.id), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/cra/products", response_model=List[schemas.CraProductRead])
def list_cra_products(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.CraProduct)
        .filter(models.CraProduct.org_id == str(org.id))
        .order_by(models.CraProduct.created_at.desc())
        .all()
    )


@router.get("/cra/products/{product_id}", response_model=schemas.CraProductRead)
def get_cra_product(product_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = db.get(models.CraProduct, product_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    _org_check(record.org_id, str(org.id))
    return record


# EUDR
@router.post("/eudr/suppliers", response_model=schemas.EudrSupplierRead, status_code=status.HTTP_201_CREATED)
def create_eudr_supplier(payload: schemas.EudrSupplierCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.EudrSupplier(org_id=str(org.id), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/eudr/suppliers", response_model=List[schemas.EudrSupplierRead])
def list_eudr_suppliers(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.EudrSupplier)
        .filter(models.EudrSupplier.org_id == str(org.id))
        .order_by(models.EudrSupplier.created_at.desc())
        .all()
    )


# AI Act
@router.post("/ai/systems", response_model=schemas.AiSystemRead, status_code=status.HTTP_201_CREATED)
def create_ai_system(payload: schemas.AiSystemCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.AiSystem(org_id=str(org.id), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/ai/systems", response_model=List[schemas.AiSystemRead])
def list_ai_systems(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.AiSystem)
        .filter(models.AiSystem.org_id == str(org.id))
        .order_by(models.AiSystem.created_at.desc())
        .all()
    )


@router.post("/ai/incidents", response_model=schemas.AiIncidentRead, status_code=status.HTTP_201_CREATED)
def create_ai_incident(payload: schemas.AiIncidentCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    system = db.get(models.AiSystem, payload.system_id)
    if not system or (system.org_id and system.org_id != str(org.id)):
        raise HTTPException(status_code=404, detail="AI system not found")
    record = models.AiIncident(org_id=str(org.id), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/ai/incidents", response_model=List[schemas.AiIncidentRead])
def list_ai_incidents(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.AiIncident)
        .filter(models.AiIncident.org_id == str(org.id))
        .order_by(models.AiIncident.created_at.desc())
        .all()
    )


# EPD
@router.post("/epd/records", response_model=schemas.EpdRecordRead, status_code=status.HTTP_201_CREATED)
def create_epd_record(payload: schemas.EpdRecordCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.EpdRecord(org_id=str(org.id), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/epd/records", response_model=List[schemas.EpdRecordRead])
def list_epd_records(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.EpdRecord)
        .filter(models.EpdRecord.org_id == str(org.id))
        .order_by(models.EpdRecord.created_at.desc())
        .all()
    )


@router.get("/epd/records/export/placeholder")
def export_epd_placeholder(org=Depends(get_current_org)):
    content = (
        f"EPD export placeholder for org {org.id}. Provide EN 15804-compliant data (PCR references, LCA docs)."
    )
    return StreamingResponse(
        iter([content]),
        media_type="text/plain",
        headers={"Content-Disposition": 'attachment; filename="epd_placeholder.txt"'},
    )


# NIS2-lite
@router.post("/nis2/attestations", response_model=schemas.Nis2AttestationRead, status_code=status.HTTP_201_CREATED)
def create_attestation(payload: schemas.Nis2AttestationCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.Nis2Attestation(org_id=str(org.id), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/nis2/attestations", response_model=List[schemas.Nis2AttestationRead])
def list_attestations(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.Nis2Attestation)
        .filter(models.Nis2Attestation.org_id == str(org.id))
        .order_by(models.Nis2Attestation.created_at.desc())
        .all()
    )


@router.get("/export/placeholder")
def export_compliance_placeholder(org=Depends(get_current_org)):
    # Placeholder combined export for CRA/EUDR/AI/EPD/NIS2 data.
    content = (
        f"Compliance export placeholder for org {org.id}. "
        "Integrate real exports per regulation (CRA SBOM/vuln, EUDR DDS, AI incidents, EPD EN15804, NIS2 evidence)."
    )
    return StreamingResponse(
        iter([content]),
        media_type="text/plain",
        headers={"Content-Disposition": 'attachment; filename="compliance_placeholder.txt"'},
    )
