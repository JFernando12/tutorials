# Step 1: Import dependencies
from datetime import datetime, timedelta, timezone
from typing import Annotated
import os

from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel

load_dotenv()

# Step 2: Configure JWT settings and create the app
SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30
app = FastAPI()

# Step 3: Set up password hashing (Argon2 — stronger than bcrypt)
password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy")  # used to prevent timing attacks

def hash_password(plain: str) -> str:
    return password_hash.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)

# Step 4: Create and decode access tokens
def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if username is None:
        raise InvalidTokenError()
    return username

# Step 5: Build the get_current_user dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

# Step 6: POST /token — login and get a token
# Mock user store — in a real app, query your database instead
USERS = {"alice": hash_password("secret")}

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/token", response_model=Token)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    hashed = USERS.get(form.username)
    if not hashed:
        verify_password(form.password, DUMMY_HASH)  # constant-time dummy check
        raise invalid_credentials
    if not verify_password(form.password, hashed):
        raise invalid_credentials
    return Token(access_token=create_access_token(form.username), token_type="bearer")

# Step 7: GET /me — protected route
@app.get("/me")
async def read_me(current_user: Annotated[str, Depends(get_current_user)]):
    return {"username": current_user}
