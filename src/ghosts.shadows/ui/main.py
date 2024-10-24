from typing import Any, Literal
from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from .auth import login, signup
from .api import query_api
import ui.app_logging as app_logging
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .config import AUTH_URL
import ui.app_logging as app_logging
import os
from datetime import timedelta

# Set up the logger
logger = app_logging.setup_logger(__name__)

# Create a FastAPI app instance
app = FastAPI()
templates = Jinja2Templates(directory="ui/templates")  # Ensure correct relative path
app.mount("/static", StaticFiles(directory="ui/static"), name="static")

# OAuth2PasswordBearer to handle token extraction from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):  # Specify the Request type
    logger.debug("Received a GET request at the root endpoint.")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/auth")
async def handle_auth(username: str = Form(...), password: str = Form(...), auth_type: str = Form(...)) -> dict[str, str] | tuple[Literal['Login successful'], str, Literal[True]] | tuple[str, Literal[False]]:
    logger.info(f"Received auth request: {auth_type} for user: {username}")

    if auth_type == "login":
        result, token, logged_in = login(username, password)
        if not logged_in:
            logger.warning(f"Failed login attempt for user: {username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")
        logger.info(f"Login successful for user: {username}")
        return {"message": result, "access_token": token}
    else:
        signup_result = signup(username, password)
        logger.info(f"Signup successful for user: {username}")
        return signup_result

@app.post("/query")
async def handle_query(
    query_text: str = Form(...), 
    model_choice: str = Form(...), 
    token: str = Depends(oauth2_scheme)  # Use Dependency Injection to get the token
) -> Any | str:
    logger.debug(f"Received query request: {query_text} with model choice: {model_choice}")

    # Verify the token
    try:
        payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        username = payload.get("sub")  # Extract username from the token
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        logger.warning("Token is invalid or expired.")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        response = query_api(query_text, model_choice, token)  # Pass the token to the query_api
        logger.debug(f"Query response: {response}")
        
        # Check if response indicates an error
        if isinstance(response, str) and response.startswith("Error:"):
            logger.warning(f"Query resulted in an error: {response}")
            raise HTTPException(status_code=400, detail=response)

        return response

    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)  # Log the error with stack trace
        raise HTTPException(status_code=500, detail="An error occurred while processing the query.")

# Endpoint for user signup
@app.post("/signup", response_model=Token)
async def signup(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    logger.info(f"Signup attempt for user: {form_data.username}")
    
    user = await get_user(db, form_data.username)
    if user:
        logger.warning(f"User already exists: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists!",
        )
    
    hashed_password = get_password_hash(form_data.password)
    new_user = User(
        username=form_data.username,
        hashed_password=hashed_password,
        full_name="",
        disabled=False,
    )
    
    async with db as session:
        session.add(new_user)
        await session.commit()
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"User created successfully: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer", "message": "Signup successful!"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the FastAPI application.")
    uvicorn.run(app, host="0.0.0.0", port=7860)
