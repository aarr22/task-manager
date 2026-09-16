from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies import get_current_user
from app.dtos.requests import UserCreateRequest
from app.dtos.responses import TokenResponse, UserResponse
from app.models import User
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a regular user account. Any 'role' sent in the body is ignored — "
    "every account starts as role=user. Admins are created only via create_admin.py.",
)
def register(payload: UserCreateRequest, session: Session = Depends(get_session)):
    existing = session.exec(
        select(User).where(
            (User.username == payload.username) | (User.email == payload.email)
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already taken")

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in and get an access token",
    description="OAuth2 password flow — send username/password as form data, not JSON. "
    "Use the returned token with the Authorize button in /docs.",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Account is disabled")

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse, summary="Get the logged-in user")
def me(current_user: User = Depends(get_current_user)):
    return current_user
