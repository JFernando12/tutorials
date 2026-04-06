from fastapi import HTTPException, status

from app.models import Token
from app.security import hash_password, verify_password, create_access_token, DUMMY_HASH

# Mock user store — in a real app, query your database instead
USERS: dict[str, str] = {"alice": hash_password("secret")}


def login(username: str, password: str) -> Token:
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    hashed = USERS.get(username)
    if not hashed:
        verify_password(password, DUMMY_HASH)  # constant-time dummy check
        raise invalid_credentials
    if not verify_password(password, hashed):
        raise invalid_credentials
    return Token(access_token=create_access_token(username), token_type="bearer")
