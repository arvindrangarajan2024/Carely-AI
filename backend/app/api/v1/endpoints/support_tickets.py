"""Support Ticket endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.support_ticket import SupportTicket
from app.schemas.support_ticket import SupportTicketCreate, SupportTicketUpdate, SupportTicketResponse

router = APIRouter()


def generate_ticket_number() -> str:
    """Generate a unique ticket number"""
    return f"TKT-{uuid.uuid4().hex[:8].upper()}"


@router.post("/", response_model=SupportTicketResponse, status_code=status.HTTP_201_CREATED)
async def create_support_ticket(
    ticket: SupportTicketCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new support ticket"""
    # Generate unique ticket number
    ticket_number = generate_ticket_number()
    
    # Ensure patient can only create tickets for themselves
    if ticket.patient_id and int(current_user["id"]) != ticket.patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tickets for other patients"
        )
    
    # If no patient_id provided, use current user
    if not ticket.patient_id:
        ticket.patient_id = int(current_user["id"])
    
    db_ticket = SupportTicket(
        **ticket.model_dump(),
        ticket_number=ticket_number
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    return db_ticket


@router.get("/", response_model=List[SupportTicketResponse])
async def get_support_tickets(
    patient_id: int = None,
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get support tickets"""
    # If patient_id is provided, ensure it's the current user
    if patient_id and int(current_user["id"]) != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view other patients' tickets"
        )
    
    # Default to current user's tickets
    filter_patient_id = patient_id if patient_id else int(current_user["id"])
    
    query = db.query(SupportTicket).filter(SupportTicket.patient_id == filter_patient_id)
    
    if status_filter:
        query = query.filter(SupportTicket.status == status_filter)
    
    tickets = query.offset(skip).limit(limit).all()
    
    return tickets


@router.get("/{ticket_id}", response_model=SupportTicketResponse)
async def get_support_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific support ticket"""
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support ticket not found"
        )
    
    # Ensure patient can only access their own tickets
    if ticket.patient_id and int(current_user["id"]) != ticket.patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this ticket"
        )
    
    return ticket


@router.get("/number/{ticket_number}", response_model=SupportTicketResponse)
async def get_support_ticket_by_number(
    ticket_number: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a support ticket by ticket number"""
    ticket = db.query(SupportTicket).filter(SupportTicket.ticket_number == ticket_number).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support ticket not found"
        )
    
    # Ensure patient can only access their own tickets
    if ticket.patient_id and int(current_user["id"]) != ticket.patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this ticket"
        )
    
    return ticket


@router.put("/{ticket_id}", response_model=SupportTicketResponse)
async def update_support_ticket(
    ticket_id: int,
    ticket_update: SupportTicketUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a support ticket"""
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support ticket not found"
        )
    
    # Ensure patient can only update their own tickets
    if ticket.patient_id and int(current_user["id"]) != ticket.patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this ticket"
        )
    
    # Update fields
    update_data = ticket_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)
    
    db.commit()
    db.refresh(ticket)
    
    return ticket

