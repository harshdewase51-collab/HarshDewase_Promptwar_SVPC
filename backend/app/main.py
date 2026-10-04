import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.api.v1.api import api_router
from app.schemas.response import APIResponse
from app.database.session import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("blindspot")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    try:
        init_db()
        logger.info("Database schema initialized successfully")
    except Exception as e:
        logger.warning(f"Database initialization warning (will retry on demand): {e}")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    lifespan=lifespan
)

# CORS setup
origins = [
    settings.FRONTEND_URL,
    "https://harsh-dewase-promptwar-svpc.vercel.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Centralized error handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_msg = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.warning(f"Validation error on {request.url.path}: {error_msg}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=APIResponse.fail(code="VALIDATION_ERROR", message=error_msg).model_dump()
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse.fail(code=f"HTTP_{exc.status_code}", message=str(exc.detail)).model_dump()
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIResponse.fail(
            code="INTERNAL_SERVER_ERROR", 
            message="An unexpected error occurred. Please try again."
        ).model_dump()
    )

# Include v1 API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {"message": "BlindSpot AI API is operational", "docs": f"{settings.API_V1_PREFIX}/docs"}
