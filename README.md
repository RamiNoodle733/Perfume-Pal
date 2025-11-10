# Perfume Pal

**Cloud Run Hackathon 2025 - AI Agents Category**

## Overview

Perfume Pal is an AI-powered web application that helps users design custom homemade perfume oil blends. Users describe their desired scent profile, strength preferences, and bottle size, and receive ready-to-mix perfume recipes complete with ingredient breakdowns, note classifications (top/heart/base), and precise drop counts.

The app uses a multi-agent architecture built with Google's Agent Development Kit (ADK) and Gemini models. Two specialized AI agents collaborate: the **Scent Planner** translates user preferences into a structured perfume brief, and the **Formula Architect** generates detailed, mixable recipes based on perfumery principles. The entire backend runs on Google Cloud Run, providing a scalable, serverless solution for personalized fragrance creation.

Whether you're a fragrance enthusiast experimenting at home or looking to explore scent combinations, Perfume Pal makes perfume design accessible and fun.

## Architecture

### Multi-Agent Workflow

```
User Input (Frontend)
    ↓
Cloud Run Backend (FastAPI)
    ↓
Agent 1: Scent Planner (Gemini via ADK)
    - Analyzes user preferences
    - Creates structured perfume brief
    - Defines note families and constraints
    ↓
Agent 2: Formula Architect (Gemini via ADK)
    - Generates detailed recipes
    - Calculates ingredient proportions
    - Provides mixing instructions
    ↓
JSON Response with Recipes
    ↓
Frontend Display
```

**Technology Stack:**
- **Backend:** Python 3.11, FastAPI, Google ADK, Gemini
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Infrastructure:** Google Cloud Run, Docker
- **Testing:** pytest

## API Documentation

### Endpoints

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

#### `POST /api/generate_blends`
Generate perfume recipes based on user preferences.

**Request Body:**
```json
{
  "style": "dark oud",
  "strength": "moderate",
  "bottle_size_ml": 10,
  "vibe_words": ["smoky", "warm", "mysterious"],
  "user_ingredients": ["oud", "sandalwood", "bergamot"]
}
```

**Fields:**
- `style` (string, required): Scent style - "dark oud", "fresh citrus", "sweet gourmand", "clean musk", or custom
- `strength` (string, required): "subtle", "moderate", or "strong"
- `bottle_size_ml` (number, required): Bottle size in ml (e.g., 5, 10, 30)
- `vibe_words` (array, optional): Additional descriptive words
- `user_ingredients` (array or string, optional): Materials user already owns

**Response:**
```json
{
  "recipes": [
    {
      "name": "Dark Souk Oud",
      "description": "A dark oud blend with smoky amber and subtle spice.",
      "notes": {
        "top": ["black pepper"],
        "heart": ["oud", "saffron"],
        "base": ["amber", "sandalwood"]
      },
      "ingredients": [
        {
          "material": "oud",
          "role": "heart",
          "percent": 35,
          "drops_for_bottle": 35
        }
      ],
      "carrier": {
        "material": "fractionated coconut oil or jojoba",
        "percent": 0
      },
      "instructions": [
        "Add all aromatics into a clean bottle using the drop counts.",
        "Top up with carrier oil to reach your bottle size.",
        "Shake gently and let rest for 2-3 days.",
        "Patch test before use."
      ],
      "safety_note": "This is informal guidance only. Always patch test and follow local safety and IFRA guidelines."
    }
  ]
}
```

## Setup and Installation

### Prerequisites

- Python 3.11+
- Docker (for containerization)
- Google Cloud account with billing enabled
- Google Cloud CLI (`gcloud`)

### Environment Variables

Create a `.env` file in the project root:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_API_KEY=your-gemini-api-key

# Optional: Service account credentials
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Server Configuration
PORT=8080
ENVIRONMENT=production
```

**Required:**
- `GOOGLE_API_KEY`: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID

### Running Locally

1. **Clone the repository:**
```bash
cd Perfume-Pal
```

2. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set environment variables:**
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your-api-key-here"
$env:GOOGLE_CLOUD_PROJECT="your-project-id"
```

5. **Run the application:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

6. **Access the app:**
Open `http://localhost:8080` in your browser.

### Running with Docker

1. **Build the Docker image:**
```bash
docker build -t perfume-pal .
```

2. **Run the container:**
```bash
docker run -p 8080:8080 `
  -e GOOGLE_API_KEY="your-api-key" `
  -e GOOGLE_CLOUD_PROJECT="your-project-id" `
  perfume-pal
```

3. **Access the app:**
Open `http://localhost:8080` in your browser.

### Deploying to Cloud Run

1. **Authenticate with Google Cloud:**
```bash
gcloud auth login
gcloud config set project your-project-id
```

2. **Enable required APIs:**
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

3. **Build and deploy:**
```bash
gcloud run deploy perfume-pal `
  --source . `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars GOOGLE_API_KEY="your-api-key",GOOGLE_CLOUD_PROJECT="your-project-id"
```

4. **Alternative: Deploy from Container Registry:**
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/your-project-id/perfume-pal

# Deploy to Cloud Run
gcloud run deploy perfume-pal `
  --image gcr.io/your-project-id/perfume-pal `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars GOOGLE_API_KEY="your-api-key",GOOGLE_CLOUD_PROJECT="your-project-id"
```

5. **Note your service URL:**
After deployment, Cloud Run will provide a URL like `https://perfume-pal-xxxxx.run.app`

### Running Tests

```bash
pytest tests/ -v
```

## Google ADK Configuration

This project uses the **Google Agent Development Kit (ADK)** with Gemini models. The ADK allows us to build structured multi-agent workflows with clear agent roles and communication patterns.

**Setup Steps:**

1. **Get API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create or use existing API key
   - Set as `GOOGLE_API_KEY` environment variable

2. **Agent Configuration:**
   - Agents are defined in `agents/workflow.py`
   - Each agent has a specific system prompt and output schema
   - Agents communicate via structured JSON

3. **Model Selection:**
   - Default: `gemini-1.5-flash` (fast, cost-effective)
   - Alternative: `gemini-1.5-pro` (more sophisticated reasoning)
   - Configurable in `agents/workflow.py`

## Project Structure

```
perfume-pal/
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI application and routes
├── agents/
│   ├── __init__.py
│   └── workflow.py          # ADK agent definitions and workflow
├── frontend/
│   ├── index.html           # Frontend UI
│   ├── app.js               # Frontend JavaScript
│   └── styles.css           # Styling
├── tests/
│   └── test_api.py          # API tests
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container configuration
├── .gitignore
├── .env.example             # Environment variables template
└── README.md
```

## Demo Script (for 3-minute video)

**[0:00-0:30] Introduction**
- "Hi! I'm demonstrating Perfume Pal, an AI-powered perfume design assistant built for the Cloud Run Hackathon."
- "It uses Google's Agent Development Kit with two AI agents that collaborate to create custom perfume recipes."

**[0:30-1:00] Architecture Overview**
- Show architecture diagram or slides
- "Two agents work together: Scent Planner analyzes preferences, Formula Architect generates recipes."
- "Everything runs on Cloud Run with Gemini models powering the agents."

**[1:00-2:00] Live Demo**
- Open the web interface
- "Let me design a dark oud perfume."
- Enter: style="dark oud", strength="moderate", bottle_size=10ml
- Add vibe words: "smoky, warm, mysterious"
- Click Generate
- Show loading state
- "The agents are collaborating to create recipes..."

**[2:00-2:45] Results Walkthrough**
- Show generated recipes
- "Here we have two unique recipes with top, heart, and base notes."
- "Each ingredient has precise drop counts for my 10ml bottle."
- "Instructions for mixing and safety notes included."
- Highlight how it considers user-owned ingredients if provided

**[2:45-3:00] Closing**
- "Perfume Pal makes fragrance design accessible using AI agents on Cloud Run."
- "Code is open source on GitHub. Thanks for watching!"
- Show #CloudRunHackathon hashtag

## Devpost Description

**Perfume Pal - AI-Powered Fragrance Design Assistant**

Perfume Pal helps users create custom homemade perfume oil blends using a multi-agent AI workflow. Simply describe your desired scent vibe, strength, and bottle size, and receive detailed recipes complete with ingredient breakdowns, note classifications, and precise mixing instructions.

Built with Google's Agent Development Kit (ADK) and Gemini models, Perfume Pal employs two specialized agents: a Scent Planner that translates preferences into structured perfume briefs, and a Formula Architect that generates mixable recipes based on perfumery principles. The backend runs entirely on Google Cloud Run, demonstrating scalable serverless architecture for AI agent applications.

Whether you're a fragrance hobbyist or simply curious about scent creation, Perfume Pal makes perfume design accessible, personalized, and fun. The app considers your existing ingredients, respects fragrance note pyramids, and provides safety guidance for home perfume making.

**Technologies:** Google Cloud Run, Google ADK, Gemini, FastAPI, Python, Docker

## Social Media Post Template

### LinkedIn/X Post

🌸 Excited to share my Cloud Run Hackathon project: Perfume Pal!

An AI-powered fragrance design assistant that helps you create custom perfume recipes at home. Built with Google's Agent Development Kit and Gemini models, two AI agents collaborate to transform your scent preferences into detailed, mixable formulas.

🤖 Agent 1 (Scent Planner): Analyzes your preferences
🧪 Agent 2 (Formula Architect): Generates precise recipes
☁️ Deployed on Google Cloud Run for serverless scalability

Check it out: [your-cloud-run-url]
Code: github.com/RamiNoodle733/Perfume-Pal

#CloudRunHackathon #GoogleCloud #AIAgents #Gemini #Serverless #AI

---

### Twitter/X (Short Version)

Built Perfume Pal for the #CloudRunHackathon! 🌸

AI agents + Gemini models = custom perfume recipes
→ Describe your vibe
→ Get detailed formulas with precise drop counts
→ Mix at home!

Powered by @GoogleCloud Run & Agent Development Kit

Try it: [url]
Code: [github-link]

## License

MIT License - Feel free to use and modify for your own projects.

## Acknowledgments

Built for the Google Cloud Run Hackathon 2025 - AI Agents Category

Powered by:
- Google Cloud Run
- Google Agent Development Kit (ADK)
- Google Gemini
- FastAPI
- Python

---

**Questions or Issues?**
Open an issue on GitHub or contact via Devpost.

**Happy fragrance crafting! 🌸✨**
