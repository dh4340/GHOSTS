from jose import jwt, JWTError
from fastapi import Header, HTTPException
from config.config import SECRET_KEY, ALGORITHM
import logging

logger = logging.getLogger(__name__)


async def decode_jwt(token: str = Header(None)):
    if token and token.startswith("Bearer "):
        token = token.split("Bearer ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if not username:
                raise ValueError("Invalid token payload")
            return username
        except JWTError:
            logger.error("JWT Error")
            raise HTTPException(status_code=401, detail="Invalid token")
    raise HTTPException(status_code=401, detail="No token provided")
