"""
Sketch model for face sketch management
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Sketch(Base):
    """Sketch model"""
    __tablename__ = "sketches"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    title = Column(String)
    description = Column(Text)
    
    # Sketch Data
    image_url = Column(String)
    image_path = Column(String)
    thumbnail_url = Column(String)
    
    # Canvas Data (JSON format)
    canvas_data = Column(JSON)  # Stores fabric.js canvas state
    elements_used = Column(JSON)  # List of facial elements used
    
    # Witness Information
    witness_name = Column(String)
    witness_statement = Column(Text)
    reliability_score = Column(Integer)  # 1-10
    
    # Recognition Results
    has_matches = Column(Boolean, default=False)
    match_count = Column(Integer, default=0)
    best_match_score = Column(String)
    
    # Case Association
    case_id = Column(Integer, ForeignKey("cases.id"))
    case = relationship("Case", back_populates="sketches")
    
    # Creator
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Face Encoding
    face_encodings = relationship("FaceEncoding", back_populates="sketch", cascade="all, delete-orphan")
    
    # Notes
    notes = Column(Text)
    
    def __repr__(self):
        return f"<Sketch {self.id}: {self.title}>"
