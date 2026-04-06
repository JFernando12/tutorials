from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.config import env

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy")  # used to prevent timing attacks

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=env.EXPIRE_MINUTES)
    return jwt.encode({"sub": username, "exp": expire}, env.JWT_SECRET, algorithm=env.ALGORITHM)


def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, env.JWT_SECRET, algorithms=[env.ALGORITHM])
    username = payload.get("sub")
    if username is None:
        raise InvalidTokenError()
    return username


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        return decode_access_token(token)
    except InvalidTokenError:
        raise credentials_exception


CurrentUserDep = Annotated[str, Depends(get_current_user)]
