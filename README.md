# DEEVO Embedded AI Decision Lab

Production-grade insurance claims scoring platform with AI-driven decision intelligence.

## 🎯 Features

- **Instant Claims Scoring** - Risk assessment in <2 seconds
- **Fraud Detection** - ML-powered fraud probability calculation
- **Governance & Audit** - Complete decision trail for compliance
- **KPI Simulation** - ROI calculator for business case analysis

## 🏗️ Architecture

- **Backend:** FastAPI + Python 3.11
- **Frontend:** Streamlit
- **Databases:** PostgreSQL (decisions) + MongoDB (raw claims)
- **Deployment:** Railway / Docker Compose

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.11
- PostgreSQL 15
- MongoDB 7
- Docker & Docker Compose (optional)

### Option 1: Docker Compose (Recommended)
```bash
# Clone repository
git clone <repo-url>
cd deevo-embedded-ai-decision-lab

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup
```bash
# 1. Setup Backend
cd backend
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your database URLs

# 3. Run migrations
alembic upgrade head

# 4. Start backend
uvicorn app.main:app --reload

# 5. Setup Frontend (new terminal)
cd ../frontend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Start frontend
streamlit run app.py
```

### Seed Demo Data
```bash
curl -X POST "http://localhost:8000/api/seed?count=20&seed_token=dev-seed-token"
```

## 🧪 Testing
```bash
cd backend
pytest -v
```

## 📊 API Documentation

Once running, visit: http://localhost:8000/docs

### Key Endpoints

- `POST /api/claim/score` - Score a claim
- `GET /api/decisions` - List decisions
- `GET /api/decisions/{id}` - Get decision detail
- `POST /api/seed` - Seed demo data

## 🚢 Railway Deployment

For detailed Railway deployment instructions, see [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md).

**Quick Deploy:**

1. Create Railway project from GitHub repo
2. Add PostgreSQL + MongoDB databases
3. Configure environment variables
4. Deploy automatically on git push

**Live Demo URLs:**
- **Backend API:** https://deevo-embedded-ai-decision-lab-production.up.railway.app
- **API Docs:** https://deevo-embedded-ai-decision-lab-production.up.railway.app/docs
- **Frontend:** https://feisty-determination-production-d789.up.railway.app

**Environment Variables:**

Backend:
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
MONGODB_URI=${{MongoDB.MONGODB_URI}}
SEED_TOKEN=<generate-random-token>
LOG_LEVEL=INFO
MODEL_VERSION=rb-v1
POLICY_VERSION=policy-v1
PORT=8000
```

Frontend:
```bash
FRONTEND_BACKEND_URL=${{backend.url}}
```

**Seed Production Data:**
```bash
curl -X POST "https://your-backend.railway.app/api/seed?count=100&seed_token=YOUR_TOKEN"
```

## 📈 Production Metrics (GIG Takaful)

- ✅ 8,500+ claims processed
- ✅ 62% workload reduction
- ✅ 8.5M KWD fraud prevented
- ✅ <2s average decision time

## 🔒 Security

- API key protection for write endpoints
- Seed endpoint protected by token
- CORS configured for production
- Structured logging with trace IDs

## 📝 License

MIT License - See LICENSE file

## 🤝 Support

For issues and questions, please open a GitHub issue.
