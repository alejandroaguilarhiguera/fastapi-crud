import pytest
from faker import Faker
from jsonschema import validate
from tests.factories import create_sample_product

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


@pytest.fixture
def sample_product(db_session):
    return create_sample_product(db_session)


@pytest.mark.anyio
async def test_get_products(client, sample_product):
    """test endpoint GET /products/"""
    
    response = await client.get(endpoint)
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 1
    for item in data:
        validate(instance=item, schema=product_schema)

    assert data[0]["id"] == sample_product.id
    assert data[0]["name"] == sample_product.name
    assert data[0]["description"] == sample_product.description
    assert data[0]["price"] == float(sample_product.price)