"""Medical Record endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.medical_record import MedicalRecord
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse

router = APIRouter()


@router.post("/", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_medical_record(
    record: MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new medical record"""
    # In a real system, only healthcare providers should create medical records
    # For now, we'll allow patients to create their own records
    if int(current_user["id"]) != record.patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create medical records for other patients"
        )
    
    db_record = MedicalRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record


@router.get("/", response_model=List[MedicalRecordResponse])
async def get_medical_records(
    patient_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get medical records"""
    # If patient_id is provided, ensure it's the current user
    if patient_id and int(current_user["id"]) != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view other patients' medical records"
        )
    
    # Default to current user's records
    filter_patient_id = patient_id if patient_id else int(current_user["id"])
    
    records = db.query(MedicalRecord)\
        .filter(MedicalRecord.patient_id == filter_patient_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return records


@router.get("/{record_id}", response_model=MedicalRecordResponse)
async def get_medical_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific medical record"""
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )
    
    # Ensure patient can only access their own records
    if int(current_user["id"]) != record.patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this medical record"
        )
    
    return record


@router.put("/{record_id}", response_model=MedicalRecordResponse)
async def update_medical_record(
    record_id: int,
    record_update: MedicalRecordUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a medical record"""
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )
    
    # Ensure patient can only update their own records
    if int(current_user["id"]) != record.patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this medical record"
        )
    
    # Update fields
    update_data = record_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
    
    db.commit()
    db.refresh(record)
    
    return record

