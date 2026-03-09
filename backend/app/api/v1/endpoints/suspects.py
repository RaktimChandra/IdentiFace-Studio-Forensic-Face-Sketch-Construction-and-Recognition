"""
Suspect management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import shutil
import os

from app.db.session import get_db
from app.models.suspect import Suspect, Gender, SuspectStatus
from app.models.user import User
from app.models.face_encoding import FaceEncoding
from app.api.v1.endpoints.auth import get_current_user
from app.services.face_recognition_service import face_service
from app.core.config import settings

router = APIRouter()


# Schemas
class SuspectCreate(BaseModel):
    first_name: str
    last_name: str
    alias: Optional[str] = None
    age: Optional[int] = None
    gender: Gender = Gender.UNKNOWN
    height: Optional[float] = None
    weight: Optional[float] = None
    eye_color: Optional[str] = None
    hair_color: Optional[str] = None
    distinguishing_marks: Optional[str] = None
    criminal_record: Optional[str] = None
    last_known_location: Optional[str] = None
    notes: Optional[str] = None


class SuspectResponse(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    alias: Optional[str]
    age: Optional[int]
    gender: Gender
    photo_url: Optional[str]
    status: SuspectStatus
    created_at: datetime
    
    class Config:
        from_attributes = True


class SuspectDetail(SuspectResponse):
    height: Optional[float]
    weight: Optional[float]
    eye_color: Optional[str]
    hair_color: Optional[str]
    skin_tone: Optional[str]
    distinguishing_marks: Optional[str]
    tattoos: Optional[str]
    scars: Optional[str]
    criminal_record: Optional[str]
    known_associates: Optional[str]
    last_known_location: Optional[str]
    notes: Optional[str]
    updated_at: Optional[datetime]


# Endpoints
@router.post("/", response_model=SuspectResponse, status_code=status.HTTP_201_CREATED)
async def create_suspect(
    suspect_data: SuspectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new suspect"""
    suspect = Suspect(
        **suspect_data.dict(),
        created_by=current_user.id,
        status=SuspectStatus.ACTIVE
    )
    
    db.add(suspect)
    db.commit()
    db.refresh(suspect)
    
    return suspect


@router.get("/", response_model=List[SuspectResponse])
def list_suspects(
    skip: int = 0,
    limit: int = 20,
    status: Optional[SuspectStatus] = None,
    gender: Optional[Gender] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all suspects with filters"""
    query = db.query(Suspect)
    
    if status:
        query = query.filter(Suspect.status == status)
    if gender:
        query = query.filter(Suspect.gender == gender)
    
    suspects = query.offset(skip).limit(limit).all()
    return suspects


@router.get("/{suspect_id}", response_model=SuspectDetail)
def get_suspect(
    suspect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get suspect details"""
    suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    
    if not suspect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suspect not found"
        )
    
    return suspect


@router.put("/{suspect_id}", response_model=SuspectDetail)
def update_suspect(
    suspect_id: int,
    suspect_data: SuspectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update suspect information"""
    suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    
    if not suspect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suspect not found"
        )
    
    for key, value in suspect_data.dict(exclude_unset=True).items():
        setattr(suspect, key, value)
    
    db.commit()
    db.refresh(suspect)
    
    return suspect


@router.delete("/{suspect_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_suspect(
    suspect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete suspect"""
    suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    
    if not suspect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suspect not found"
        )
    
    db.delete(suspect)
    db.commit()
    
    return None


@router.post("/{suspect_id}/photo", response_model=SuspectDetail)
async def upload_suspect_photo(
    suspect_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload photo for suspect and generate face encoding"""
    suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    
    if not suspect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suspect not found"
        )
    
    # Validate file type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type"
        )
    
    # Save file
    file_extension = file.filename.split(".")[-1]
    filename = f"suspect_{suspect_id}_{int(datetime.now().timestamp())}.{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, "suspects", filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Generate face encoding
    encoding = face_service.generate_encoding(file_path)
    
    if encoding is not None:
        # Save encoding to database
        face_encoding = FaceEncoding(
            encoding=face_service.serialize_encoding(encoding),
            source_type="suspect",
            suspect_id=suspect.id,
            confidence_score=0.95,
            image_quality_score=face_service.estimate_face_quality(file_path)
        )
        db.add(face_encoding)
    
    # Update suspect
    suspect.photo_path = file_path
    suspect.photo_url = f"/uploads/suspects/{filename}"
    
    db.commit()
    db.refresh(suspect)
    
    return suspect


@router.get("/search/{query}")
def search_suspects(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search suspects by name or alias"""
    suspects = db.query(Suspect).filter(
        (Suspect.first_name.ilike(f"%{query}%")) |
        (Suspect.last_name.ilike(f"%{query}%")) |
        (Suspect.alias.ilike(f"%{query}%"))
    ).limit(20).all()
    
    return suspects
