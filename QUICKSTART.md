# 🚀 QUICK START GUIDE

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for Gemini API)

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy your API key

### Step 3: Configure Environment
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```

### Step 4: Start the Server
```bash
uvicorn main:app --reload
```

### Step 5: Open in Browser
Visit: http://localhost:8000/docs

---

## Common Commands

### Start Server
```bash
uvicorn main:app --reload
```

### Run Demo Script
```bash
python demo.py
```

### Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Test API with cURL

**Create a todo (auto-generates description):**
```bash
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Python"}'
```

**List all todos:**
```bash
curl http://localhost:8000/todos
```

**Generate AI description:**
```bash
curl -X POST http://localhost:8000/generate-description \
  -H "Content-Type: application/json" \
  -d '{"title": "Build a website"}'
```

---

## Project Files

| File | Purpose |
|------|---------|
| `main.py` | Main FastAPI application |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `demo.py` | Interactive demo script |
| `.env.example` | Environment variables template |
| `.gitignore` | Git ignore rules |

---

## Troubleshooting

### Port 8000 already in use?
```bash
uvicorn main:app --reload --port 8001
```

### Module not found errors?
Make sure virtual environment is activated:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

### API key not working?
- Verify key is in `.env` file (not just `.env.example`)
- Check key is correct at: https://makersuite.google.com/app/apikey
- Restart the server after updating.env

---

## Next Steps

1. ✅ Get the server running
2. 📖 Explore http://localhost:8000/docs
3. 🧪 Run `python demo.py`
4. 🔧 Modify and extend the code
5. 🚀 Deploy your API

---

For full documentation, see: **README.md**
