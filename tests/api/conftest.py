import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.utils.security import hash_password


TEST_DATABASE_URL = "sqlite://"


engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture()
def db():

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db):

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def admin_user(db):

    user = User(
        username="admin_test",
        email="admin@test.com",
        password_hash=hash_password("Admin@123"),
        role="ADMIN",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture()
def customer_user(db):

    user = User(
        username="customer_test",
        email="customer@test.com",
        password_hash=hash_password("Customer@123"),
        role="CUSTOMER",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture()
def inactive_user(db):

    user = User(
        username="inactive_test",
        email="inactive@test.com",
        password_hash=hash_password("Inactive@123"),
        role="CUSTOMER",
        is_active=False,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user