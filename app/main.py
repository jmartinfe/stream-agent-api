import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import router as innie_router
from app.core.exceptions import AppError
from app.core.logging import init_logging, get_logger
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
init_logging()
logger = get_logger(__name__)

app = FastAPI(title=os.getenv("APP_TITLE", "Stream Agent API"))

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    logger.error("AppError handled: %s", exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.on_event("startup")
async def on_startup():
    logger.info("Stream Agent API startup complete")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Stream Agent API shutdown")

# Set up CORS middleware
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
origins = [origin.strip() for origin in allowed_origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the tracker router
app.include_router(innie_router)