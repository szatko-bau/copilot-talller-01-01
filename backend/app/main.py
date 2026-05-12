from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel

from app.auth import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    FAKE_USERS_DB,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
)

app = FastAPI(
    title="JWT Authentication API",
    description="FastAPI application demonstrating JWT authentication with access and refresh tokens.",
    version="0.1.0",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class UserInfo(BaseModel):
    username: str


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise credentials_exception
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = FAKE_USERS_DB.get(username)
    if user is None:
        raise credentials_exception
    return user


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.post("/token", response_model=Token, summary="Login and obtain JWT tokens")
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Authenticate with **username** and **password** and receive a pair of
    JWT tokens (access + refresh).

    - Default credentials: `admin` / `admin123`
    - Access token expires in **300 seconds**.
    - Refresh token expires in **24 hours**.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(
        access_token=create_access_token(user["username"]),
        refresh_token=create_refresh_token(user["username"]),
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.post("/token/refresh", response_model=Token, summary="Refresh JWT tokens")
def refresh_token(body: RefreshRequest) -> Token:
    """
    Exchange a valid **refresh token** for a new pair of access + refresh tokens.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise credentials_exception
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = FAKE_USERS_DB.get(username)
    if user is None:
        raise credentials_exception

    return Token(
        access_token=create_access_token(user["username"]),
        refresh_token=create_refresh_token(user["username"]),
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.get("/me", response_model=UserInfo, summary="Get current user info")
def read_current_user(current_user: dict = Depends(get_current_user)) -> UserInfo:
    """
    Returns information about the currently authenticated user.
    Requires a valid **access token** in the `Authorization: Bearer <token>` header.
    """
    return UserInfo(username=current_user["username"])
