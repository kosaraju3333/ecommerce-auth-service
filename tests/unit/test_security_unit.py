from app.utils.security import hash_password, verify_password


def test_hash_password_returns_different_value():
    password = "Password@123"

    hashed = hash_password(password)

    assert hashed != password


def test_hash_password_returns_string():
    hashed = hash_password("Password@123")

    assert isinstance(hashed, str)
    assert len(hashed) > 0


def test_verify_password_with_correct_password():
    password = "Password@123"
    hashed = hash_password(password)

    result = verify_password(password, hashed)

    assert result is True


def test_verify_password_with_wrong_password():
    hashed = hash_password("Password@123")

    result = verify_password("WrongPassword", hashed)

    assert result is False