# Step 1: Import dependencies
import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pydantic import BaseModel

load_dotenv()

# Step 2: Configure JWT settings and create the app
SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

app = FastAPI()

# Step 3: Set up password hashing
password_hash = PasswordHash.recommended()

def hash_password(plain: str) -> str:
    return password_hash.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)

# Step 4: Create and decode access tokens
def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(
        {
            "sub": username,
            "exp": expire
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if username is None:
        raise InvalidTokenError()
    return username

# Step 5: Build the get_current_user dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        return decode_access_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
        )

# Step 6: POST /token — login and get a token
# Mock user store, query your database instead
USERS = {"alice": hash_password("secret")}

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/token", response_model=Token)
async def login(body: LoginRequest):
    hashed = USERS.get(body.username)
    
    if not hashed or not verify_password(body.password, hashed):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
        
    return Token(
        access_token=create_access_token(body.username),
        token_type="bearer"
    )

# Step 7: GET /me — protected route
@app.get("/me")
async def read_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
