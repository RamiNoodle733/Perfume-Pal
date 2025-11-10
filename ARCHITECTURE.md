# Perfume Pal - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          User Browser                            │
│                     (Frontend: HTML/CSS/JS)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS Request
                             │ POST /api/generate_blends
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Google Cloud Run                            │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              FastAPI Application                        │    │
│  │              (app/main.py)                              │    │
│  │                                                          │    │
│  │  • Receives user preferences                            │    │
│  │  • Validates input                                       │    │
│  │  • Calls multi-agent workflow                           │    │
│  │  • Returns JSON recipes                                  │    │
│  └──────────────────────┬──────────────────────────────────┘    │
│                         │                                         │
│                         │ Calls workflow                          │
│                         │                                         │
│  ┌──────────────────────▼──────────────────────────────────┐    │
│  │         Multi-Agent Workflow (agents/workflow.py)        │    │
│  │                                                          │    │
│  │  ┌────────────────────────────────────────────────┐    │    │
│  │  │  Agent 1: Scent Planner                        │    │    │
│  │  │  ─────────────────────                         │    │    │
│  │  │  • Analyzes user preferences                   │    │    │
│  │  │  • Creates structured brief:                   │    │    │
│  │  │    - Target profile                            │    │    │
│  │  │    - Note families                             │    │    │
│  │  │    - Constraints                               │    │    │
│  │  │  • Uses Gemini via Google Generative AI       │    │    │
│  │  └──────────────┬─────────────────────────────────┘    │    │
│  │                 │                                        │    │
│  │                 │ Brief JSON                             │    │
│  │                 │                                        │    │
│  │  ┌──────────────▼─────────────────────────────────┐    │    │
│  │  │  Agent 2: Formula Architect                    │    │    │
│  │  │  ────────────────────────                      │    │    │
│  │  │  • Receives brief from Agent 1                 │    │    │
│  │  │  • Generates detailed recipes:                 │    │    │
│  │  │    - Ingredient list                           │    │    │
│  │  │    - Note breakdown (top/heart/base)           │    │    │
│  │  │    - Proportions & drop counts                 │    │    │
│  │  │    - Mixing instructions                       │    │    │
│  │  │  • Uses Gemini via Google Generative AI       │    │    │
│  │  └────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            │ API Calls
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Google Gemini API                             │
│                  (google.generativeai)                           │
│                                                                   │
│  • Model: gemini-1.5-flash (default)                            │
│  • Generates structured JSON responses                          │
│  • Powers both AI agents                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Request Flow
1. User fills out form on frontend with:
   - Scent style (e.g., "dark oud")
   - Strength (subtle/moderate/strong)
   - Bottle size (5-100ml)
   - Optional: vibe words, user ingredients

2. JavaScript sends POST request to `/api/generate_blends`

3. FastAPI validates request using Pydantic models

4. Backend calls `run_blend_workflow()` with user preferences

### Multi-Agent Workflow

5. **Agent 1 (Scent Planner)** executes:
   ```
   Input: User preferences
   Process: 
     - Analyzes scent style and preferences
     - Considers note families (woody, citrus, floral, etc.)
     - Creates structured brief
   Output: 
     {
       "target_profile": "Deep woody oriental with smoky undertones",
       "bottle_size_ml": 10,
       "intensity": "moderate",
       "note_families": ["oud", "amber", "citrus"],
       "recipes_to_generate": 2,
       "max_ingredients_per_recipe": 6,
       "constraints": {...}
     }
   ```

6. **Agent 2 (Formula Architect)** executes:
   ```
   Input: Brief from Agent 1 + user ingredients (optional)
   Process:
     - Selects appropriate fragrance materials
     - Balances note pyramid (top/heart/base)
     - Calculates proportions (total = 100%)
     - Computes drop counts for bottle size
     - Generates mixing instructions
   Output:
     {
       "recipes": [
         {
           "name": "Dark Souk Oud",
           "description": "...",
           "notes": {
             "top": ["bergamot"],
             "heart": ["oud", "saffron"],
             "base": ["amber", "sandalwood"]
           },
           "ingredients": [
             {"material": "oud", "percent": 35, "drops": 35},
             ...
           ],
           "instructions": [...],
           "safety_note": "..."
         }
       ]
     }
   ```

7. FastAPI returns recipes JSON to frontend

8. JavaScript renders recipe cards with:
   - Recipe names and descriptions
   - Note breakdowns
   - Ingredient tables
   - Instructions
   - Safety warnings

## Technology Stack Details

### Backend
- **Framework:** FastAPI 0.109.0
- **Runtime:** Python 3.11
- **AI Framework:** Google Generative AI (google-generativeai)
- **Model:** Gemini 1.5 Flash
- **Validation:** Pydantic v2
- **Server:** Uvicorn with async support

### Frontend
- **HTML5** for structure
- **CSS3** with custom properties for theming
- **Vanilla JavaScript** (no frameworks)
- **Fetch API** for backend communication

### Infrastructure
- **Platform:** Google Cloud Run
- **Container:** Docker (Python 3.11-slim base)
- **Port:** 8080 (configurable via PORT env var)
- **Scaling:** Automatic via Cloud Run
- **Authentication:** API key-based (GOOGLE_API_KEY)

### Development
- **Testing:** pytest with TestClient
- **Linting:** Follows PEP 8
- **Logging:** Python logging module
- **Environment:** python-dotenv for local dev

## Key Features

### Multi-Agent Collaboration
- Two specialized agents with distinct roles
- Structured communication via JSON
- Sequential workflow (Agent 1 → Agent 2)

### Intelligent Recipe Generation
- Respects fragrance note pyramids
- Considers user's existing ingredients
- Calculates precise drop counts
- Provides safety guidance

### Scalability
- Stateless design
- Containerized for easy deployment
- Cloud Run auto-scaling
- No persistent storage required

### User Experience
- Clean, intuitive interface
- Real-time loading feedback
- Detailed recipe cards
- Print-friendly output
- Mobile responsive

## Security Considerations

- API keys stored in environment variables
- Input validation via Pydantic
- XSS prevention in frontend
- CORS configuration
- No user data persistence
- Rate limiting via Cloud Run

## Future Enhancements

- Add more agent types (Scent Reviewer, Safety Checker)
- Support for custom note databases
- User accounts and saved recipes
- Batch recipe generation
- Integration with fragrance suppliers
- Advanced filtering and search
