"""Chat endpoints for AI assistant"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from openai import OpenAI
import uuid

from app.core.config import settings
from app.core.security import get_current_user
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.db.session import get_db
from app.models.chat_conversation import ChatConversation
from app.models.chat_message import ChatMessage

router = APIRouter()

# System prompt for medical assistant
SYSTEM_PROMPT = """You are a helpful and empathetic medical assistant for Carely, a healthcare platform. 
Your role is to:
- Provide clear, accurate, and empathetic responses to healthcare-related questions
- Help users understand medical information in accessible terms
- Guide users on when to seek professional medical care
- Never provide diagnoses or replace professional medical advice
- Always remind users to consult with healthcare professionals for serious medical concerns, diagnoses, or treatment decisions
- Be supportive, understanding, and maintain patient confidentiality
- If asked about medications, symptoms, or treatments, emphasize the importance of consulting healthcare providers

Remember: You are an assistant that provides information and guidance, but not medical diagnoses or treatment prescriptions."""

# Initialize OpenAI client
openai_client = None
if settings.OPENAI_API_KEY:
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)


@router.post("/", response_model=ChatMessageResponse, status_code=status.HTTP_200_OK)
async def chat(
    request: ChatMessageRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process user message and return AI assistant response with conversation history.
    
    - **message**: The user's message to process
    - **conversation_id**: Optional conversation ID to continue an existing conversation
    - Requires authentication via Bearer token
    
    If conversation_id is not provided, a new conversation will be created.
    """
    # Check if OpenAI is configured
    if not openai_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API is not configured. Please set OPENAI_API_KEY in environment variables."
        )
    
    # Parse and validate user message
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    try:
        patient_id = int(current_user["id"])
        
        # Get or create conversation
        conversation = None
        if request.conversation_id:
            # Try to find existing conversation
            conversation = db.query(ChatConversation).filter(
                ChatConversation.conversation_id == request.conversation_id,
                ChatConversation.patient_id == patient_id
            ).first()
            
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or access denied"
                )
        else:
            # Create new conversation
            conversation = ChatConversation(
                conversation_id=str(uuid.uuid4()),
                patient_id=patient_id
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Retrieve conversation history (ordered by creation time)
        history_messages = db.query(ChatMessage).filter(
            ChatMessage.conversation_id == conversation.conversation_id
        ).order_by(ChatMessage.created_at.asc()).all()
        
        # Build messages array with system prompt, history, and current message
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history
        for msg in history_messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API using responses.create
        response = openai_client.responses.create(
            model="gpt-5-mini",  # or another available model
            input=messages
        )
        
        # Extract the response text
        ai_response = response.output_text.strip()
        
        # Generate message IDs for tracking
        user_message_id = str(uuid.uuid4())
        assistant_message_id = str(uuid.uuid4())
        
        # Store user message in database
        db_user_message = ChatMessage(
            conversation_id=conversation.conversation_id,
            role="user",
            content=user_message,
            message_id=user_message_id
        )
        db.add(db_user_message)
        
        # Store assistant response in database
        db_assistant_message = ChatMessage(
            conversation_id=conversation.conversation_id,
            role="assistant",
            content=ai_response,
            message_id=assistant_message_id
        )
        db.add(db_assistant_message)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        
        db.commit()
        
        return ChatMessageResponse(
            response=ai_response,
            message_id=assistant_message_id,
            conversation_id=conversation.conversation_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )

