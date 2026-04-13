from fastapi import APIRouter

from app.models import LoginRequest, Token
from app.security import CurrentUserDep
from app.services import login

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token)
async def login_route(body: LoginRequest):
    return login(body.username, body.password)


@router.get("/me")
async def read_me(current_user: CurrentUserDep):
    return {"username": current_user}
