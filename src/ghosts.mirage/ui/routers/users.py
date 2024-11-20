# routers/users.py
from config import ALGORITHM, SECRET_KEY
from crud import get_user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from security import oauth2_scheme
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/users/me")
async def read_users_me(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> dict:
    """Get the current user's information using the JWT token."""
    try:
        # Decode the token to extract the username
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        # Retrieve the user from the database
        user = get_user(db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return {"username": username}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
