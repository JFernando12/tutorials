from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models import Token
from app.security import CurrentUserDep
from app.services import login

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token)
async def login_route(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return login(form.username, form.password)


@router.get("/me")
async def read_me(current_user: CurrentUserDep):
    return {"username": current_user}
