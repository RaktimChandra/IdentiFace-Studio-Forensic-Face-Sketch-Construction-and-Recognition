"""
Sketch management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import shutil
import os
import json

from app.db.session import get_db
from app.models.sketch import Sketch
from app.models.user import User
from app.models.face_encoding import FaceEncoding
from app.api.v1.endpoints.auth import get_current_user
from app.services.face_recognition_service import face_service
from app.core.config import settings

router = APIRouter()


# Schemas
class SketchCreate(BaseModel):
    title: str
    description: Optional[str] = None
    case_id: Optional[int] = None
    witness_name: Optional[str] = None
    witness_statement: Optional[str] = None
    reliability_score: Optional[int] = None
    notes: Optional[str] = None


class SketchResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    image_url: Optional[str]
    has_matches: bool
    match_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SketchDetail(SketchResponse):
    canvas_data: Optional[dict]
    elements_used: Optional[dict]
    witness_name: Optional[str]
    witness_statement: Optional[str]
    reliability_score: Optional[int]
    best_match_score: Optional[str]
    case_id: Optional[int]
    notes: Optional[str]
    updated_at: Optional[datetime]


@router.post("/", response_model=SketchResponse, status_code=status.HTTP_201_CREATED)
def create_sketch(
    sketch_data: SketchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new sketch"""
    sketch = Sketch(
        **sketch_data.dict(),
        created_by=current_user.id
    )
    
    db.add(sketch)
    db.commit()
    db.refresh(sketch)
    
    return sketch


@router.get("/", response_model=List[SketchResponse])
def list_sketches(
    skip: int = 0,
    limit: int = 20,
    case_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all sketches"""
    query = db.query(Sketch)
    
    if case_id:
        query = query.filter(Sketch.case_id == case_id)
    
    sketches = query.order_by(Sketch.created_at.desc()).offset(skip).limit(limit).all()
    return sketches


@router.get("/{sketch_id}", response_model=SketchDetail)
def get_sketch(
    sketch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get sketch details"""
    sketch = db.query(Sketch).filter(Sketch.id == sketch_id).first()
    
    if not sketch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sketch not found"
        )
    
    return sketch


@router.put("/{sketch_id}", response_model=SketchDetail)
def update_sketch(
    sketch_id: int,
    sketch_data: SketchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update sketch"""
    sketch = db.query(Sketch).filter(Sketch.id == sketch_id).first()
    
    if not sketch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sketch not found"
        )
    
    for key, value in sketch_data.dict(exclude_unset=True).items():
        setattr(sketch, key, value)
    
    db.commit()
    db.refresh(sketch)
    
    return sketch


@router.post("/{sketch_id}/image", response_model=SketchDetail)
async def upload_sketch_image(
    sketch_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload sketch image and generate face encoding"""
    sketch = db.query(Sketch).filter(Sketch.id == sketch_id).first()
    
    if not sketch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sketch not found"
        )
    
    # Validate file type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type"
        )
    
    # Save file
    file_extension = file.filename.split(".")[-1]
    filename = f"sketch_{sketch_id}_{int(datetime.now().timestamp())}.{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, "sketches", filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Generate face encoding
    encoding = face_service.generate_encoding(file_path)
    
    if encoding is not None:
        # Save encoding
        face_encoding = FaceEncoding(
            encoding=face_service.serialize_encoding(encoding),
            source_type="sketch",
            sketch_id=sketch.id,
            confidence_score=0.90,
            image_quality_score=face_service.estimate_face_quality(file_path)
        )
        db.add(face_encoding)
    
    # Update sketch
    sketch.image_path = file_path
    sketch.image_url = f"/uploads/sketches/{filename}"
    
    db.commit()
    db.refresh(sketch)
    
    return sketch


@router.post("/{sketch_id}/canvas")
def save_canvas_data(
    sketch_id: int,
    canvas_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Save canvas data (fabric.js state)"""
    sketch = db.query(Sketch).filter(Sketch.id == sketch_id).first()
    
    if not sketch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sketch not found"
        )
    
    sketch.canvas_data = canvas_data
    
    # Extract elements used
    if "objects" in canvas_data:
        elements = {}
        for obj in canvas_data["objects"]:
            if "element_type" in obj:
                elem_type = obj["element_type"]
                elements[elem_type] = elements.get(elem_type, 0) + 1
        sketch.elements_used = elements
    
    db.commit()
    db.refresh(sketch)
    
    return {"message": "Canvas data saved", "elements_count": len(canvas_data.get("objects", []))}


@router.delete("/{sketch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sketch(
    sketch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete sketch"""
    sketch = db.query(Sketch).filter(Sketch.id == sketch_id).first()
    
    if not sketch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sketch not found"
        )
    
    db.delete(sketch)
    db.commit()
    
    return None
