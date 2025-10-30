"""Authentication endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)
from app.db.session import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientResponse
from app.schemas.auth import Token

router = APIRouter()


@router.post("/register", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def register(patient: PatientCreate, db: Session = Depends(get_db)):
    """Register a new patient"""
    # Check if patient already exists
    existing_patient = db.query(Patient).filter(Patient.email == patient.email).first()
    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new patient
    db_patient = Patient(
        email=patient.email,
        hashed_password=get_password_hash(patient.password),
        first_name=patient.first_name,
        last_name=patient.last_name,
        date_of_birth=patient.date_of_birth,
        phone_number=patient.phone_number,
        address=patient.address,
        emergency_contact_name=patient.emergency_contact_name,
        emergency_contact_phone=patient.emergency_contact_phone,
        blood_type=patient.blood_type,
        allergies=patient.allergies,
        medical_conditions=patient.medical_conditions,
        medications=patient.medications,
        insurance_provider=patient.insurance_provider,
        insurance_policy_number=patient.insurance_policy_number,
        preferred_language=patient.preferred_language
    )
    
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    return db_patient


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    # Authenticate patient
    patient = db.query(Patient).filter(Patient.email == form_data.username).first()
    if not patient or not verify_password(form_data.password, patient.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(patient.id), "email": patient.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=PatientResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current authenticated user information"""
    patient = db.query(Patient).filter(Patient.id == int(current_user["id"])).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    return patient

