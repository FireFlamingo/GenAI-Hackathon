# main.py - Parent Portal App Engine entry point
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

logger.info("Starting Parent Portal...")

try:
    # Try to import from frontend folder
    from frontend.parent_portal_client import app
    logger.info("Successfully imported parent_portal_client from frontend")
except ImportError as e:
    logger.error(f"Failed to import from frontend: {e}")
    try:
        # Try direct import
        from parent_portal_client import app
        logger.info("Successfully imported parent_portal_client directly")
    except ImportError as e2:
        logger.error(f"Failed direct import: {e2}")
        # Create fallback app
        from fastapi import FastAPI
        app = FastAPI()
        
        @app.get("/")
        async def root():
            return {
                "message": "Parent Portal - Import Error", 
                "error": f"Frontend import: {e}, Direct import: {e2}",
                "status": "Please check file structure"
            }

# Health check endpoints for App Engine
@app.get("/_ah/warmup")
async def warmup():
    logger.info("Parent Portal warmup request received")
    return {"status": "ok", "service": "parent-portal"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "parent-portal"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Parent Portal server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
