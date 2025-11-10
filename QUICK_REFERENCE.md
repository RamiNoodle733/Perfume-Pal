# 🚀 QUICK REFERENCE - Perfume Pal

## ⚡ Super Quick Start

```powershell
# 1. Get API Key
# Visit: https://aistudio.google.com/app/apikey

# 2. Setup
.\start.ps1

# 3. Configure
notepad .env
# Add: GOOGLE_API_KEY=your-key-here

# 4. Run
uvicorn app.main:app --reload

# 5. Open
start http://localhost:8080
```

## 🎯 Essential Commands

### Development
```powershell
# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Run tests
pytest -v

# Check code
python -m pytest --cov=app --cov=agents
```

### Docker
```powershell
# Build
docker build -t perfume-pal .

# Run
docker run -p 8080:8080 -e GOOGLE_API_KEY="key" perfume-pal
```

### Deploy to Cloud Run
```powershell
# One-command deploy
gcloud run deploy perfume-pal --source . --region us-central1 --allow-unauthenticated --set-env-vars GOOGLE_API_KEY="your-key"
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI routes & validation |
| `agents/workflow.py` | Multi-agent workflow |
| `frontend/index.html` | UI structure |
| `frontend/app.js` | Frontend logic |
| `requirements.txt` | Dependencies |
| `Dockerfile` | Container config |
| `.env` | Environment variables |

## 🔑 Environment Variables

```bash
GOOGLE_API_KEY=your-gemini-api-key-here
GOOGLE_CLOUD_PROJECT=your-project-id
PORT=8080
ENVIRONMENT=development
```

## 🌐 Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Frontend UI |
| `/health` | GET | Health check |
| `/api/generate_blends` | POST | Generate recipes |
| `/docs` | GET | API documentation |

## 📋 API Request Example

```json
{
  "style": "dark oud",
  "strength": "moderate",
  "bottle_size_ml": 10,
  "vibe_words": ["smoky", "warm"],
  "user_ingredients": ["oud", "sandalwood"]
}
```

## 🎬 Demo Video Script (3 min)

**[0:00-0:30]** Intro
- "Hi! This is Perfume Pal, AI fragrance design for Cloud Run Hackathon"
- "Multi-agent system with Google ADK and Gemini"

**[0:30-1:00]** Architecture
- Show diagram
- "Two agents: Scent Planner → Formula Architect"
- "Deployed on Cloud Run"

**[1:00-2:00]** Live Demo
- Enter: Dark Oud, Moderate, 10ml
- Add vibes: smoky, mysterious
- Generate and wait
- Show results

**[2:00-2:45]** Results Tour
- Recipe name and description
- Top/Heart/Base notes
- Ingredient table with drops
- Instructions

**[2:45-3:00]** Close
- "Multi-agent AI makes perfume design accessible"
- GitHub link
- #CloudRunHackathon

## 📱 Social Media Post

```
🌸 Just built Perfume Pal for #CloudRunHackathon!

An AI-powered fragrance designer using multi-agent workflow:
🤖 Agent 1: Analyzes your scent preferences  
🧪 Agent 2: Generates precise perfume recipes
☁️ Deployed on Google Cloud Run

Describe your vibe → Get custom recipes with exact drop counts!

Built with Google ADK + Gemini + FastAPI
Try it: [your-url]
Code: github.com/RamiNoodle733/Perfume-Pal

#GoogleCloud #AIAgents #Gemini
```

## 🐛 Troubleshooting

### Server won't start
```powershell
# Check Python
python --version

# Reinstall deps
pip install -r requirements.txt

# Check port
netstat -ano | findstr :8080
```

### API key not working
```powershell
# Check .env exists
cat .env

# Verify key format
# Should be: GOOGLE_API_KEY=AIza...

# Restart server
```

### Import errors
```powershell
# Activate venv
venv\Scripts\activate

# Reinstall
pip install -r requirements.txt
```

## 📊 Testing Checklist

- [ ] Health endpoint works: `/health`
- [ ] Frontend loads: `http://localhost:8080`
- [ ] API docs load: `/docs`
- [ ] Can generate recipe with minimal input
- [ ] Can generate recipe with all fields
- [ ] Error handling works (invalid input)
- [ ] Tests pass: `pytest -v`

## 🎯 Deployment Checklist

- [ ] Code committed to GitHub
- [ ] `.env` file not committed (in `.gitignore`)
- [ ] API key obtained from Google AI Studio
- [ ] GCP project created
- [ ] Cloud Run API enabled
- [ ] Deployed successfully
- [ ] Public URL works
- [ ] Environment variables set on Cloud Run

## 📹 Demo Video Checklist

- [ ] Recorded (max 3 minutes)
- [ ] Uploaded to YouTube (public)
- [ ] Shows project functioning
- [ ] Explains architecture
- [ ] In English or with subtitles
- [ ] Good audio quality
- [ ] Shows URL/GitHub

## 📝 Devpost Submission Checklist

- [ ] Project title: "Perfume Pal"
- [ ] Category: AI Agents
- [ ] Description written
- [ ] Demo video link added
- [ ] GitHub repo link added
- [ ] Cloud Run URL added
- [ ] Architecture diagram included
- [ ] Screenshots added
- [ ] Technologies listed
- [ ] Share app link (if AI Studio category)

## 💡 Key Talking Points

1. **Multi-agent collaboration** - Two specialized AI agents
2. **Google ADK** - Official agent framework
3. **Gemini** - Powering both agents
4. **Cloud Run** - Serverless, scalable deployment
5. **Real value** - Practical tool for hobbyists
6. **Production ready** - Full error handling, testing, docs

## 🏆 Bonus Points Strategy

✅ Use Gemini models (+0.4)
✅ Multiple Cloud Run services (+0.4)
✅ Write blog post about building it (+0.4)
✅ Post on social media with #CloudRunHackathon (+0.4)

**Total potential bonus: +1.6 points!**

## 📚 Documentation Map

- `README.md` - Start here, main overview
- `PROJECT_SUMMARY.md` - Complete project summary
- `ARCHITECTURE.md` - Technical architecture details
- `DEPLOYMENT.md` - Step-by-step Cloud Run deployment
- `DEVGUIDE.md` - Developer guide and best practices
- `QUICK_REFERENCE.md` - This file

## 🔗 Important Links

- **AI Studio (API Key):** https://aistudio.google.com/app/apikey
- **Cloud Run Console:** https://console.cloud.google.com/run
- **Hackathon Page:** https://run.devpost.com
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Google ADK Docs:** https://ai.google.dev

## ✨ You're Ready!

Everything is set up and ready to go. Just:
1. Get your API key
2. Run `.\start.ps1`
3. Start coding/testing
4. Record demo video
5. Deploy to Cloud Run
6. Submit to Devpost

**Good luck! 🌸✨**

---

*For detailed information, see the full documentation files.*
