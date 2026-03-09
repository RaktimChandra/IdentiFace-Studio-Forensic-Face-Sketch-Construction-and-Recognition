"""
Face recognition endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import shutil
import os

from app.db.session import get_db
from app.models.sketch import Sketch
from app.models.suspect import Suspect
from app.models.face_encoding import FaceEncoding
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.services.face_recognition_service import face_service
from app.core.config import settings

router = APIRouter()


# Schemas
class MatchResult(BaseModel):
    suspect_id: int
    similarity_score: float
    is_match: bool
    confidence: str
    suspect_info: dict


class RecognitionResponse(BaseModel):
    total_matches: int
    processing_time: float
    matches: List[MatchResult]


@router.post("/match-sketch/{sketch_id}", response_model=RecognitionResponse)
def match_sketch(
    sketch_id: int,
    min_score: float = 0.4,
    max_results: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Match sketch against suspect database"""
    import time
    start_time = time.time()
    
    # Get sketch
    sketch = db.query(Sketch).filter(Sketch.id == sketch_id).first()
    if not sketch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sketch not found"
        )
    
    # Get sketch face encoding
    sketch_encoding_record = db.query(FaceEncoding).filter(
        FaceEncoding.sketch_id == sketch_id
    ).first()
    
    if not sketch_encoding_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No face encoding found for sketch. Please upload sketch image first."
        )
    
    sketch_encoding = face_service.deserialize_encoding(sketch_encoding_record.encoding)
    
    # Get all suspect encodings
    suspect_encodings = db.query(FaceEncoding).filter(
        FaceEncoding.source_type == "suspect",
        FaceEncoding.suspect_id.isnot(None)
    ).all()
    
    if not suspect_encodings:
        return RecognitionResponse(
            total_matches=0,
            processing_time=time.time() - start_time,
            matches=[]
        )
    
    # Prepare encodings for batch comparison
    database_encodings = [
        (enc.suspect_id, face_service.deserialize_encoding(enc.encoding))
        for enc in suspect_encodings
    ]
    
    # Perform batch comparison
    matches = face_service.batch_compare(sketch_encoding, database_encodings)
    
    # Filter by minimum score
    filtered_matches = [m for m in matches if m["similarity_score"] >= min_score]
    
    # Get suspect details
    results = []
    for match in filtered_matches[:max_results]:
        suspect = db.query(Suspect).filter(Suspect.id == match["suspect_id"]).first()
        if suspect:
            results.append(MatchResult(
                suspect_id=match["suspect_id"],
                similarity_score=match["similarity_score"],
                is_match=match["is_match"],
                confidence=match["confidence"],
                suspect_info={
                    "first_name": suspect.first_name,
                    "last_name": suspect.last_name,
                    "alias": suspect.alias,
                    "age": suspect.age,
                    "gender": suspect.gender.value if suspect.gender else None,
                    "photo_url": suspect.photo_url,
                    "status": suspect.status.value if suspect.status else None
                }
            ))
    
    # Update sketch with match info
    sketch.has_matches = len(results) > 0
    sketch.match_count = len(results)
    if results:
        sketch.best_match_score = f"{results[0].similarity_score:.2%}"
    db.commit()
    
    processing_time = time.time() - start_time
    
    return RecognitionResponse(
        total_matches=len(results),
        processing_time=processing_time,
        matches=results
    )


@router.post("/match-photo", response_model=RecognitionResponse)
async def match_photo(
    file: UploadFile = File(...),
    min_score: float = 0.4,
    max_results: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Match uploaded photo against suspect database"""
    import time
    start_time = time.time()
    
    # Validate file
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type"
        )
    
    # Save temp file
    temp_filename = f"temp_{int(datetime.now().timestamp())}_{file.filename}"
    temp_path = os.path.join(settings.UPLOAD_DIR, "temp", temp_filename)
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Generate encoding
    query_encoding = face_service.generate_encoding(temp_path)
    
    if query_encoding is None:
        os.remove(temp_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No face detected in uploaded image"
        )
    
    # Get all suspect encodings
    suspect_encodings = db.query(FaceEncoding).filter(
        FaceEncoding.source_type == "suspect",
        FaceEncoding.suspect_id.isnot(None)
    ).all()
    
    if not suspect_encodings:
        os.remove(temp_path)
        return RecognitionResponse(
            total_matches=0,
            processing_time=time.time() - start_time,
            matches=[]
        )
    
    # Prepare encodings
    database_encodings = [
        (enc.suspect_id, face_service.deserialize_encoding(enc.encoding))
        for enc in suspect_encodings
    ]
    
    # Perform comparison
    matches = face_service.batch_compare(query_encoding, database_encodings)
    
    # Filter and format results
    filtered_matches = [m for m in matches if m["similarity_score"] >= min_score]
    
    results = []
    for match in filtered_matches[:max_results]:
        suspect = db.query(Suspect).filter(Suspect.id == match["suspect_id"]).first()
        if suspect:
            results.append(MatchResult(
                suspect_id=match["suspect_id"],
                similarity_score=match["similarity_score"],
                is_match=match["is_match"],
                confidence=match["confidence"],
                suspect_info={
                    "first_name": suspect.first_name,
                    "last_name": suspect.last_name,
                    "alias": suspect.alias,
                    "age": suspect.age,
                    "gender": suspect.gender.value if suspect.gender else None,
                    "photo_url": suspect.photo_url,
                    "status": suspect.status.value if suspect.status else None
                }
            ))
    
    # Clean up temp file
    os.remove(temp_path)
    
    processing_time = time.time() - start_time
    
    return RecognitionResponse(
        total_matches=len(results),
        processing_time=processing_time,
        matches=results
    )


@router.get("/stats")
def get_recognition_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get face recognition statistics"""
    total_suspects = db.query(Suspect).count()
    total_sketches = db.query(Sketch).count()
    suspects_with_encodings = db.query(FaceEncoding).filter(
        FaceEncoding.source_type == "suspect"
    ).count()
    sketches_with_matches = db.query(Sketch).filter(Sketch.has_matches == True).count()
    
    return {
        "total_suspects": total_suspects,
        "total_sketches": total_sketches,
        "suspects_with_encodings": suspects_with_encodings,
        "sketches_with_matches": sketches_with_matches,
        "recognition_ready": suspects_with_encodings > 0
    }
