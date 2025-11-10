"""
Tests for Perfume Pal API endpoints.

Tests the FastAPI application endpoints including health checks
and blend generation functionality.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test the /health endpoint returns 200 and expected JSON."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "version" in data


def test_root_endpoint(client):
    """Test the root endpoint returns successfully."""
    response = client.get("/")
    
    # Should return either the frontend HTML or a JSON message
    assert response.status_code == 200


@patch("agents.workflow.run_blend_workflow")
def test_generate_blends_success(mock_workflow, client):
    """Test successful blend generation with mocked workflow."""
    
    # Mock the workflow response
    mock_workflow.return_value = {
        "recipes": [
            {
                "name": "Test Blend",
                "description": "A test perfume blend",
                "notes": {
                    "top": ["bergamot"],
                    "heart": ["lavender"],
                    "base": ["sandalwood"]
                },
                "ingredients": [
                    {
                        "material": "sandalwood",
                        "role": "base",
                        "percent": 50,
                        "drops_for_bottle": 50
                    },
                    {
                        "material": "lavender",
                        "role": "heart",
                        "percent": 30,
                        "drops_for_bottle": 30
                    },
                    {
                        "material": "bergamot",
                        "role": "top",
                        "percent": 20,
                        "drops_for_bottle": 20
                    }
                ],
                "carrier": {
                    "material": "jojoba oil",
                    "percent": 0
                },
                "instructions": [
                    "Add all ingredients to bottle",
                    "Shake well",
                    "Let rest for 48 hours"
                ],
                "safety_note": "Always patch test before use."
            }
        ]
    }
    
    # Make request
    request_data = {
        "style": "fresh citrus",
        "strength": "moderate",
        "bottle_size_ml": 10,
        "vibe_words": ["fresh", "clean"],
        "user_ingredients": ["bergamot", "lavender"]
    }
    
    response = client.post("/api/generate_blends", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "recipes" in data
    assert len(data["recipes"]) > 0
    
    recipe = data["recipes"][0]
    assert "name" in recipe
    assert "description" in recipe
    assert "notes" in recipe
    assert "ingredients" in recipe
    assert "instructions" in recipe
    assert "safety_note" in recipe


def test_generate_blends_validation_missing_style(client):
    """Test validation error when style is missing."""
    request_data = {
        "strength": "moderate",
        "bottle_size_ml": 10
    }
    
    response = client.post("/api/generate_blends", json=request_data)
    
    assert response.status_code == 422  # Validation error


def test_generate_blends_validation_invalid_strength(client):
    """Test validation error when strength is invalid."""
    request_data = {
        "style": "fresh citrus",
        "strength": "invalid_strength",
        "bottle_size_ml": 10
    }
    
    response = client.post("/api/generate_blends", json=request_data)
    
    assert response.status_code == 422  # Validation error


def test_generate_blends_validation_bottle_size_too_small(client):
    """Test validation error when bottle size is too small."""
    request_data = {
        "style": "fresh citrus",
        "strength": "moderate",
        "bottle_size_ml": 2  # Too small (min is 5)
    }
    
    response = client.post("/api/generate_blends", json=request_data)
    
    assert response.status_code == 422  # Validation error


def test_generate_blends_validation_bottle_size_too_large(client):
    """Test validation error when bottle size is too large."""
    request_data = {
        "style": "fresh citrus",
        "strength": "moderate",
        "bottle_size_ml": 150  # Too large (max is 100)
    }
    
    response = client.post("/api/generate_blends", json=request_data)
    
    assert response.status_code == 422  # Validation error


def test_generate_blends_with_optional_fields(client):
    """Test blend generation with all optional fields."""
    with patch("agents.workflow.run_blend_workflow") as mock_workflow:
        mock_workflow.return_value = {"recipes": []}
        
        request_data = {
            "style": "dark oud",
            "strength": "strong",
            "bottle_size_ml": 30,
            "vibe_words": ["smoky", "mysterious", "warm"],
            "user_ingredients": ["oud", "sandalwood", "amber"]
        }
        
        response = client.post("/api/generate_blends", json=request_data)
        
        # Should succeed even if no recipes returned
        assert response.status_code == 200


def test_generate_blends_with_string_ingredients(client):
    """Test blend generation with comma-separated ingredients string."""
    with patch("agents.workflow.run_blend_workflow") as mock_workflow:
        mock_workflow.return_value = {"recipes": []}
        
        request_data = {
            "style": "sweet gourmand",
            "strength": "moderate",
            "bottle_size_ml": 10,
            "user_ingredients": "vanilla, tonka bean, cocoa"
        }
        
        response = client.post("/api/generate_blends", json=request_data)
        
        assert response.status_code == 200


@patch("agents.workflow.run_blend_workflow")
def test_generate_blends_workflow_error(mock_workflow, client):
    """Test error handling when workflow fails."""
    from agents.workflow import WorkflowError
    
    # Mock workflow to raise an error
    mock_workflow.side_effect = WorkflowError("Failed to generate recipes")
    
    request_data = {
        "style": "fresh citrus",
        "strength": "moderate",
        "bottle_size_ml": 10
    }
    
    response = client.post("/api/generate_blends", json=request_data)
    
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
