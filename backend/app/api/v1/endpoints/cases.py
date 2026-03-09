"""
Case management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.db.session import get_db
from app.models.case import Case, CaseStatus, CasePriority
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


# Schemas
class CaseCreate(BaseModel):
    case_number: str
    title: str
    description: Optional[str] = None
    case_type: Optional[str] = None
    priority: CasePriority = CasePriority.MEDIUM
    incident_location: Optional[str] = None
    incident_date: Optional[datetime] = None
    victim_name: Optional[str] = None
    lead_investigator: Optional[str] = None
    notes: Optional[str] = None


class CaseResponse(BaseModel):
    id: int
    case_number: str
    title: str
    case_type: Optional[str]
    priority: CasePriority
    status: CaseStatus
    created_at: datetime
    
    class Config:
        from_attributes = True


class CaseDetail(CaseResponse):
    description: Optional[str]
    incident_location: Optional[str]
    incident_date: Optional[datetime]
    victim_name: Optional[str]
    witness_count: int
    suspect_count: int
    lead_investigator: Optional[str]
    department: Optional[str]
    evidence_description: Optional[str]
    notes: Optional[str]
    updated_at: Optional[datetime]


@router.post("/", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(
    case_data: CaseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new case"""
    # Check if case number exists
    existing_case = db.query(Case).filter(Case.case_number == case_data.case_number).first()
    if existing_case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Case number already exists"
        )
    
    case = Case(
        **case_data.dict(),
        assigned_to=current_user.id,
        status=CaseStatus.OPEN
    )
    
    db.add(case)
    db.commit()
    db.refresh(case)
    
    return case


@router.get("/", response_model=List[CaseResponse])
def list_cases(
    skip: int = 0,
    limit: int = 20,
    status: Optional[CaseStatus] = None,
    priority: Optional[CasePriority] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all cases with filters"""
    query = db.query(Case)
    
    if status:
        query = query.filter(Case.status == status)
    if priority:
        query = query.filter(Case.priority == priority)
    
    cases = query.order_by(Case.created_at.desc()).offset(skip).limit(limit).all()
    return cases


@router.get("/{case_id}", response_model=CaseDetail)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get case details"""
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    return case


@router.put("/{case_id}", response_model=CaseDetail)
def update_case(
    case_id: int,
    case_data: CaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update case information"""
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    for key, value in case_data.dict(exclude_unset=True).items():
        setattr(case, key, value)
    
    db.commit()
    db.refresh(case)
    
    return case


@router.patch("/{case_id}/status")
def update_case_status(
    case_id: int,
    new_status: CaseStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update case status"""
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    case.status = new_status
    
    if new_status in [CaseStatus.SOLVED, CaseStatus.CLOSED]:
        case.closed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(case)
    
    return {"message": "Status updated", "new_status": new_status}


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete case"""
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    db.delete(case)
    db.commit()
    
    return None
