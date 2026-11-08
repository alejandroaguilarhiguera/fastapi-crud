# tests/factories.py
from faker import Faker
from app.models.product import Product
from datetime import datetime, timezone

fake = Faker()

def create_sample_product(db_session, deleted: bool = False):
    product = Product(
        name=fake.word(),
        description=fake.sentence(),
        price=fake.pyfloat(min_value=1, max_value=1000, right_digits=2),
        deleted_at=datetime.now(timezone.utc) if deleted else None
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product