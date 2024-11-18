from typing import Any

import app_logging
from database import init_db
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import auth, users

# Set up the logger
logger = app_logging.setup_logger(__name__)

# FastAPI application instance
app = FastAPI()

# Jinja2 templates for rendering HTML
app.mount("/static", StaticFiles(directory="ui/static"), name="static")
templates = Jinja2Templates(directory="ui/templates")

# Initialize the database
init_db()

# Include routers
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def get_spa(request: Request) -> Any:
    """Serve the main HTML file for the single-page application."""
    return templates.TemplateResponse("index.html", {"request": request})


# This section ensures that Uvicorn runs correctly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)
