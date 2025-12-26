"""Restricted artifact metadata endpoints."""

from __future__ import annotations

from typing import List
from uuid import UUID

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError

from .. import models, schemas
from ..auth import get_current_org
from ..config import get_settings
from ..database import get_db

router = APIRouter(prefix="/api/artifacts", tags=["artifacts"])
settings = get_settings()
s3_client = None
if settings.use_s3 and settings.s3_bucket:
    s3_client = boto3.client(
        "s3",
        region_name=settings.s3_region,
        endpoint_url=settings.s3_endpoint_url or None,
        aws_access_key_id=settings.aws_access_key_id or None,
        aws_secret_access_key=settings.aws_secret_access_key or None,
    )


def _public_s3_url(key: str) -> str:
    if settings.s3_endpoint_url:
        return f"{settings.s3_endpoint_url.rstrip('/')}/{settings.s3_bucket}/{key}"
    if settings.s3_region:
        return f"https://{settings.s3_bucket}.s3.{settings.s3_region}.amazonaws.com/{key}"
    return f"https://{settings.s3_bucket}.s3.amazonaws.com/{key}"


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
    if settings.use_s3:
        if not s3_client or not settings.s3_bucket:
            raise HTTPException(status_code=500, detail="S3 storage not configured")
        key = f"{org.id}/{filename}"
        try:
            upload_url = s3_client.generate_presigned_url(
                "put_object",
                Params={"Bucket": settings.s3_bucket, "Key": key},
                ExpiresIn=900,
            )
        except (BotoCoreError, ClientError, NoCredentialsError):
            raise HTTPException(status_code=500, detail="Failed to generate upload URL")
        return {"upload_url": upload_url, "public_url": _public_s3_url(key)}
    # Placeholder for local storage path if not using S3.
    return {
        "upload_url": f"/storage/{org.id}/{filename}",
        "public_url": f"/storage/{org.id}/{filename}",
    }


@router.post("/upload", response_model=schemas.RestrictedArtifactRead, status_code=status.HTTP_201_CREATED)
async def upload_artifact(
    passport_id: UUID = Form(...),
    kind: str = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    org=Depends(get_current_org),
):
    passport = db.get(models.BatteryPassport, passport_id)
    if not passport or (passport.org_id and passport.org_id != str(org.id)):
        raise HTTPException(status_code=404, detail="Passport not found")

    filename = f"{uuid.uuid4()}_{file.filename}"
    contents = await file.read()

    if settings.use_s3:
        if not s3_client or not settings.s3_bucket:
            raise HTTPException(status_code=500, detail="S3 storage not configured")
        key = f"{org.id}/{filename}"
        try:
            s3_client.put_object(
                Bucket=settings.s3_bucket,
                Key=key,
                Body=contents,
                ContentType=file.content_type or "application/octet-stream",
            )
        except (BotoCoreError, ClientError, NoCredentialsError):
            raise HTTPException(status_code=500, detail="Failed to upload artifact to S3")
        public_url = _public_s3_url(key)
    else:
        storage_dir = Path(settings.storage_path) / str(org.id)
        storage_dir.mkdir(parents=True, exist_ok=True)
        dest = storage_dir / filename
        dest.write_bytes(contents)
        public_url = f"/storage/{org.id}/{filename}"

    record = models.RestrictedArtifact(
        org_id=str(org.id),
        passport_id=passport_id,
        kind=kind,
        title=title,
        url=public_url,
        metadata={"original_filename": file.filename},
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


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
