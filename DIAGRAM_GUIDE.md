# Architecture Diagram - Visual Guide

## Quick Visual Diagram (Use draw.io, Lucidchart, PowerPoint, or Canva)

### Layout: Top to Bottom Flow

```
Layer 1: USER INTERFACE
┌─────────────────────────────────────┐
│     👤 USER BROWSER                  │
│  ┌───────────────────────────────┐  │
│  │  FRONTEND                     │  │
│  │  • HTML/CSS/JS                │  │
│  │  • Intro Screen               │  │
│  │  • Form Inputs                │  │
│  │  • Recipe Display             │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
           │
           │ POST /api/generate_blends
           │ {"style": "dark oud", ...}
           ▼
Layer 2: CLOUD PLATFORM
┌─────────────────────────────────────┐
│  ☁️ GOOGLE CLOUD RUN                │
│  ┌───────────────────────────────┐  │
│  │  🐍 FASTAPI BACKEND           │  │
│  │  • Python 3.11                │  │
│  │  • Pydantic Validation        │  │
│  │  • Route Handling             │  │
│  └───────────────────────────────┘  │
│           │                          │
│           │ run_blend_workflow()     │
│           ▼                          │
│  ┌───────────────────────────────┐  │
│  │  🤖 MULTI-AGENT WORKFLOW      │  │
│  │                               │  │
│  │  ┌─────────────────────────┐ │  │
│  │  │ 🧠 AGENT 1              │ │  │
│  │  │ Scent Planner           │ │  │
│  │  │ • Analyze preferences   │ │  │
│  │  │ • Create brief          │ │  │
│  │  └──────────┬──────────────┘ │  │
│  │             │ Brief (JSON)    │  │
│  │             ▼                 │  │
│  │  ┌─────────────────────────┐ │  │
│  │  │ ⚗️ AGENT 2              │ │  │
│  │  │ Formula Architect       │ │  │
│  │  │ • Generate recipes      │ │  │
│  │  │ • Calculate amounts     │ │  │
│  │  │ • Create instructions   │ │  │
│  │  └─────────────────────────┘ │  │
│  └───────────────────────────────┘  │
└─────────────────┬───────────────────┘
                  │
                  │ API Calls
                  ▼
Layer 3: AI SERVICE
┌─────────────────────────────────────┐
│  ⚡ GOOGLE GEMINI API                │
│  • gemini-flash-latest              │
│  • JSON Mode                         │
│  • Temperature: 0.7                  │
└─────────────────────────────────────┘
```

## Colors to Use:

- **User Browser**: Light Blue (#87CEEB)
- **Cloud Run Container**: Dark Blue/Navy (#1E3A8A)
- **FastAPI**: Green (#10B981)
- **Agent 1**: Purple (#9D4EDD)
- **Agent 2**: Orange (#F97316)
- **Gemini API**: Google Blue (#4285F4)
- **Arrows**: Cyan (#00D4FF)

## Icons to Include:

- User Browser: 💻 or 👤
- Cloud: ☁️
- Python: 🐐 or Python logo
- AI Agents: 🤖 or 🧠
- Flask/Chemistry: ⚗️ or 🧪
- Lightning: ⚡
- Lock (Security): 🔒

## Key Components to Show:

1. **Frontend Box**
   - Label: "Frontend (HTML/CSS/JS)"
   - Inside: List the 3 sections (Intro, Designer, About)

2. **FastAPI Box**
   - Label: "FastAPI Backend"
   - Show 3 endpoints: GET /, GET /health, POST /api/generate_blends

3. **Agent 1 Box**
   - Label: "Scent Planner Agent"
   - Show: "Input: User Preferences → Output: Structured Brief"

4. **Agent 2 Box**
   - Label: "Formula Architect Agent"
   - Show: "Input: Brief → Output: Recipes with Ingredients"

5. **Gemini API Box**
   - Label: "Google Gemini API"
   - Show: Model name (gemini-flash-latest)

## Arrows/Flow:

1. User Browser → Cloud Run: "HTTP POST" (cyan arrow)
2. FastAPI → Multi-Agent Workflow: "Async Call" (green arrow)
3. Agent 1 → Gemini: "Generate Brief" (purple arrow)
4. Agent 1 → Agent 2: "Structured Brief (JSON)" (orange arrow)
5. Agent 2 → Gemini: "Generate Recipes" (orange arrow)
6. Multi-Agent → FastAPI: "Recipes (JSON)" (green arrow)
7. FastAPI → User Browser: "HTTP Response" (cyan arrow)

## Side Panel - Technology Stack:

Create a small box listing:
- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python, FastAPI, Pydantic
- **AI**: Google Gemini, Google ADK
- **Infrastructure**: Google Cloud Run, Docker
- **Database**: None (stateless)

## Alternative: Simple 3-Box Diagram

If you want it super simple:

```
┌──────────────┐
│   FRONTEND   │
│ (HTML/CSS/JS)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  CLOUD RUN   │
│   FASTAPI    │
│  +2 AI Agents│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ GEMINI API   │
│(AI Models)   │
└──────────────┘
```

## Tools You Can Use:

1. **draw.io** (FREE, easiest)
   - Go to: https://app.diagrams.net/
   - Use rectangles, arrows, and text
   - Export as PNG

2. **Excalidraw** (FREE, hand-drawn style)
   - Go to: https://excalidraw.com/
   - Simple and clean

3. **Canva** (FREE account)
   - Search for "Flowchart" template
   - Customize colors

4. **PowerPoint/Google Slides**
   - Insert shapes
   - Add arrows
   - Screenshot

## Final Touches:

- Add title: "Perfume Pal - System Architecture"
- Add subtitle: "Multi-Agent AI on Google Cloud Run"
- Add your name
- Add date: "November 2025"
- Add footer: "Cloud Run Hackathon 2025"

Save as PNG or PDF and upload to Devpost!
