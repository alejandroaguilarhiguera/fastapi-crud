import pytest
from app.models.product import Product
from tests.factories import create_sample_product

endpoint = "/products/"


@pytest.fixture
def sample_product(db_session):
    """Fixture that creates an active test product."""
    return create_sample_product(db_session, deleted=False)


@pytest.fixture
def trashed_product(db_session):
    """Fixture that creates a soft-deleted test product."""
    return create_sample_product(db_session, deleted=True)


@pytest.mark.anyio
async def test_destroy_product_not_found(client):
    """1. Not Found: Test that permanently deleting a non-existent product returns 404 Not Found."""
    response = await client.delete(f"{endpoint}99999/destroy")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_destroy_active_product_success(client, db_session, sample_product):
    """2. Destroy product: Test permanent deletion of an active product successfully."""
    product_id = sample_product.id  # Save ID locally before deletion

    response = await client.delete(f"{endpoint}{product_id}/destroy")

    assert response.status_code in [200, 204]

    # Verify that the record is completely removed from the database
    db_session.expire_all()
    db_product = db_session.query(Product).filter(Product.id == product_id).first()
    assert db_product is None


@pytest.mark.anyio
async def test_destroy_soft_deleted_product_success(client, db_session, trashed_product):
    """3. Destroy product deleted: Test permanent deletion of an already soft-deleted product successfully."""
    product_id = trashed_product.id  # Save ID locally before deletion

    response = await client.delete(f"{endpoint}{product_id}/destroy")

    assert response.status_code in [200, 204]

    # Verify that the record is completely removed from the database
    db_session.expire_all()
    db_product = db_session.query(Product).filter(Product.id == product_id).first()
    assert db_product is None