# RELAI Deployment Guide

Complete guide to deploy RELAI to production.

---

## 📋 Pre-Deployment Checklist

- [ ] All API keys obtained and tested
- [ ] Code tested locally
- [ ] Environment variables documented
- [ ] Database configured (if using)
- [ ] Object storage setup (for videos)
- [ ] Domain name registered
- [ ] SSL certificate ready

---

## 🚀 Deployment Options

### Option 1: Quick Deploy (Recommended for MVP)

**Backend: Railway**
**Frontend: Vercel**
**Storage: Cloudflare R2**

This is the fastest and cheapest option for getting started.

---

## 1️⃣ Deploy Backend to Railway

### Step 1: Prepare Backend

Create `Procfile` in backend folder:
```bash
cd /Users/pedromeza/pedromeza/RELAI/backend
```

Add `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Add `runtime.txt`:
```
python-3.11.0
```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `GYMTOPZ/RELAI`
5. Configure:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables

In Railway dashboard, add:
```
OPENAI_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
SUNO_API_KEY=your_key
PORT=8000
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
```

### Step 4: Get Backend URL

Railway will provide: `https://your-app.railway.app`

---

## 2️⃣ Deploy Frontend to Vercel

### Step 1: Update API URL

Update `frontend/src/App.jsx` to use production backend:

```javascript
// Add at the top
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Update axios calls
axios.post(`${API_URL}/api/upload/image`, formData)
```

Create `frontend/.env.production`:
```
VITE_API_URL=https://your-app.railway.app
```

### Step 2: Deploy to Vercel

```bash
cd frontend
npm install -g vercel
vercel login
vercel
```

Follow prompts:
- Project name: `relai`
- Framework: `Vite`
- Build command: `npm run build`
- Output directory: `dist`

### Step 3: Set Environment Variables

In Vercel dashboard:
```
VITE_API_URL=https://your-app.railway.app
```

### Step 4: Get Frontend URL

Vercel provides: `https://relai.vercel.app`

---

## 3️⃣ Configure Storage (Cloudflare R2)

For storing videos long-term (optional but recommended):

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to R2 Object Storage
3. Create bucket: `relai-videos`
4. Get API credentials
5. Update backend to use R2 instead of local storage

---

## 🔧 Alternative Deployment Options

### Option 2: All-in-One (Docker + DigitalOcean)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - SUNO_API_KEY=${SUNO_API_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./generated_videos:/app/generated_videos

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://backend:8000

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
```

Deploy to DigitalOcean:
1. Create Droplet (Ubuntu 22.04)
2. Install Docker & Docker Compose
3. Clone repo
4. Run `docker-compose up -d`

---

### Option 3: Serverless (AWS Lambda + S3)

For serverless architecture:
- Backend: AWS Lambda (via API Gateway)
- Frontend: S3 + CloudFront
- Storage: S3
- Functions: Lambda for video processing

---

## 🗄️ Database Setup (Optional)

For tracking users and videos:

### PostgreSQL on Supabase (Free tier)

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Get connection string
4. Create tables:

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE videos (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  prompt TEXT NOT NULL,
  status VARCHAR(50) DEFAULT 'processing',
  video_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE uploads (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  file_type VARCHAR(50),
  file_path TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

Update backend to use database instead of in-memory storage.

---

## 🔐 Security Hardening

### 1. Environment Variables

Never commit API keys. Use:
- Railway/Vercel: Built-in secrets
- Docker: `.env` file (add to `.gitignore`)
- AWS: Secrets Manager

### 2. CORS Configuration

Update `backend/main.py`:
```python
origins = [
    "https://relai.vercel.app",
    "https://www.yourdomian.com"
]
```

### 3. Rate Limiting

Add to `backend/main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/video/generate")
@limiter.limit("5/minute")
async def generate_video(request: Request, ...):
    ...
```

### 4. File Upload Limits

Already configured in code, but verify:
```python
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
```

---

## 📊 Monitoring & Logging

### Sentry (Error Tracking)

```bash
pip install sentry-sdk
```

In `backend/main.py`:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

### LogTail (Logging)

```bash
pip install logtail-python
```

---

## 🌐 Custom Domain Setup

### 1. Configure DNS

Add records:
```
Type  | Name | Value
------|------|------
A     | @    | Vercel IP
CNAME | www  | cname.vercel-dns.com
CNAME | api  | your-app.railway.app
```

### 2. Update Vercel

- Go to project settings
- Add domain: `yourdomain.com`
- Vercel handles SSL automatically

### 3. Update Railway

- Add custom domain in settings
- Point `api.yourdomain.com` to Railway

---

## 📈 Scaling Considerations

### When to Scale

- \> 100 videos/day: Consider dedicated server
- \> 1000 users: Add database
- \> 10000 API calls/day: Implement caching
- \> 100GB videos: Move to S3/R2

### Horizontal Scaling

1. Add load balancer (Nginx, CloudFlare)
2. Multiple backend instances
3. Redis for session storage
4. CDN for video delivery

---

## 💰 Cost Estimation

### Monthly Costs (Approximate)

**Low Usage (< 100 videos/month):**
- Railway: $5/month
- Vercel: Free
- Cloudflare R2: ~$1/month
- **Total: ~$6/month**

**Medium Usage (< 1000 videos/month):**
- Railway: $20/month
- Vercel: Free
- Cloudflare R2: ~$10/month
- **Total: ~$30/month**

**High Usage (> 5000 videos/month):**
- DigitalOcean Droplet: $40/month
- Cloudflare R2: ~$50/month
- Database: $25/month
- **Total: ~$115/month**

*Plus API costs (Sora, ElevenLabs, Suno)*

---

## 🧪 Testing in Production

### Health Checks

```bash
# Backend
curl https://your-api.railway.app/

# Frontend
curl https://relai.vercel.app/
```

### End-to-End Test

1. Upload image
2. Generate video
3. Download video
4. Verify quality

---

## 🚨 Rollback Plan

If deployment fails:

1. **Vercel**: Rollback to previous deployment (one click)
2. **Railway**: Rollback in deployments tab
3. **Docker**: `docker-compose down && git checkout previous-commit && docker-compose up`

---

## 📝 Post-Deployment

- [ ] Test all endpoints
- [ ] Verify video generation works
- [ ] Check error logging
- [ ] Monitor performance
- [ ] Set up alerts
- [ ] Update documentation with URLs
- [ ] Announce to users!

---

## 🆘 Troubleshooting

**Issue: Videos not generating**
- Check API keys are correct
- Verify Sora 2 API is enabled
- Check logs for errors

**Issue: Frontend can't reach backend**
- Verify CORS settings
- Check API_URL is correct
- Test backend directly with curl

**Issue: Files not uploading**
- Check file size limits
- Verify upload directory permissions
- Check network timeout settings

---

## 📚 Additional Resources

- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [Cloudflare R2 Docs](https://developers.cloudflare.com/r2/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

**Ready to deploy? Start with Option 1 for fastest results!**
