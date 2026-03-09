"""
Case model for case management
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class CaseStatus(str, enum.Enum):
    """Case status enumeration"""
    OPEN = "open"
    UNDER_INVESTIGATION = "under_investigation"
    SOLVED = "solved"
    CLOSED = "closed"
    COLD = "cold"


class CasePriority(str, enum.Enum):
    """Case priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Case(Base):
    """Case model"""
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Case Information
    case_number = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # Classification
    case_type = Column(String)  # e.g., "robbery", "assault", "murder"
    priority = Column(Enum(CasePriority), default=CasePriority.MEDIUM)
    status = Column(Enum(CaseStatus), default=CaseStatus.OPEN)
    
    # Location & Time
    incident_location = Column(String)
    incident_date = Column(DateTime)
    incident_time = Column(String)
    
    # People Involved
    victim_name = Column(String)
    witness_count = Column(Integer, default=0)
    suspect_count = Column(Integer, default=0)
    
    # Investigation Details
    lead_investigator = Column(String)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    department = Column(String)
    
    # Evidence
    evidence_description = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime)
    
    # Relationships
    sketches = relationship("Sketch", back_populates="case", cascade="all, delete-orphan")
    
    # Notes
    notes = Column(Text)
    
    def __repr__(self):
        return f"<Case {self.case_number}: {self.title}>"
