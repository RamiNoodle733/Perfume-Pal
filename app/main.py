"""
FastAPI application for Perfume Pal.

This module defines the API endpoints for the perfume recipe generator,
including health checks and the main blend generation endpoint.
"""

import os
import logging
from typing import Optional, List, Union
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator

from agents.workflow import run_blend_workflow, WorkflowError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Perfume Pal API",
    description="AI-powered perfume recipe generator using multi-agent workflow",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend)
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


# Request/Response Models
class GenerateBlendRequest(BaseModel):
    """Request model for generating perfume blends."""
    
    style: str = Field(
        ...,
        description="Scent style (e.g., 'dark oud', 'fresh citrus', 'sweet gourmand', 'clean musk')",
        example="dark oud"
    )
    strength: str = Field(
        ...,
        description="Fragrance strength: 'subtle', 'moderate', or 'strong'",
        example="moderate"
    )
    bottle_size_ml: int = Field(
        ...,
        ge=5,
        le=100,
        description="Bottle size in milliliters (5-100ml)",
        example=10
    )
    vibe_words: Optional[List[str]] = Field(
        default=None,
        description="Optional list of descriptive words for the fragrance vibe",
        example=["smoky", "warm", "mysterious"]
    )
    user_ingredients: Optional[Union[List[str], str]] = Field(
        default=None,
        description="Optional list or comma-separated string of materials user already owns",
        example=["oud", "sandalwood", "bergamot"]
    )
    
    @validator("strength")
    def validate_strength(cls, v):
        """Validate strength value."""
        allowed = ["subtle", "moderate", "strong"]
        if v.lower() not in allowed:
            raise ValueError(f"Strength must be one of: {', '.join(allowed)}")
        return v.lower()
    
    @validator("user_ingredients")
    def normalize_ingredients(cls, v):
        """Normalize user ingredients to list format."""
        if v is None:
            return None
        if isinstance(v, str):
            # Split by comma and clean whitespace
            return [ingredient.strip() for ingredient in v.split(",") if ingredient.strip()]
        return v


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str = "1.0.0"


# API Endpoints

@app.get("/", include_in_schema=False)
async def root():
    """Serve the frontend."""
    index_path = frontend_path / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Perfume Pal API", "docs": "/docs"}


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the service status and version.
    """
    return HealthResponse(status="ok", version="1.0.0")


@app.post("/api/generate_blends", tags=["Blends"])
async def generate_blends(request: GenerateBlendRequest):
    """
    Generate perfume blend recipes based on user preferences.
    
    This endpoint uses a multi-agent workflow with Google ADK and Gemini:
    - Agent 1 (Scent Planner): Analyzes preferences and creates a structured brief
    - Agent 2 (Formula Architect): Generates detailed recipes with ingredients
    
    Args:
        request: User preferences including style, strength, bottle size, etc.
    
    Returns:
        JSON with generated recipes including ingredients, notes, and instructions.
    
    Raises:
        HTTPException: If the workflow fails or returns invalid data.
    """
    try:
        logger.info(f"Generating blends for style: {request.style}, strength: {request.strength}")
        
        # Prepare user preferences for workflow
        user_preferences = {
            "style": request.style,
            "strength": request.strength,
            "bottle_size_ml": request.bottle_size_ml,
            "vibe_words": request.vibe_words or [],
            "user_ingredients": request.user_ingredients or []
        }
        
        # Run the multi-agent workflow
        result = await run_blend_workflow(user_preferences)
        
        logger.info(f"Successfully generated {len(result.get('recipes', []))} recipe(s)")
        return JSONResponse(content=result)
        
    except WorkflowError as e:
        logger.error(f"Workflow error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate blends: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while generating blends"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info("=" * 60)
    logger.info("Perfume Pal API Starting...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Port: {os.getenv('PORT', '8080')}")
    
    # Check for required environment variables
    required_vars = ["GOOGLE_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.warning("The application may not function correctly without these variables.")
    else:
        logger.info("All required environment variables are set")
    
    logger.info("Perfume Pal API Started Successfully!")
    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
