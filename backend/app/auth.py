import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production-use-a-long-random-string")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 300
REFRESH_TOKEN_EXPIRE_SECONDS = 86400  # 24 hours

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# In a real application, users would be stored in a database.
FAKE_USERS_DB: dict[str, dict] = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123"),
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str) -> dict | None:
    user = FAKE_USERS_DB.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_token(data: dict, expires_delta: timedelta, token_type: str = "access") -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(username: str) -> str:
    return create_token(
        {"sub": username},
        timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS),
        token_type="access",
    )


def create_refresh_token(username: str) -> str:
    return create_token(
        {"sub": username},
        timedelta(seconds=REFRESH_TOKEN_EXPIRE_SECONDS),
        token_type="refresh",
    )


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token. Raises JWTError on failure."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
