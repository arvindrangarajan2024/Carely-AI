"""
AI Agent for handling appointment scheduling through natural conversation.
This agent extracts appointment details, suggests available slots, and completes bookings.
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from sqlalchemy.orm import Session
import json
import re

from app.core.config import settings
from app.models.appointment import Appointment
from app.models.patient import Patient


class AppointmentAgent:
    """AI Agent that handles appointment scheduling requests"""
    
    # Appointment types available
    APPOINTMENT_TYPES = [
        "consultation",
        "follow-up",
        "check-up",
        "emergency",
        "vaccination",
        "lab_test",
        "physical_exam",
        "specialist_visit"
    ]
    
    # Available doctors (in a real system, this would come from a database)
    DOCTORS = [
        {"name": "Dr. Sarah Johnson", "specialty": "General Practice", "id": "dr_johnson"},
        {"name": "Dr. Michael Chen", "specialty": "Cardiology", "id": "dr_chen"},
        {"name": "Dr. Emily Rodriguez", "specialty": "Pediatrics", "id": "dr_rodriguez"},
        {"name": "Dr. James Williams", "specialty": "Orthopedics", "id": "dr_williams"},
        {"name": "Dr. Lisa Anderson", "specialty": "Dermatology", "id": "dr_anderson"}
    ]
    
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the appointment agent"""
        return f"""You are an intelligent appointment management agent for Carely Healthcare.

Your capabilities:
1. **Book appointments** - Schedule new appointments with doctors
2. **List appointments** - Show user's upcoming and past appointments  
3. **Cancel appointments** - Cancel existing appointments by ID
4. **Update/Reschedule appointments** - Modify appointment times and details
5. **Show available slots** - Display available time slots

Available appointment types: {', '.join(self.APPOINTMENT_TYPES)}

Available doctors:
{self._format_doctors_list()}

Guidelines:
- Be conversational, friendly, and helpful
- For booking: Ask clarifying questions if details are missing
- For cancellations: Confirm before cancelling
- For updates: Ask what they want to change
- Handle date/time parsing intelligently (e.g., "tomorrow at 2pm", "next Monday morning")
- Default to 30-minute appointments unless specified
- Remind users they can choose in-person or virtual appointments
- Users can reference appointments by their ID number (e.g., "appointment #5")

**For booking new appointments**, when you have enough information, respond with JSON:
{{
  "action": "book_appointment",
  "appointment_details": {{
    "appointment_type": "consultation",
    "doctor_name": "Dr. Sarah Johnson",
    "scheduled_time": "2024-11-10T14:00:00",
    "reason": "Annual check-up",
    "is_virtual": false,
    "duration_minutes": 30
  }}
}}

**For showing available slots**:
{{
  "action": "show_slots",
  "date_range": "2024-11-10 to 2024-11-15"
}}

**For rescheduling**, when user provides new time and appointment ID:
{{
  "action": "update_appointment",
  "appointment_id": 5,
  "updates": {{
    "scheduled_time": "2024-11-12T15:00:00"
  }}
}}

Note: List and cancel operations are handled directly without AI processing.

Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    def _format_doctors_list(self) -> str:
        """Format doctors list for system prompt"""
        return '\n'.join([f"- {doc['name']} ({doc['specialty']})" for doc in self.DOCTORS])
    
    def detect_appointment_intent(self, message: str) -> str:
        """
        Detect if the message is related to appointments and what type of operation.
        Returns: 'create', 'list', 'view', 'update', 'cancel', or None
        """
        message_lower = message.lower()
        
        # Cancel/Delete keywords
        cancel_keywords = ['cancel', 'delete', 'remove appointment', 'cancel appointment']
        if any(keyword in message_lower for keyword in cancel_keywords):
            return 'cancel'
        
        # Update/Reschedule keywords
        update_keywords = ['reschedule', 'change', 'move', 'update', 'modify appointment']
        if any(keyword in message_lower for keyword in update_keywords):
            return 'update'
        
        # List/View all appointments
        list_keywords = ['my appointments', 'my appointment', 'list appointments', 'list appointment',
                        'show appointments', 'show appointment', 'show my', 'list my',
                        'view appointments', 'view appointment', 'view my',
                        'upcoming appointments', 'appointment history', 'see my appointments',
                        'all appointments', 'next appointment', 'check my appointments',
                        'display appointments', 'get my appointments', 'what appointments']
        if any(keyword in message_lower for keyword in list_keywords):
            return 'list'
        
        # Create/Book keywords
        create_keywords = ['book', 'schedule', 'make appointment', 'need appointment',
                          'want appointment', 'see a doctor', 'consultation', 'check-up',
                          'available', 'time slot']
        if any(keyword in message_lower for keyword in create_keywords):
            return 'create'
        
        # Check for general appointment mention
        if 'appointment' in message_lower:
            return 'general'
        
        return None
    
    def generate_available_slots(
        self, 
        start_date: Optional[datetime] = None,
        days_ahead: int = 7
    ) -> List[Dict]:
        """
        Generate available appointment slots.
        In a real system, this would check actual doctor availability.
        """
        if start_date is None:
            start_date = datetime.now()
        
        # Remove time component
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        slots = []
        
        # Generate slots for next N days (weekdays only, 9 AM - 5 PM)
        for day_offset in range(days_ahead):
            current_date = start_date + timedelta(days=day_offset)
            
            # Skip weekends
            if current_date.weekday() >= 5:
                continue
            
            # Generate slots for business hours (9 AM - 5 PM, every 30 mins)
            for hour in range(9, 17):
                for minute in [0, 30]:
                    slot_time = current_date.replace(hour=hour, minute=minute)
                    
                    # Skip past times
                    if slot_time < datetime.now():
                        continue
                    
                    slots.append({
                        "datetime": slot_time.isoformat(),
                        "formatted": slot_time.strftime("%A, %B %d at %I:%M %p"),
                        "available": True
                    })
        
        return slots[:20]  # Return first 20 available slots
    
    def extract_appointment_details(self, ai_response: str) -> Optional[Dict]:
        """
        Extract appointment details from AI response if present.
        Looks for JSON data in the response.
        """
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{[\s\S]*\}', ai_response)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                
                if data.get('action') in ['book_appointment', 'show_slots', 'list_appointments', 
                                          'cancel_appointment', 'update_appointment']:
                    return data
        except (json.JSONDecodeError, AttributeError):
            pass
        
        return None
    
    def list_appointments(self, patient_id: int, db: Session, limit: int = 10) -> Tuple[str, Dict]:
        """
        List appointments for a patient.
        Returns formatted message and appointment data.
        """
        try:
            # Query appointments (exclude cancelled ones)
            appointments = db.query(Appointment).filter(
                Appointment.patient_id == patient_id,
                Appointment.status != 'cancelled'
            ).order_by(Appointment.scheduled_time.desc()).limit(limit).all()
            
            if not appointments:
                return "You don't have any appointments scheduled yet. Would you like to book one?", {
                    "action": "list_appointments",
                    "appointments": [],
                    "count": 0
                }
            
            # Format appointments
            response = f"📅 **Your Appointments** ({len(appointments)} total):\n\n"
            
            appointment_list = []
            for apt in appointments:
                status_emoji = {
                    'scheduled': '🟢',
                    'confirmed': '✅',
                    'completed': '✔️',
                    'cancelled': '❌'
                }.get(apt.status, '⚪')
                
                response += f"{status_emoji} **Appointment #{apt.id}**\n"
                response += f"   • Doctor: {apt.doctor_name}\n"
                response += f"   • Type: {apt.appointment_type.title()}\n"
                response += f"   • Date: {apt.scheduled_time.strftime('%A, %B %d, %Y at %I:%M %p')}\n"
                response += f"   • Status: {apt.status.title()}\n"
                if apt.reason:
                    response += f"   • Reason: {apt.reason}\n"
                response += f"   • Location: {'Virtual' if apt.is_virtual else (apt.location or 'Main Clinic')}\n"
                response += "\n"
                
                appointment_list.append({
                    "id": apt.id,
                    "doctor_name": apt.doctor_name,
                    "appointment_type": apt.appointment_type,
                    "scheduled_time": apt.scheduled_time.isoformat(),
                    "status": apt.status,
                    "reason": apt.reason,
                    "is_virtual": bool(apt.is_virtual),
                    "duration_minutes": apt.duration_minutes
                })
            
            response += "\n💡 You can cancel or reschedule any appointment by telling me the appointment number."
            
            return response, {
                "action": "list_appointments",
                "appointments": appointment_list,
                "count": len(appointments)
            }
            
        except Exception as e:
            return f"I'm sorry, I encountered an error retrieving your appointments: {str(e)}", {
                "action": "list_appointments",
                "error": str(e),
                "success": False
            }
    
    def cancel_appointment(self, patient_id: int, appointment_id: int, db: Session) -> Tuple[str, Dict]:
        """
        Cancel an appointment.
        Returns confirmation message and status.
        """
        try:
            # Find appointment
            appointment = db.query(Appointment).filter(
                Appointment.id == appointment_id,
                Appointment.patient_id == patient_id
            ).first()
            
            if not appointment:
                return f"I couldn't find appointment #{appointment_id} for your account. Please check the appointment number.", {
                    "action": "cancel_appointment",
                    "success": False,
                    "error": "Appointment not found"
                }
            
            if appointment.status == 'cancelled':
                return f"Appointment #{appointment_id} is already cancelled.", {
                    "action": "cancel_appointment",
                    "success": False,
                    "error": "Already cancelled"
                }
            
            # Cancel the appointment
            old_status = appointment.status
            appointment.status = 'cancelled'
            appointment.updated_at = datetime.utcnow()
            db.commit()
            
            response = f"""❌ **Appointment Cancelled**

Appointment #{appointment.id} has been successfully cancelled.

**Cancelled Appointment Details:**
• Doctor: {appointment.doctor_name}
• Type: {appointment.appointment_type.title()}
• Was scheduled for: {appointment.scheduled_time.strftime('%A, %B %d, %Y at %I:%M %p')}
• Previous status: {old_status.title()}

If you'd like to book a new appointment, just let me know!"""
            
            return response, {
                "action": "cancel_appointment",
                "success": True,
                "appointment_id": appointment.id,
                "cancelled_appointment": {
                    "id": appointment.id,
                    "doctor_name": appointment.doctor_name,
                    "scheduled_time": appointment.scheduled_time.isoformat(),
                    "status": appointment.status
                }
            }
            
        except Exception as e:
            db.rollback()
            return f"I'm sorry, I encountered an error cancelling the appointment: {str(e)}", {
                "action": "cancel_appointment",
                "success": False,
                "error": str(e)
            }
    
    def update_appointment(
        self, 
        patient_id: int, 
        appointment_id: int,
        updates: Dict,
        db: Session
    ) -> Tuple[str, Dict]:
        """
        Update an appointment.
        Returns confirmation message and updated data.
        """
        try:
            # Find appointment
            appointment = db.query(Appointment).filter(
                Appointment.id == appointment_id,
                Appointment.patient_id == patient_id
            ).first()
            
            if not appointment:
                return f"I couldn't find appointment #{appointment_id} for your account.", {
                    "action": "update_appointment",
                    "success": False,
                    "error": "Appointment not found"
                }
            
            if appointment.status == 'cancelled':
                return f"Appointment #{appointment_id} is cancelled. Would you like to book a new one instead?", {
                    "action": "update_appointment",
                    "success": False,
                    "error": "Appointment is cancelled"
                }
            
            # Store old values for confirmation
            old_time = appointment.scheduled_time
            old_notes = appointment.notes
            
            # Update fields
            if 'scheduled_time' in updates:
                appointment.scheduled_time = updates['scheduled_time']
            if 'notes' in updates:
                appointment.notes = updates['notes']
            if 'duration_minutes' in updates:
                appointment.duration_minutes = updates['duration_minutes']
            if 'is_virtual' in updates:
                appointment.is_virtual = int(updates['is_virtual'])
                appointment.location = 'Virtual' if updates['is_virtual'] else 'Main Clinic'
            
            appointment.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(appointment)
            
            response = f"""✅ **Appointment Updated**

Appointment #{appointment.id} has been successfully updated.

**Updated Details:**
• Doctor: {appointment.doctor_name}
• Type: {appointment.appointment_type.title()}
• New Date & Time: {appointment.scheduled_time.strftime('%A, %B %d, %Y at %I:%M %p')}
• Duration: {appointment.duration_minutes} minutes
• Location: {'Virtual' if appointment.is_virtual else appointment.location}
• Status: {appointment.status.title()}

"""
            if old_time != appointment.scheduled_time:
                response += f"📅 Changed from: {old_time.strftime('%A, %B %d, %Y at %I:%M %p')}\n"
            
            response += "\nYou'll receive a reminder 24 hours before your appointment."
            
            return response, {
                "action": "update_appointment",
                "success": True,
                "appointment_id": appointment.id,
                "updated_appointment": {
                    "id": appointment.id,
                    "doctor_name": appointment.doctor_name,
                    "scheduled_time": appointment.scheduled_time.isoformat(),
                    "duration_minutes": appointment.duration_minutes,
                    "is_virtual": bool(appointment.is_virtual),
                    "status": appointment.status
                }
            }
            
        except Exception as e:
            db.rollback()
            return f"I'm sorry, I encountered an error updating the appointment: {str(e)}", {
                "action": "update_appointment",
                "success": False,
                "error": str(e)
            }
    
    async def process_appointment_request(
        self,
        message: str,
        conversation_history: List[Dict],
        patient_id: int,
        db: Session,
        intent: str = None
    ) -> Tuple[str, Optional[Dict]]:
        """
        Process an appointment-related message.
        Returns (AI response, appointment_data)
        """
        # Handle direct operations (list, cancel specific appointment)
        if intent == 'list':
            return self.list_appointments(patient_id, db)
        
        # Check for appointment ID in message for cancel/update operations
        appointment_id_match = re.search(r'#?(\d+)', message)
        
        if intent == 'cancel' and appointment_id_match:
            appointment_id = int(appointment_id_match.group(1))
            return self.cancel_appointment(patient_id, appointment_id, db)
        
        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Extract appointment details if present
            appointment_data = self.extract_appointment_details(ai_response)
            
            # If booking appointment, create it in the database
            if appointment_data and appointment_data.get('action') == 'book_appointment':
                details = appointment_data.get('appointment_details', {})
                
                # Parse the scheduled time
                scheduled_time_str = details.get('scheduled_time')
                if scheduled_time_str:
                    try:
                        scheduled_time = datetime.fromisoformat(scheduled_time_str.replace('Z', '+00:00'))
                        
                        # Create appointment in database
                        appointment = Appointment(
                            patient_id=patient_id,
                            doctor_name=details.get('doctor_name', 'Dr. Sarah Johnson'),
                            appointment_type=details.get('appointment_type', 'consultation'),
                            scheduled_time=scheduled_time,
                            duration_minutes=details.get('duration_minutes', 30),
                            reason=details.get('reason', ''),
                            is_virtual=int(details.get('is_virtual', False)),
                            status='scheduled',
                            location='Main Clinic' if not details.get('is_virtual') else 'Virtual'
                        )
                        
                        db.add(appointment)
                        db.commit()
                        db.refresh(appointment)
                        
                        # Add appointment ID to response data
                        appointment_data['appointment_id'] = appointment.id
                        appointment_data['success'] = True
                        
                        # Clean up the AI response to remove JSON
                        ai_response = re.sub(r'\{[\s\S]*\}', '', ai_response).strip()
                        
                        # Add confirmation message if not present
                        if not ai_response:
                            ai_response = f"""✅ Appointment booked successfully!

📅 **Appointment Details:**
- **Doctor:** {appointment.doctor_name}
- **Type:** {appointment.appointment_type.title()}
- **Date & Time:** {appointment.scheduled_time.strftime('%A, %B %d, %Y at %I:%M %p')}
- **Duration:** {appointment.duration_minutes} minutes
- **Location:** {'Virtual Meeting' if appointment.is_virtual else 'Main Clinic'}
- **Reason:** {appointment.reason}

You'll receive a reminder 24 hours before your appointment. If you need to reschedule or cancel, just let me know!"""
                        
                    except (ValueError, KeyError) as e:
                        appointment_data['success'] = False
                        appointment_data['error'] = str(e)
            
            # If showing available slots
            elif appointment_data and appointment_data.get('action') == 'show_slots':
                slots = self.generate_available_slots()
                appointment_data['slots'] = slots[:10]  # Return top 10 slots
                
                # Format slots in response
                slots_text = "\n\n📅 **Available Appointments:**\n"
                for i, slot in enumerate(slots[:10], 1):
                    slots_text += f"{i}. {slot['formatted']}\n"
                
                ai_response = re.sub(r'\{[\s\S]*\}', '', ai_response).strip()
                if not ai_response:
                    ai_response = "Here are the available appointment slots:"
                ai_response += slots_text
            
            return ai_response, appointment_data
            
        except Exception as e:
            error_message = f"I apologize, but I encountered an error while processing your appointment request: {str(e)}"
            return error_message, {"error": str(e), "success": False}
    
    def format_appointment_confirmation(self, appointment: Appointment) -> str:
        """Format appointment confirmation message"""
        return f"""✅ **Appointment Confirmed!**

📋 **Details:**
- **ID:** #{appointment.id}
- **Doctor:** {appointment.doctor_name}
- **Type:** {appointment.appointment_type.title()}
- **Date & Time:** {appointment.scheduled_time.strftime('%A, %B %d, %Y at %I:%M %p')}
- **Duration:** {appointment.duration_minutes} minutes
- **Location:** {'Virtual Meeting' if appointment.is_virtual else appointment.location}
- **Status:** {appointment.status.title()}

📝 **Reason:** {appointment.reason}

We'll send you a reminder 24 hours before your appointment. See you then!"""

