# Stream Agent API (Template)
A lightweight FastAPI template to build AI agents with streaming responses and session history management.

## Features
Real-time response streaming using StreamingResponse.

Server-side session history management by session_id.

Decoupled system prompt loaded from an external file (prompts/system_prompt.txt) ignored by Git.

## Setup
**Clone the repository and navigate into the project directory.**

**Create and activate a virtual environment:**
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**Install dependencies:**
```
pip install -r requirements.txt
```

**Environment Variables:**
Create a `.env` file in the root directory based on the example below:
    ```
    OPENAI_API_KEY=sk-proj-your-actual-api-key
    API_KEY=your-internal-api-key
    ALLOWED_ORIGINS=http://localhost:5500,https://your-frontend.vercel.app
    ENVIRONMENT=development
    LOG_LEVEL=INFO
    APP_TITLE=Stream Agent API
    ```

**Create your system prompt file at data/system_prompt.txt with your agent instructions.**

## Running the Application
Start the development server with Uvicorn:
uvicorn main:app --reload

Access the interactive API documentation at http://127.0.0.1:8000/docs

## API Endpoints
**Send Message (Streaming)**
Sends a message within a specific session and streams the generated response.

Method: POST

Endpoint: /stream/send-message

Headers: Content-Type: application/json

Request Body:
{
"session_id": "string",
"message": "string"
}

Response: StreamingResponse (text/event-stream)

**Clear Session**
Deletes the stored conversation history for a given session.

Method: DELETE

Endpoint: /stream/clear-session

Headers: Content-Type: application/json

Request Body:
"string"

Response:
{
"message": "Session {session_id} cleared successfully."
}

## License
MIT