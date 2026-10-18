
from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Retrieve all active products."""
        return (
            self.db.query(Product)
            .filter(Product.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(
        self,
        id: int,
        include_deleted: bool = False,
    ) -> Product:
        """Retrieve a product by ID, optionally including deleted products."""
        query = self.db.query(Product).filter(
            Product.id == id
        )

        if not include_deleted:
            query = query.filter(Product.deleted_at.is_(None))

        product = query.first()

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return product

    def create(self, id: ProductCreate) -> Product:
        """Create a new product."""
        product = Product(**id.model_dump())

        try:
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            return product

        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A product with this name already exists",
            ) from e

    def update(
        self,
        id: int,
        product: ProductUpdate,
    ) -> Product:
        """Update an active product."""
        product = self.get_by_id(id)

        update_product = product.model_dump(exclude_unset=True)

        for key, value in update_product.items():
            setattr(product, key, value)

        try:
            self.db.commit()
            self.db.refresh(product)
            return product

        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A product with this name already exists",
            ) from e

    def delete(self, id: int) -> Product:
        """Move an active product to the trash (soft delete)."""
        product = self.get_by_id(id)

        product.deleted_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(product)
        return product

    def get_trashed(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Product]:
        """Retrieve all soft-deleted products."""
        return (
            self.db.query(Product)
            .filter(Product.deleted_at.isnot(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def restore(self, id: int) -> Product:
        """Restore a soft-deleted product."""
        product = self.get_by_id(
            id,
            include_deleted=True,
        )

        if product.deleted_at is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product is already active",
            )

        product.deleted_at = None

        try:
            self.db.commit()
            self.db.refresh(product)
            return product

        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot restore the product because its name may already exist",
            ) from e

    def destroy(self, product_id: int) -> None:
        """Permanently delete a product from the database."""
        product = self.get_by_id(
            product_id,
            include_deleted=True,
        )

        self.db.delete(product)
        self.db.commit()
