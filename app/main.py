from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.logger import logger
from app.routers import producer

app = FastAPI(
    title="Rural Producer API",
    description="API para gerenciamento de produtores rurais",
    version="1.0.0",
)

app.include_router(producer.router, prefix="/api/v1")


@app.get("/")
def read_root() -> dict:
    return {"message": "Rural Producer API", "version": "1.0.0", "status": "running"}


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.exception(f"Unhandled error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Completed request with status {response.status_code}")
    return response
