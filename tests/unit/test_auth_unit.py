from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.routers.auth import login, LoginRequest


def test_login_success():

    # Fake user
    user = MagicMock()
    user.id = 1
    user.username = "customer_test"
    user.password_hash = "fake-hashed-password"
    user.role = "CUSTOMER"
    user.is_active = True

    # Fake DB
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = user

    login_data = LoginRequest(
        username="customer_test",
        password="Password@123"
    )

    with patch(
        "app.routers.auth.verify_password",
        return_value=True
    ), patch(
        "app.routers.auth.create_access_token",
        return_value="fake-jwt-token"
    ):

        result = login(login_data, db)

    assert result["access_token"] == "fake-jwt-token"
    assert result["token_type"] == "bearer"
    assert result["user"]["id"] == 1
    assert result["user"]["username"] == "customer_test"
    assert result["user"]["role"] == "CUSTOMER"

def test_login_user_not_found():

    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    login_data = LoginRequest(
        username="unknown",
        password="Password@123"
    )

    with pytest.raises(HTTPException) as exc:

        login(login_data, db)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid username or password"

def test_login_wrong_password():

    user = MagicMock()
    user.password_hash = "fake-hash"
    user.is_active = True

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = user

    login_data = LoginRequest(
        username="customer_test",
        password="WrongPassword"
    )

    with patch(
        "app.routers.auth.verify_password",
        return_value=False
    ):

        with pytest.raises(HTTPException) as exc:

            login(login_data, db)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid username or password"

def test_login_wrong_password():

    user = MagicMock()
    user.password_hash = "fake-hash"
    user.is_active = True

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = user

    login_data = LoginRequest(
        username="customer_test",
        password="WrongPassword"
    )

    with patch(
        "app.routers.auth.verify_password",
        return_value=False
    ):

        with pytest.raises(HTTPException) as exc:

            login(login_data, db)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid username or password"