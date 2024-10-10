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
):
    return jwt.decode(jwt=jwt_token, key=public_key, algorithms=[algorithm])


def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password.encode(), salt=salt)


def validate_password(password: str, hash: bytes):
    return bcrypt.checkpw(password=password.encode(), hashed_password=hash)
