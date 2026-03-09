"""
Face encoding model for storing face recognition data
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class FaceEncoding(Base):
    """Face encoding model for face recognition"""
    __tablename__ = "face_encodings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Encoding Data (128-dimensional vector)
    encoding = Column(LargeBinary, nullable=False)  # Pickled numpy array
    
    # Source Information
    source_type = Column(String)  # 'suspect' or 'sketch'
    
    # Suspect Association
    suspect_id = Column(Integer, ForeignKey("suspects.id"), nullable=True)
    suspect = relationship("Suspect", back_populates="face_encodings")
    
    # Sketch Association
    sketch_id = Column(Integer, ForeignKey("sketches.id"), nullable=True)
    sketch = relationship("Sketch", back_populates="face_encodings")
    
    # Face Detection Info
    face_location = Column(String)  # JSON string of bounding box
    face_landmarks = Column(String)  # JSON string of facial landmarks
    
    # Quality Metrics
    confidence_score = Column(Float)
    image_quality_score = Column(Float)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<FaceEncoding {self.id} ({self.source_type})>"
