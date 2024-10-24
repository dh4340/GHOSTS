from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import app_logging
from routes import activity, chat, content, lessons, social
import os

# Initialize logging
logger = app_logging.setup_logger(__name__)

# FastAPI app
app = FastAPI()

# Include routes from different modules
app.include_router(activity.router, prefix="/activity")
app.include_router(chat.router, prefix="/chat")
app.include_router(content.router, prefix="/content")
app.include_router(lessons.router, prefix="/lessons")
app.include_router(social.router, prefix="/social")

# Serve static files from the 'assets' directory
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
async def root():
    return {"message": "Welcome to the GHOSTS SHADOWS API"}


if __name__ == "__main__":
    import uvicorn

    logger.info("""

            ('-. .-.               .-')    .-') _     .-')    
            ( OO )  /              ( OO ). (  OO) )   ( OO ).  
  ,----.    ,--. ,--. .-'),-----. (_)---\_)/     '._ (_)---\_) 
 '  .-./-') |  | |  |( OO'  .-.  '/    _ | |'--...__)/    _ |  
 |  |_( O- )|   .|  |/   |  | |  |\  :` `. '--.  .--'\  :` `.  
 |  | .--, \|       |\_) |  |\|  | '..`''.)   |  |    '..`''.) 
(|  | '. (_/|  .-.  |  \ |  | |  |.-._)   \   |  |   .-._)   \ 
 |  '--'  | |  | |  |   `'  '-'  '\       /   |  |   \       / 
  `------'  `--' `--'     `-----'  `-----'    `--'    `-----'  

""")
    logger.info("GHOSTS SHADOWS coming online...")

    ollama_host = os.getenv("GHOSTS_OLLAMA_URL", "http://localhost:11434")
    uvicorn.run("main:app", host="0.0.0.0", port=5900, reload=True)
