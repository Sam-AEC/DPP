"""Catalog and template endpoints for reusable battery specs."""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import get_current_org
from ..database import get_db

router = APIRouter(prefix="/api/catalog", tags=["catalog"])


# Components
@router.post("/components", response_model=schemas.ComponentRead, status_code=status.HTTP_201_CREATED)
def create_component(payload: schemas.ComponentCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.Component(org_id=str(org.id), **payload.model_dump(exclude={"org_id"}))
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/components", response_model=List[schemas.ComponentRead])
def list_components(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.Component)
        .filter(models.Component.org_id == str(org.id))
        .order_by(models.Component.created_at.desc())
        .all()
    )


@router.get("/components/{component_id}", response_model=schemas.ComponentRead)
def get_component(component_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = db.get(models.Component, component_id)
    if not record:
        raise HTTPException(status_code=404, detail="Component not found")
    if record.org_id and record.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Component not found")
    return record


@router.patch("/components/{component_id}", response_model=schemas.ComponentRead)
def update_component(
    component_id: UUID, payload: schemas.ComponentUpdate, db: Session = Depends(get_db), org=Depends(get_current_org)
):
    record = db.get(models.Component, component_id)
    if not record:
        raise HTTPException(status_code=404, detail="Component not found")
    if record.org_id and record.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Component not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


# Templates
@router.post("/templates", response_model=schemas.ProductTemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(payload: schemas.ProductTemplateCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.ProductTemplate(org_id=str(org.id), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/templates", response_model=List[schemas.ProductTemplateRead])
def list_templates(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.ProductTemplate)
        .filter(models.ProductTemplate.org_id == str(org.id))
        .order_by(models.ProductTemplate.created_at.desc())
        .all()
    )


@router.get("/templates/{template_id}", response_model=schemas.ProductTemplateRead)
def get_template(template_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = db.get(models.ProductTemplate, template_id)
    if not record:
        raise HTTPException(status_code=404, detail="Template not found")
    if record.org_id and record.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Template not found")
    return record


@router.patch("/templates/{template_id}", response_model=schemas.ProductTemplateRead)
def update_template(
    template_id: UUID, payload: schemas.ProductTemplateUpdate, db: Session = Depends(get_db), org=Depends(get_current_org)
):
    record = db.get(models.ProductTemplate, template_id)
    if not record:
        raise HTTPException(status_code=404, detail="Template not found")
    if record.org_id and record.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Template not found")
    for key, value in payload.model_dump(exclude_none=True, exclude={"org_id"}).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


@router.post(
    "/templates/{template_id}/components",
    response_model=schemas.TemplateComponentRead,
    status_code=status.HTTP_201_CREATED,
)
def attach_component(
    template_id: UUID,
    payload: schemas.TemplateComponentCreate,
    db: Session = Depends(get_db),
    org=Depends(get_current_org),
):
    if str(payload.template_id) != str(template_id):
        raise HTTPException(status_code=400, detail="template_id mismatch")
    template = db.get(models.ProductTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if template.org_id and template.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Template not found")
    component = db.get(models.Component, payload.component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    if component.org_id and component.org_id != str(org.id):
        raise HTTPException(status_code=404, detail="Component not found")
    record = models.TemplateComponent(org_id=str(org.id), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get(
    "/templates/{template_id}/components",
    response_model=List[schemas.TemplateComponentRead],
)
def list_template_components(template_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    template = db.get(models.ProductTemplate, template_id)
    if not template or (template.org_id and template.org_id != str(org.id)):
        raise HTTPException(status_code=404, detail="Template not found")
    return (
        db.query(models.TemplateComponent)
        .filter(models.TemplateComponent.template_id == template_id)
        .order_by(models.TemplateComponent.created_at.desc())
        .all()
    )
