"""
Suspect model for database management
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class Gender(str, enum.Enum):
    """Gender enumeration"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class SuspectStatus(str, enum.Enum):
    """Suspect status enumeration"""
    ACTIVE = "active"
    ARRESTED = "arrested"
    CLEARED = "cleared"
    DECEASED = "deceased"
    UNKNOWN = "unknown"


class Suspect(Base):
    """Suspect model"""
    __tablename__ = "suspects"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal Information
    first_name = Column(String)
    last_name = Column(String)
    alias = Column(String)
    age = Column(Integer)
    date_of_birth = Column(DateTime)
    gender = Column(Enum(Gender), default=Gender.UNKNOWN)
    
    # Physical Characteristics
    height = Column(Float)  # in cm
    weight = Column(Float)  # in kg
    eye_color = Column(String)
    hair_color = Column(String)
    skin_tone = Column(String)
    
    # Identifying Features
    distinguishing_marks = Column(Text)
    tattoos = Column(Text)
    scars = Column(Text)
    
    # Criminal Information
    criminal_record = Column(Text)
    known_associates = Column(Text)
    last_known_location = Column(String)
    
    # Photos
    photo_url = Column(String)
    photo_path = Column(String)
    
    # Status
    status = Column(Enum(SuspectStatus), default=SuspectStatus.ACTIVE)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Notes
    notes = Column(Text)
    
    # Relationships
    face_encodings = relationship("FaceEncoding", back_populates="suspect", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Suspect {self.first_name} {self.last_name}>"
