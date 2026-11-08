import pytest
from faker import Faker
from jsonschema import validate
from app.models.product import Product

fake = Faker()

endpoint = "/products/"

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


@pytest.mark.anyio
async def test_create_product_success(client, db_session):
    """Test successful product creation via POST /products/."""
    payload = {
        "name": fake.word(),
        "description": fake.sentence(),
        "price": fake.pyfloat(min_value=1, max_value=500, right_digits=2)
    }

    response = await client.post(endpoint, json=payload)

    # 1. Verify HTTP status 201 Created
    assert response.status_code == 201
    data = response.json()

    # 2. Validate structure against the JSON Schema
    validate(instance=data, schema=product_schema)

    # 3. Validate response content
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]
    assert data["id"] is not None

    # 4. Verify actual persistence in the DB
    db_product = db_session.query(Product).filter(Product.id == data["id"]).first()
    assert db_product is not None
    assert db_product.name == payload["name"]


@pytest.mark.anyio
async def test_create_product_invalid_price(client):
    """Test validation failure when price is less than or equal to 0."""
    payload = {
        "name": fake.word(),
        "description": fake.sentence(),
        "price": -10.0  # forbidden price
    }

    response = await client.post(endpoint, json=payload)
    assert response.status_code == 422

@pytest.mark.anyio
async def test_create_product_only_name_fails(client):
    """Test that the API rejects creation with 422 if only the 'name' field is sent and price is missing."""
    payload = {
        "name": fake.word()
    }

    response = await client.post(endpoint, json=payload)

    assert response.status_code == 422
