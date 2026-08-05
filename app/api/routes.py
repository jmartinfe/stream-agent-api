
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.core.exceptions import AppError
from app.core.logging import get_logger
from app.schemas.chat import ChatRequest, ClearSessionRequest
from app.services.agent import clear_all_sessions, response_generator, clear_session

logger = get_logger(__name__)
router = APIRouter(prefix="/stream", tags=["Chat Endpoints"])

@router.post("/send-message", response_class=StreamingResponse)
async def chat_stream(payload: ChatRequest):
    """
    Endpoint to stream responses from the LLM based on user input.
    """
    session_id = payload.session_id or str(uuid4())
    logger.info("Received chat stream request session_id=%s", session_id)

    try:
        # Ensure the system prompt is available
        response_stream = response_generator(
            session_id=session_id, 
            user_message=payload.message
        )
        
        return StreamingResponse(
            response_stream,
            media_type="text/event-stream",
            headers={"X-Session-ID": session_id}
        )
    except AppError:
        raise
    except Exception as e:
        logger.exception("Unexpected error during chat stream for session_id=%s", session_id)
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.delete("/clear-session")
async def clear_chat_session(payload: ClearSessionRequest):
    """
    Endpoint to clear the session history for a given session_id.
    """
    try:
        clear_session(session_id=payload.session_id)
        return {"message": f"Session {payload.session_id} cleared successfully."}
    except AppError:
        raise
    except Exception as e:
        logger.exception("Error clearing session session_id=%s", payload.session_id)
        raise HTTPException(status_code=500, detail=f"Error clearing session: {str(e)}")

@router.delete("/clear-all-sessions")
async def clear_all_chat_sessions():
    """
    Endpoint to clear all session histories.
    """
    logger.info("Clearing all sessions")
    try:
        clear_all_sessions()
        logger.info("All sessions cleared successfully")
        return {"message": "All sessions cleared successfully."}
    except AppError:
        raise
    except Exception as e:
        logger.exception("Error clearing all sessions")
        raise HTTPException(status_code=500, detail=f"Error clearing all sessions: {str(e)}")