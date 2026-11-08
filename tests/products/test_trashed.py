import pytest
from faker import Faker
from jsonschema import validate
from app.models.product import Product
from tests.factories import create_sample_product

fake = Faker()
endpoint = "/products/trashed"  # Ajusta esta ruta si en tu router es /products/trash

# Schema for a single product (to validate individual items in the trashed list)
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
    """Fixture that creates an active test product."""
    return create_sample_product(db_session, deleted=False)


@pytest.fixture
def trashed_product(db_session):
    """Fixture that creates a soft-deleted test product."""
    return create_sample_product(db_session, deleted=True)


@pytest.mark.anyio
async def test_get_trashed_products_success(client, db_session, sample_product, trashed_product):
    """Test retrieving all soft-deleted products via GET /products/trashed."""
    response = await client.get(endpoint)

    # 1. Verify HTTP status 200 OK
    assert response.status_code == 200
    products = response.json()

    assert isinstance(products, list)
    assert len(products) >= 1

    # 2. Validate structure against the JSON Schema and ensure they are deleted
    for product in products:
        validate(instance=product, schema=product_schema)
        assert product["deleted_at"] is not None  # Must be trashed

    # 3. Verify our specific trashed product is present, and active product is not
    trashed_ids = [product["id"] for product in products]
    assert trashed_product.id in trashed_ids
    assert sample_product.id not in trashed_ids


@pytest.mark.anyio
async def test_get_trashed_products_empty(client, db_session):
    """Test that getting trashed products returns an empty list when no products are deleted."""
    response = await client.get(endpoint)

    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) == 0