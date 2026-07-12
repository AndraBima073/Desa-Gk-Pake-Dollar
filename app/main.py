"""Entry point aplikasi FastAPI (API-only, siap dikonsumsi frontend JS)."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.core.database import init_db
from app.routers import ai, dashboard, user

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Membuat tabel saat startup (dev). Gunakan Alembic untuk produksi."""
    await init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS agar frontend (Fetch/Axios) dapat mengakses API dari origin berbeda.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Exception handlers: memastikan SELURUH error tetap ber-format konsisten ===
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc: StarletteHTTPException):
    """Membungkus HTTPException ke envelope {status, message, data}."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": str(exc.detail), "data": None},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    """Error validasi Pydantic dikembalikan dengan format seragam."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Validasi payload gagal.",
            "data": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, __: Exception):
    """Fallback 500 — tidak membocorkan detail internal ke klien."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error", "message": "Internal server error.", "data": None},
    )


# === Registrasi router modular ===
app.include_router(user.router, prefix=settings.API_V1_PREFIX)
app.include_router(ai.router, prefix=settings.API_V1_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["System"])
async def health_check():
    """Endpoint liveness sederhana untuk monitoring/load balancer."""
    return {"status": "success", "message": "healthy", "data": None}
