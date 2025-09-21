# main.py - App Engine entry point
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

logger.info("Starting Youth Portal...")

try:
    from youth_portal_client import app
    logger.info("Successfully imported youth_portal_client")
except ImportError as e:
    logger.error(f"Failed to import youth_portal_client: {e}")
    # Create fallback app
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"status": "Youth Portal - Import Error", "error": str(e)}
    
    @app.get("/_ah/warmup")
    async def warmup():
        return {"status": "ok"}

# Health check endpoint for App Engine
@app.get("/_ah/warmup")
async def warmup():
    logger.info("Warmup request received")
    return {"status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
