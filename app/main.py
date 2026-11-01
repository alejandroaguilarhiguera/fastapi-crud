from fastapi import FastAPI
from app.routes import api_router
from app.utils.exceptions import global_exception_handler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI CRUD",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome fastapi-crud API"}

# Incluir todas las rutas desde el router centralizado
app.include_router(api_router)

# Exception handlers
app.add_exception_handler(Exception, global_exception_handler)