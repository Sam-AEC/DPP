"""Passport CRUD and QR endpoints."""

from __future__ import annotations

from io import BytesIO
import json
from typing import List
from uuid import UUID

import segno
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import get_current_org
from ..config import get_settings
from ..database import get_db

router = APIRouter(prefix="/api/passports", tags=["passports"])
settings = get_settings()


def record_audit(
    db: Session,
    action: str,
    entity: str,
    entity_id: str,
    org_id: str | None = None,
    details: dict | None = None,
):
    entry = models.AuditLog(
        actor="system",
        action=action,
        entity=entity,
        entity_id=str(entity_id),
        org_id=org_id,
        details=details or {},
    )
    db.add(entry)


@router.post("", response_model=schemas.BatteryPassportRead, status_code=status.HTTP_201_CREATED)
def create_passport(
    passport: schemas.BatteryPassportCreate,
    db: Session = Depends(get_db),
    org=Depends(get_current_org),
):
    record = models.BatteryPassport(org_id=str(org.id), **passport.model_dump())
    db.add(record)
    record_audit(
        db,
        "create",
        "battery_passport",
        record.id,
        org_id=str(org.id),
        details={"origin": "manual"},
    )
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Serial number must be unique") from exc
    db.refresh(record)
    return record


@router.get("", response_model=List[schemas.BatteryPassportRead])
def list_passports(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.BatteryPassport)
        .filter(models.BatteryPassport.org_id == str(org.id))
        .order_by(models.BatteryPassport.created_at.desc())
        .all()
    )


@router.get("/{passport_id}", response_model=schemas.BatteryPassportRead)
def get_passport(passport_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = db.get(models.BatteryPassport, passport_id)
    if not record:
        raise HTTPException(status_code=404, detail="Passport not found")
    if record.org_id and record.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Passport not found")
    return record


@router.patch("/{passport_id}", response_model=schemas.BatteryPassportRead)
def update_passport(
    passport_id: UUID,
    updates: schemas.BatteryPassportUpdate,
    db: Session = Depends(get_db),
    org=Depends(get_current_org),
):
    record = db.get(models.BatteryPassport, passport_id)
    if not record:
        raise HTTPException(status_code=404, detail="Passport not found")
    if record.org_id and record.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Passport not found")
    for key, value in updates.model_dump(exclude_none=True).items():
        setattr(record, key, value)
    try:
        record_audit(
            db,
            "update",
            "battery_passport",
            record.id,
            org_id=str(org.id),
            details={"updated_fields": list(updates.model_dump(exclude_none=True).keys())},
        )
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Serial number must be unique") from exc
    db.refresh(record)
    return record


@router.post(
    "/from-template",
    response_model=schemas.BatteryPassportRead,
    status_code=status.HTTP_201_CREATED,
)
def create_from_template(
    payload: schemas.BatteryPassportFromTemplate,
    db: Session = Depends(get_db),
    org=Depends(get_current_org),
):
    template = db.get(models.ProductTemplate, payload.template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if template.org_id and template.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Template not found")

    # Start with template defaults where present
    combined = {
        "manufacturer_name": template.manufacturer_name,
        "manufacturer_address": template.manufacturer_address,
        "battery_model": template.battery_model or template.name,
        "battery_category": template.battery_category,
        "manufacturing_place": payload.manufacturing_place,
        "manufacturing_date": payload.manufacturing_date,
        "serial_number": payload.serial_number,
        "gtin": payload.gtin or template.gtin,
        "battery_status": payload.battery_status or "original",
        "battery_weight_kg": payload.battery_weight_kg or template.battery_weight_kg,
        "carbon_footprint_kg_per_kwh": (
            payload.carbon_footprint_kg_per_kwh or template.carbon_footprint_kg_per_kwh
        ),
        "carbon_footprint_class": payload.carbon_footprint_class or template.carbon_footprint_class,
        "recycled_content_cobalt": payload.recycled_content_cobalt or template.recycled_content_cobalt,
        "recycled_content_lead": payload.recycled_content_lead or template.recycled_content_lead,
        "recycled_content_lithium": payload.recycled_content_lithium or template.recycled_content_lithium,
        "recycled_content_nickel": payload.recycled_content_nickel or template.recycled_content_nickel,
        "rated_capacity_kwh": payload.rated_capacity_kwh or template.rated_capacity_kwh,
        "expected_lifetime_cycles": payload.expected_lifetime_cycles
        or template.expected_lifetime_cycles,
        "expected_lifetime_years": payload.expected_lifetime_years or template.expected_lifetime_years,
        "hazardous_substances": payload.hazardous_substances or template.hazardous_substances,
        "performance_class": payload.performance_class or template.performance_class,
        "additional_public_data": payload.additional_public_data or template.additional_public_data,
        "restricted_data": payload.restricted_data or template.restricted_data,
        "end_of_life": payload.end_of_life,
        "template_id": template.id,
    }

    # Ensure required fields exist
    required_fields = [
        "manufacturer_name",
        "manufacturer_address",
        "battery_model",
        "battery_category",
        "manufacturing_date",
        "manufacturing_place",
        "serial_number",
        "gtin",
        "battery_weight_kg",
        "carbon_footprint_kg_per_kwh",
        "rated_capacity_kwh",
    ]
    missing = [field for field in required_fields if combined.get(field) in (None, "")]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Template + overrides missing required fields: {', '.join(missing)}",
        )

    # Snapshot linked components for traceability
    template_components = (
        db.query(models.TemplateComponent)
        .filter(models.TemplateComponent.template_id == template.id)
        .all()
    )
    combined["component_snapshot"] = [
        {
            "component_id": str(item.component_id),
            "quantity": item.quantity,
            "notes": item.notes,
        }
        for item in template_components
    ]

    record = models.BatteryPassport(org_id=str(org.id), **combined)
    db.add(record)
    record_audit(
        db,
        "create",
        "battery_passport",
        record.id,
        org_id=str(org.id),
        details={"origin": "template", "template_id": str(template.id)},
    )
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


@router.get("/{passport_id}/export/jsonld")
def export_jsonld(passport_id: UUID, db: Session = Depends(get_db)):
    record = db.get(models.BatteryPassport, passport_id)
    if not record:
        raise HTTPException(status_code=404, detail="Passport not found")
    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": record.battery_model,
        "manufacturer": record.manufacturer_name,
        "gtin": record.gtin,
        "serialNumber": record.serial_number,
        "category": record.battery_category,
        "weight": {"value": record.battery_weight_kg, "unitCode": "KGM"},
        "carbonFootprint": record.carbon_footprint_kg_per_kwh,
        "additionalProperty": [
            {"name": "batteryStatus", "value": record.battery_status},
            {"name": "ratedCapacityKWh", "value": record.rated_capacity_kwh},
            {"name": "carbonFootprintClass", "value": record.carbon_footprint_class},
            {"name": "recycledContentCobalt", "value": record.recycled_content_cobalt},
            {"name": "recycledContentNickel", "value": record.recycled_content_nickel},
            {"name": "recycledContentLithium", "value": record.recycled_content_lithium},
            {"name": "recycledContentLead", "value": record.recycled_content_lead},
            {"name": "expectedLifetimeCycles", "value": record.expected_lifetime_cycles},
            {"name": "expectedLifetimeYears", "value": record.expected_lifetime_years},
            {"name": "hazardousSubstances", "value": record.hazardous_substances},
        ],
    }
    return JSONResponse(content=data)
