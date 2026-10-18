from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)

@router.get("/", response_model=List[ProductResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    service: ProductService = Depends(get_product_service),
):
    return service.get_all(skip=skip, limit=limit)

@router.get("/trashed", response_model=List[ProductResponse])
def trashed(
    skip: int = 0,
    limit: int = 100,
    service: ProductService = Depends(get_product_service),
):
    return service.get_trashed(skip=skip, limit=limit)

@router.get("/{id}", response_model=ProductResponse)
def show(id: int, service: ProductService = Depends(get_product_service)):
    return service.get_by_id(id)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add(
    product_in: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return service.create(product_in)

@router.patch("/{id}", response_model=ProductResponse)
def edit(
    id: int,
    product: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    return service.update(id, product)


@router.delete("/{id}")
def delete(id: int, service: ProductService = Depends(get_product_service)):
    service.delete(id)
    return {"message": "Product deleted"}

@router.put("/{id}/restore")
def restore(id: int, service: ProductService = Depends(get_product_service)):
    product = service.restore(id)
    return {"message": "Product restored", "product": product}

@router.delete(
    "/{id}/destroy",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def destroy(
    id: int,
    service: ProductService = Depends(get_product_service),
) -> Response:
    service.destroy(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)