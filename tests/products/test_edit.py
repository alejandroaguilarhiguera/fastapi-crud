import pytest
from faker import Faker
from jsonschema import validate
from app.models.product import Product
from tests.factories import create_sample_product

fake = Faker()
endpoint = "/products/"

# Schema for a single product (to validate individual responses like PATCH)
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
    return create_sample_product(db_session)

@pytest.mark.anyio
async def test_update_product_success(client, db_session, sample_product):
    """Test successful partial update of a product via PATCH /products/{id}."""
    payload = {
        "name": fake.address(),
        "price": fake.pyfloat(min_value=1, max_value=1000, right_digits=2)
    }

    # Use the dynamic ID from the sample_product fixture
    response = await client.patch(f"{endpoint}{sample_product.id}", json=payload)

    # 1. Verify HTTP status 200 OK
    assert response.status_code == 200
    data = response.json()

    # 2. Validate structure against the JSON Schema
    validate(instance=data, schema=product_schema)

    # 3. Verify response content (updated fields)
    assert data["id"] == sample_product.id
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    # Verify that un-sent fields remain unchanged
    assert data["description"] == sample_product.description

    # 4. Verify actual persistence in the DB
    db_session.expire_all()
    updated_db_product = db_session.query(Product).filter(Product.id == sample_product.id).first()
    assert updated_db_product.name == payload["name"]
    assert float(updated_db_product.price) == payload["price"]


@pytest.mark.anyio
async def test_update_product_not_found(client):
    """Test that updating a non-existent product returns 404 Not Found."""
    payload = {
        "name": "Non Existent",
        "price": 100.0
    }

    response = await client.patch(f"{endpoint}99999", json=payload)

    # Should return 404 Not Found
    assert response.status_code == 404