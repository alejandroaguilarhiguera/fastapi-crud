# FastAPI Product Management API

run migration
alembic upgrade head


A robust, modern, and asynchronous RESTful API built with **FastAPI**, **SQLAlchemy**, and **Pydantic V2**, featuring a complete product lifecycle management system including **Soft Delete**, **Trash Management**, **Restoration**, and **Permanent Deletion (Hard Delete)**.

---

## 🚀 Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Async web framework)
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) (Database management)
* **Validation:** [Pydantic V2](https://docs.pydantic.dev/) & [jsonschema](https://python-jsonschema.readthedocs.io/)
* **Testing:** [Pytest](https://docs.pytest.org/) with `anyio` for async support
* **Mock Data:** [Faker](https://faker.readthedocs.io/)

---

## 📁 Project Structure

```text
app/
├── models/
│   └── product.py         # SQLAlchemy Product model (with deleted_at)
├── schemas/
│   └── product.py         # Pydantic validation schemas (Create, Update, Response)
├── services/
│   └── product.py         # Business logic & database operations
└── routers/
    └── product.py         # API Endpoints (CRUD, Soft Delete, Get Trashed, Restore, Destroy)

tests/
├── factories.py           # Reusable data factories for testing under demand
├── conftest.py            # Global test fixtures (DB session, async client)
└── products/
    ├── test_create.py     # Tests for product creation
    ├── test_edit.py       # Tests for partial updates (PATCH)
    ├── test_delete.py     # Tests for soft deletion (DELETE)
    ├── test_trashed.py    # Tests for listing trashed products (GET /trashed)
    ├── test_restore.py    # Tests for restoring deleted products (POST /restore)
    └── test_destroy.py    # Tests for permanent deletion (DELETE /destroy)