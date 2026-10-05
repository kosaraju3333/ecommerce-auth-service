from jose import jwt

from app.config import settings


# --------------------------------------------------
# ROOT / HEALTH
# --------------------------------------------------

def test_root(client):

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "service": "auth-service",
        "status": "running",
    }


def test_health(client):

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "UP"


# --------------------------------------------------
# REGISTRATION
# --------------------------------------------------

def test_register_customer_success(client):

    response = client.post(
        "/api/auth/register",
        json={
            "username": "newcustomer",
            "email": "newcustomer@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "User registered successfully"

    assert data["user"]["username"] == "newcustomer"
    assert data["user"]["email"] == "newcustomer@test.com"

    # Registration must always create CUSTOMER
    assert data["user"]["role"] == "CUSTOMER"

    # Password must never be returned
    assert "password" not in data["user"]
    assert "password_hash" not in data["user"]


def test_register_duplicate_username(client, customer_user):

    response = client.post(
        "/api/auth/register",
        json={
            "username": "customer_test",
            "email": "different@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 409

    assert response.json()["detail"] == "Username already exists"


def test_register_duplicate_email(client, customer_user):

    response = client.post(
        "/api/auth/register",
        json={
            "username": "differentuser",
            "email": "customer@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 409

    assert response.json()["detail"] == "Email already exists"


def test_register_missing_username(client):

    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422


# --------------------------------------------------
# ADMIN LOGIN
# --------------------------------------------------

def test_admin_login_success(client, admin_user):

    response = client.post(
        "/api/auth/login",
        json={
            "username": "admin_test",
            "password": "Admin@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    assert data["user"]["username"] == "admin_test"
    assert data["user"]["role"] == "ADMIN"


# --------------------------------------------------
# CUSTOMER LOGIN
# --------------------------------------------------

def test_customer_login_success(client, customer_user):

    response = client.post(
        "/api/auth/login",
        json={
            "username": "customer_test",
            "password": "Customer@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    assert data["user"]["username"] == "customer_test"
    assert data["user"]["role"] == "CUSTOMER"


# --------------------------------------------------
# INVALID LOGIN
# --------------------------------------------------

def test_wrong_password(client, customer_user):

    response = client.post(
        "/api/auth/login",
        json={
            "username": "customer_test",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401

    assert (
        response.json()["detail"]
        == "Invalid username or password"
    )


def test_nonexistent_user(client):

    response = client.post(
        "/api/auth/login",
        json={
            "username": "does_not_exist",
            "password": "Password@123",
        },
    )

    assert response.status_code == 401

    assert (
        response.json()["detail"]
        == "Invalid username or password"
    )


# --------------------------------------------------
# INACTIVE USER
# --------------------------------------------------

def test_inactive_user_cannot_login(client, inactive_user):

    response = client.post(
        "/api/auth/login",
        json={
            "username": "inactive_test",
            "password": "Inactive@123",
        },
    )

    assert response.status_code == 403

    assert response.json()["detail"] == "User account is inactive"


# --------------------------------------------------
# REQUEST VALIDATION
# --------------------------------------------------

def test_login_without_password(client):

    response = client.post(
        "/api/auth/login",
        json={
            "username": "customer_test"
        },
    )

    assert response.status_code == 422


def test_login_without_username(client):

    response = client.post(
        "/api/auth/login",
        json={
            "password": "Password@123"
        },
    )

    assert response.status_code == 422


# --------------------------------------------------
# JWT VALIDATION
# --------------------------------------------------

def test_login_token_contains_correct_claims(
    client,
    customer_user,
):

    response = client.post(
        "/api/auth/login",
        json={
            "username": "customer_test",
            "password": "Customer@123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert payload["sub"] == str(customer_user.id)
    assert payload["username"] == "customer_test"
    assert payload["role"] == "CUSTOMER"

    assert "exp" in payload