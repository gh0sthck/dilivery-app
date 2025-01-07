import datetime
from fastapi import HTTPException
import jwt
import bcrypt

from app.auth.schemas import JWTPayload
from app.settings import config


def encode_jwt(
    payload: JWTPayload,
    private_key: str = config.auth.private_key_path.read_text(),
    algorithm: str = config.auth.algorithm
) -> bytes:
    return jwt.encode(
        payload=payload.model_dump(),
        key=private_key,
        algorithm=algorithm
    ).encode()


def decode_jwt(
    jwt_token: bytes,
    public_key: str = config.auth.public_key_path.read_text(),
    algorithm: str = config.auth.algorithm
) -> dict:
    try:
        decoded: dict = jwt.decode(jwt=jwt_token, key=public_key, algorithms=[algorithm])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token not valid")
    # if not decoded.get("exp") or int(decoded.get("expire")) < datetime.datetime.now().timestamp():
        # raise HTTPException(status_code=401, detail="Token expired") 
    return decoded


def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password.encode(), salt=salt)


def validate_password(password: str, hash: bytes):
    return bcrypt.checkpw(password=password.encode(), hashed_password=hash)
