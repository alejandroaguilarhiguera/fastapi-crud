import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger("uvicorn.error")

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no controlado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Error interno del servidor. Por favor, intente más tarde."
        },
    )