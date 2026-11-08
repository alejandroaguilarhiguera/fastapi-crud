import pytest
from faker import Faker
from jsonschema import validate
from app.models.product import Product
from tests.factories import create_sample_product

fake = Faker()
endpoint = "/products/"

# Schema for a single product (to validate individual responses)
product_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "description": {"type": ["string", "null"]},
        "price": {"type": "number"},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "deleted_at": {"type": ["string", "null"]}
    },
    "required": ["id", "name", "description", "price", "created_at", "updated_at", "deleted_at"]
}


@pytest.fixture
def sample_product(db_session):
    return create_sample_product(db_session, deleted=False)


@pytest.fixture
def trashed_product(db_session):
    return create_sample_product(db_session, deleted=True)


@pytest.mark.anyio
async def test_restore_product_success(client, db_session, trashed_product):
    """Test successful restoration of a soft-deleted product via PUT /products/{id}/restore."""
    # 1. Verify that the product starts as deleted
    assert trashed_product.deleted_at is not None

    # 2. Request the restoration
    response = await client.put(f"{endpoint}{trashed_product.id}/restore")

    # 3. Verify HTTP status 200 OK
    assert response.status_code == 200
    data = response.json()
    assert data["message"] is not None
    # 4. Validate structure against the JSON Schema
    validate(instance=data["product"], schema=product_schema)

    # 5. Verify that deleted_at is now null in the response and database
    assert data["product"]["deleted_at"] is None

    db_session.expire_all()
    restored_db_product = db_session.query(Product).filter(Product.id == trashed_product.id).first()
    assert restored_db_product.deleted_at is None


@pytest.mark.anyio
async def test_restore_product_not_found(client):
    """Test that restoring a non-existent product returns 404 Not Found."""
    response = await client.put(f"{endpoint}99999/restore")

    # Should return 404 Not Found
    assert response.status_code == 404


@pytest.mark.anyio
async def test_restore_product_already_active_fails(client, db_session, sample_product):
    """Test that restoring an already active (non-deleted) product returns a conflict status (409)."""
    response = await client.put(f"{endpoint}{sample_product.id}/restore")

    # Should return 409 Conflict because the product is not deleted
    assert response.status_code == 409