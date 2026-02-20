# Railway Deployment Guide - DEEVO Intelligence Lab

## 🚀 Quick Deploy to Railway

### Prerequisites
- Railway account (https://railway.app)
- GitHub repository with code
- 15 minutes

### Step-by-Step Deployment

#### 1. Create Railway Project

```bash
# Option A: Using Railway CLI
npm install -g @railway/cli
railway login
railway init
railway link

# Option B: Using Web Dashboard
# Go to https://railway.app/new
# Click "Deploy from GitHub repo"
# Select your repository
```

#### 2. Add PostgreSQL Database

1. In Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically:
   - Provision PostgreSQL 15
   - Generate `DATABASE_URL` environment variable
   - Inject into backend service

**No configuration needed** - Railway handles this automatically.

#### 3. Add MongoDB Database

**Option A: Railway MongoDB Plugin (Recommended)**

1. Click **"+ New"** → **"Database"** → **"Add MongoDB"**
2. Railway provisions MongoDB
3. Auto-generates `MONGODB_URI`

**Option B: MongoDB Atlas (Free Tier)**

1. Go to https://cloud.mongodb.com
2. Create free account
3. Create M0 cluster (free tier, 512MB)
4. Click **"Connect"** → **"Connect your application"**
5. Copy connection string:
```
mongodb+srv://username:password@cluster.mongodb.net/deevo_lab
```
6. Replace `<password>` with actual password
7. Add to Railway backend environment variables

#### 4. Configure Backend Service

**Service Settings:**

- **Name:** backend
- **Root Directory:** `/backend`
- **Builder:** nixpacks (auto-detected)

**Environment Variables:**

Click "Variables" tab and add:
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}  # Auto-populated
MONGODB_URI=${{MongoDB.MONGODB_URI}}     # Auto-populated or paste Atlas URI
SEED_TOKEN=<generate-random-token>       # Generate with: openssl rand -hex 16
LOG_LEVEL=INFO
MODEL_VERSION=rb-v1
POLICY_VERSION=policy-v1
PORT=8000
```

**Optional Variables:**
```bash
OLLAMA_BASE_URL=http://your-ollama-server:11434  # If using Ollama
OLLAMA_MODEL=llama3.1
API_KEY=<your-api-key>  # For write endpoint protection
```

**Build Settings:**

Railway auto-detects from `nixpacks.toml`:
```toml
[start]
cmd = "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

**Custom Domain (Optional):**
- Settings → Networking → Generate Domain
- Or add custom domain: `api.yourcompany.com`

#### 5. Configure Frontend Service

**Service Settings:**

- **Name:** frontend
- **Root Directory:** `/frontend`
- **Builder:** nixpacks

**Environment Variables:**
```bash
FRONTEND_BACKEND_URL=${{backend.url}}  # Railway auto-links services
```

**Build Settings:**

From `nixpacks.toml`:
```toml
[start]
cmd = "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"
```

#### 6. Deploy Services

**Automatic Deployment:**

Railway automatically deploys when you push to GitHub:
```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
```

Railway will:
1. Detect changes
2. Build backend (~2-3 min)
3. Run migrations (`alembic upgrade head`)
4. Build frontend (~1-2 min)
5. Generate public URLs

**Manual Deployment:**

Click **"Deploy"** button in Railway dashboard for each service.

#### 7. Verify Deployment

**Backend Health Check:**
```bash
curl https://your-backend.railway.app/health
# Expected: {"status":"healthy","service":"deevo-backend"}
```

**API Documentation:**
```
https://your-backend.railway.app/docs
```

**Frontend:**
```
https://your-frontend.railway.app
```

#### 8. Seed Demo Data
```bash
curl -X POST "https://your-backend.railway.app/api/seed?count=100&seed_token=YOUR_SEED_TOKEN"
```

**Response:**
```json
{"message": "Seeded 100 demo claims"}
```

#### 9. Test End-to-End

1. Open frontend URL
2. Navigate to "Claim Scoring" page
3. Enter test claim:
```
Claim ID: PROD-TEST-001
Customer ID: CUST-12345
Amount: 5000
Incident Type: collision
History Score: 45
```
4. Click "Score Claim"
5. Verify decision returns in <2 seconds

---

## 🔧 Troubleshooting

### Backend Fails to Start

**Check logs:**
```bash
railway logs --service backend
```

**Common issues:**

1. **Database connection failed**
   - Verify `DATABASE_URL` is set
   - Check PostgreSQL service is running
   - Format: `postgresql://user:pass@host:port/db`

2. **Migration errors**
   - Ensure Alembic migrations run before uvicorn
   - Check start command includes `alembic upgrade head`

3. **Port binding**
   - Must use `$PORT` environment variable
   - Railway assigns port dynamically

**Solution:**
```toml
# nixpacks.toml
[start]
cmd = "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

### Frontend Can't Connect to Backend

**Check:**
1. `FRONTEND_BACKEND_URL` environment variable set correctly
2. Use `${{backend.url}}` for automatic service linking
3. Backend service is healthy (check /health endpoint)

**Fix:**
```bash
# In frontend service environment variables
FRONTEND_BACKEND_URL=${{backend.url}}
```

### MongoDB Connection Issues

**If using MongoDB Atlas:**

1. **Whitelist Railway IPs:**
   - Atlas → Security → Network Access
   - Add IP: `0.0.0.0/0` (allow all)
   - Or specific Railway IPs

2. **Check connection string:**
```
mongodb+srv://user:password@cluster.mongodb.net/deevo_lab?retryWrites=true&w=majority
```

3. **Database user permissions:**
   - Atlas → Database Access
   - Ensure user has read/write permissions

### Build Failures

**Python dependency errors:**
```bash
# Check requirements.txt versions are compatible
pip install -r requirements.txt
```

**Nixpacks configuration:**

Ensure `nixpacks.toml` exists in service root directory.

---

## 📊 Monitoring & Logs

### View Logs

**Backend:**
```bash
railway logs --service backend --tail
```

**Frontend:**
```bash
railway logs --service frontend --tail
```

**Web Dashboard:**
- Railway project → Service → Logs tab

### Metrics

Railway provides built-in metrics:
- CPU usage
- Memory usage
- Network traffic
- Response times

Access: Service → Metrics tab

### Health Checks

Configure health check endpoints:

**Backend:**
- Endpoint: `/health`
- Interval: 60s
- Timeout: 10s

**Frontend:**
- Streamlit includes built-in health check
- Automatically configured by Railway

---

## 🔒 Security Best Practices

### 1. Environment Variables

**Never commit secrets:**
```bash
# .gitignore
.env
.env.local
.env.production
```

**Use Railway secrets:**
- All sensitive values in Railway Variables
- Auto-encrypted at rest
- Injected at runtime

### 2. API Key Protection

Enable API key for write endpoints:
```bash
# In environment variables
API_KEY=your-secret-key-here
```

Protected endpoints:
- POST /api/claim/score
- POST /api/seed

### 3. CORS Configuration

Restrict origins in production:
```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.railway.app",
        "https://yourcompany.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 4. Database Backups

**PostgreSQL:**
- Railway automatic daily backups
- Retention: 7 days
- Access: Database service → Backups

**MongoDB Atlas:**
- Configure backup schedule
- Atlas → Backup → Configure

---

## 💰 Cost Management

### Railway Pricing

**Hobby Plan:** $5/month
- Includes $5 credit
- Pay per usage after credit
- Estimate: $10-20/month for moderate traffic

**Pro Plan:** $20/month
- Includes $20 credit
- Better for production

### Optimize Costs

1. **Scale down when not in use:**
   - Settings → Sleep mode (Hobby plan)

2. **Monitor usage:**
   - Dashboard → Usage tab
   - Set up budget alerts

3. **Database optimization:**
   - PostgreSQL: Shared instance for development
   - MongoDB: Use free Atlas tier (512MB)

---

## 🔄 CI/CD Pipeline

### Automatic Deployments

Railway auto-deploys on git push:
```bash
# Enable/disable in Railway dashboard
Settings → Deploys → Auto-deploy: ON
```

**Branch deployments:**
- `main` → production
- `staging` → staging environment
- Feature branches → preview deployments

### Manual Deployments
```bash
# Using Railway CLI
railway up

# Or from GitHub Actions
- name: Deploy to Railway
  env:
    RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
  run: railway up
```

---

## 📈 Scaling

### Horizontal Scaling

**Railway supports:**
- Multiple instances per service
- Load balancing (automatic)
- Auto-scaling based on traffic

**Enable:**
```bash
# Settings → Service → Replicas
Min: 1
Max: 5
```

### Vertical Scaling

**Increase resources:**
- Settings → Resources
- Adjust CPU/Memory limits
- Costs increase proportionally

### Database Scaling

**PostgreSQL:**
- Start: Shared instance
- Scale: Dedicated instance
- Railway managed

**MongoDB:**
- Atlas M0 (free) → M10 (paid)
- Vertical + horizontal scaling available

---

## 🎯 Production Checklist

Before going live:

- [ ] All environment variables configured
- [ ] Database backups enabled
- [ ] Custom domain configured
- [ ] CORS restricted to production domains
- [ ] API key protection enabled
- [ ] Health checks passing
- [ ] Logs monitoring configured
- [ ] SSL certificates active (Railway auto)
- [ ] Rate limiting considered
- [ ] Load testing completed

---

## 🔗 Live Deployment URLs

**Current Production:**
- **Backend API:** https://deevo-embedded-ai-decision-lab-production.up.railway.app
- **API Docs:** https://deevo-embedded-ai-decision-lab-production.up.railway.app/docs
- **Frontend:** https://feisty-determination-production-d789.up.railway.app

---

## 📞 Support

**Railway:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Support: https://help.railway.app

**DEEVO Platform:**
- GitHub: https://github.com/PyBADR/deevo-embedded-ai-decision-lab
- Documentation: README.md
