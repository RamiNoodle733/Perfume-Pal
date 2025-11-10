# Development Guide

This guide provides detailed information for developers working on Perfume Pal.

## Table of Contents

- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Running Locally](#running-locally)
- [Testing](#testing)
- [Code Style](#code-style)
- [Adding New Features](#adding-new-features)
- [Troubleshooting](#troubleshooting)

## Project Structure

```
perfume-pal/
├── app/                        # FastAPI application
│   ├── __init__.py
│   └── main.py                 # API endpoints and app initialization
├── agents/                     # AI agent implementations
│   ├── __init__.py
│   └── workflow.py             # Multi-agent workflow with ADK
├── frontend/                   # Static frontend files
│   ├── index.html              # Main UI
│   ├── app.js                  # Frontend logic
│   └── styles.css              # Styling
├── tests/                      # Test suite
│   └── test_api.py             # API endpoint tests
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── README.md                   # Main documentation
├── ARCHITECTURE.md             # Architecture details
├── DEPLOYMENT.md               # Deployment guide
├── DEVGUIDE.md                 # This file
└── start.ps1                   # Quick start script (Windows)
```

## Development Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- Google Cloud account (for deployment)
- Gemini API key

### Initial Setup

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/RamiNoodle733/Perfume-Pal.git
   cd Perfume-Pal
   ```

2. **Create virtual environment:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```powershell
   # Copy example env file
   copy .env.example .env
   
   # Edit .env and add your API key
   notepad .env
   ```

5. **Get API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create or copy your API key
   - Add to `.env` file as `GOOGLE_API_KEY=your-key-here`

## Running Locally

### Method 1: Direct Python

```powershell
# Make sure virtual environment is activated
venv\Scripts\activate

# Set environment variables (if not using .env)
$env:GOOGLE_API_KEY="your-api-key"
$env:GOOGLE_CLOUD_PROJECT="your-project-id"

# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Method 2: Using Docker

```powershell
# Build the image
docker build -t perfume-pal .

# Run the container
docker run -p 8080:8080 `
  -e GOOGLE_API_KEY="your-api-key" `
  -e GOOGLE_CLOUD_PROJECT="your-project-id" `
  perfume-pal
```

### Method 3: Quick Start Script

```powershell
# Run the setup and start script
.\start.ps1
```

### Accessing the Application

- **Frontend:** http://localhost:8080
- **API Docs:** http://localhost:8080/docs
- **Health Check:** http://localhost:8080/health

## Testing

### Running Tests

```powershell
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=app --cov=agents tests/

# Generate coverage report
pytest --cov=app --cov=agents --cov-report=html tests/
```

### Manual Testing

#### Test Health Endpoint

```powershell
curl http://localhost:8080/health
```

#### Test Generate Blends Endpoint

```powershell
# PowerShell
$body = @{
    style = "dark oud"
    strength = "moderate"
    bottle_size_ml = 10
    vibe_words = @("smoky", "warm")
    user_ingredients = @("oud", "sandalwood")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api/generate_blends" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

### Writing Tests

When adding new features, follow these testing patterns:

```python
# tests/test_new_feature.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_new_endpoint(client):
    response = client.get("/new-endpoint")
    assert response.status_code == 200
    assert "expected_key" in response.json()
```

## Code Style

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specifics:

- **Line length:** 100 characters max
- **Indentation:** 4 spaces
- **Imports:** Grouped and sorted
- **Docstrings:** Google style

Example:

```python
def generate_recipe(preferences: dict) -> dict:
    """
    Generate a perfume recipe based on user preferences.
    
    Args:
        preferences: Dictionary with user input including style, strength, etc.
        
    Returns:
        Dictionary containing the generated recipe.
        
    Raises:
        ValueError: If preferences are invalid.
    """
    # Implementation
    pass
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import List, Dict, Optional

def process_ingredients(
    ingredients: List[str], 
    bottle_size: int,
    intensity: Optional[str] = None
) -> Dict[str, any]:
    pass
```

### Docstrings

All modules, classes, and functions should have docstrings:

```python
"""
Module docstring explaining the purpose.
"""

class ScentPlanner:
    """
    Class docstring explaining the agent's role.
    """
    
    def create_brief(self, preferences: dict) -> dict:
        """
        Method docstring with Args, Returns, Raises sections.
        """
        pass
```

## Adding New Features

### Adding a New API Endpoint

1. **Define Pydantic model in `app/main.py`:**

```python
class NewFeatureRequest(BaseModel):
    field1: str
    field2: int
```

2. **Create endpoint function:**

```python
@app.post("/api/new-feature", tags=["Features"])
async def new_feature(request: NewFeatureRequest):
    """Endpoint documentation."""
    # Implementation
    return {"result": "data"}
```

3. **Add tests in `tests/test_api.py`:**

```python
def test_new_feature_endpoint(client):
    response = client.post("/api/new-feature", json={
        "field1": "value",
        "field2": 42
    })
    assert response.status_code == 200
```

### Adding a New Agent

1. **Create agent class in `agents/workflow.py`:**

```python
class NewAgent:
    """New agent for specific task."""
    
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)
        self.system_prompt = """Agent instructions..."""
    
    async def execute(self, input_data: dict) -> dict:
        """Execute agent task."""
        # Implementation
        pass
```

2. **Integrate into workflow:**

```python
async def run_blend_workflow(user_preferences: dict) -> dict:
    # ... existing agents ...
    new_agent = NewAgent()
    result = await new_agent.execute(data)
    # ... continue workflow ...
```

### Modifying the Frontend

1. **Update HTML** (`frontend/index.html`) for structure
2. **Update CSS** (`frontend/styles.css`) for styling
3. **Update JavaScript** (`frontend/app.js`) for functionality

Example: Adding a new form field:

```html
<!-- frontend/index.html -->
<div class="form-group">
    <label for="new-field">New Field</label>
    <input type="text" id="new-field" name="new-field">
</div>
```

```javascript
// frontend/app.js
function getFormData() {
    // ... existing code ...
    const newField = document.getElementById('new-field').value;
    return {
        // ... existing fields ...
        new_field: newField
    };
}
```

## Environment Variables

### Required Variables

- `GOOGLE_API_KEY`: Your Gemini API key
- `GOOGLE_CLOUD_PROJECT`: GCP project ID (optional for local dev)

### Optional Variables

- `PORT`: Server port (default: 8080)
- `ENVIRONMENT`: Environment name (development/production)

### Loading Environment Variables

The app uses `python-dotenv` to load from `.env` file:

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
```

## Debugging

### Enable Debug Logging

```python
# In app/main.py or agents/workflow.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

#### Issue: Import errors

**Solution:**
```powershell
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: API key not working

**Solution:**
1. Check `.env` file exists and has correct format
2. Verify API key at [AI Studio](https://aistudio.google.com/app/apikey)
3. Restart the server after updating `.env`

#### Issue: Port already in use

**Solution:**
```powershell
# Find process using port 8080
netstat -ano | findstr :8080

# Kill the process (replace PID)
taskkill /PID <process_id> /F

# Or use a different port
uvicorn app.main:app --port 8081
```

### Using VS Code Debugger

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--port",
                "8080"
            ],
            "jinja": true,
            "justMyCode": true,
            "env": {
                "GOOGLE_API_KEY": "your-api-key-here"
            }
        }
    ]
}
```

## Performance Optimization

### Backend

1. **Cache responses** (if appropriate)
2. **Use async/await** properly
3. **Optimize Gemini calls** (batch when possible)
4. **Monitor memory usage**

### Frontend

1. **Minimize API calls**
2. **Add loading states**
3. **Implement debouncing** for user input
4. **Optimize CSS** (remove unused styles)

## Git Workflow

### Branching Strategy

```
main                  # Production-ready code
├── develop          # Development branch
│   ├── feature/xxx  # Feature branches
│   ├── bugfix/xxx   # Bug fix branches
│   └── hotfix/xxx   # Urgent fixes
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new scent style options
fix: resolve API timeout issue
docs: update deployment guide
test: add tests for agent workflow
refactor: simplify ingredient calculation
```

## Resources

### Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Google Generative AI Python](https://ai.google.dev/tutorials/python_quickstart)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Cloud Run Docs](https://cloud.google.com/run/docs)

### Tools

- [Postman](https://www.postman.com/) - API testing
- [VS Code](https://code.visualstudio.com/) - IDE
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) - Containerization
- [Google Cloud Console](https://console.cloud.google.com/) - Cloud management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Questions?

- **Issues:** Open an issue on GitHub
- **Discussions:** Use GitHub Discussions
- **Email:** Contact via Devpost profile

---

Happy coding! 🌸✨
