import pytest
from faker import Faker
from app.models.product import Product
from tests.factories import create_sample_product

fake = Faker()

endpoint = "/products/"

@pytest.fixture
def sample_product(db_session):
    return create_sample_product(db_session)

@pytest.mark.anyio
async def test_soft_delete_product_success(client, db_session, sample_product):
    """Test successful soft delete of a product via DELETE /products/{id}."""
    # Use the dynamic ID from the sample_product fixture
    response = await client.delete(f"{endpoint}{sample_product.id}")

    # 1. Verify HTTP status (200 OK)
    assert response.status_code is 200

    # 2. Verify actual persistence in the DB: check that deleted_at is set (Soft Delete)
    db_session.expire_all()
    deleted_db_product = db_session.query(Product).filter(Product.id == sample_product.id).first()
    
    assert deleted_db_product is not None  # It still exists in the database
    assert deleted_db_product.deleted_at is not None  # But deleted_at is populated


@pytest.mark.anyio
async def test_soft_delete_product_not_found(client):
    """Test that deleting a non-existent product returns 404 Not Found."""
    response = await client.delete(f"{endpoint}99999")

    # Should return 404 Not Found
    assert response.status_code == 404