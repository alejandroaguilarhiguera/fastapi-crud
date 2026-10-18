import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.routes import api_router
from app.utils.exceptions import global_exception_handler

app = FastAPI(
    title="FastAPI CRUD",
    version="1.0.0",
)
@app.get("/")
def root():
    return {"message": "Welcome fastapi-crud API"}

# Incluir todas las rutas desde el router centralizado
app.include_router(api_router)

# Exception handlers
app.add_exception_handler(Exception, global_exception_handler)