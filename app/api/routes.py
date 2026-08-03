
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest, ClearSessionRequest
from app.services.agent import response_generator, clear_session

router = APIRouter(prefix="/stream", tags=["Chat Endpoints"])

@router.post("/send-message", response_class=StreamingResponse)
async def chat_stream(payload: ChatRequest):
    """
    Endpoint to stream responses from the LLM based on user input.
    """
    session_id = payload.session_id or str(uuid4())

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
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.delete("/clear-session")
async def clear_chat_session(payload: ClearSessionRequest):
    """
    Endpoint to clear the session history for a given session_id.
    """
    try:
        clear_session(session_id=payload.session_id)
        return {"message": f"Session {payload.session_id} cleared successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing session: {str(e)}")