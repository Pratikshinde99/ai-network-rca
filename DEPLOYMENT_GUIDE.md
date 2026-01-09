# 🚀 DEPLOYMENT GUIDE - AI Network RCA Platform

## ✅ PREREQUISITES

- GitHub account
- Render.com account (free tier works)
- Azure OpenAI credentials
- Azure Storage account

---

## 📦 STEP 1: PUSH TO GITHUB (Already Done!)

Your code is at: https://github.com/Pratikshinde99/ai-network-rca

---

## 🌐 STEP 2: DEPLOY BACKEND TO RENDER

### 2.1 Create Web Service

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select repository: `ai-network-rca`
5. Click **"Connect"**

### 2.2 Configure Backend

**Basic Settings:**
- **Name:** `ai-network-rca-backend`
- **Region:** Singapore (closest to India)
- **Branch:** `main`
- **Root Directory:** `backend`
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app_local:app`

### 2.3 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these (get values from your `backend/local.settings.json`):

```
AZURE_OPENAI_ENDPOINT=YOUR_AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY=YOUR_AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT=YOUR_DEPLOYMENT_NAME
AZURE_STORAGE_CONNECTION_STRING=YOUR_STORAGE_CONNECTION_STRING
BLOB_CONTAINER_NAME=rca-reports
```

**Note:** Copy these values from your local `backend/local.settings.json` file.

### 2.4 Deploy

1. Select **"Free"** plan
2. Click **"Create Web Service"**
3. Wait 5-10 minutes for deployment
4. **Copy your backend URL** (e.g., `https://ai-network-rca-backend.onrender.com`)

---

## 💻 STEP 3: DEPLOY FRONTEND TO NETLIFY

### 3.1 Update Frontend Configuration

1. Open `frontend/.env.production`
2. Replace with your Render backend URL:
   ```
   REACT_APP_API_URL=https://YOUR-BACKEND-URL.onrender.com/api
   ```

### 3.2 Build Frontend

```powershell
cd frontend
npm install
npm run build
```

This creates a `build` folder with production files.

### 3.3 Deploy to Netlify

**Option A: Drag & Drop (Easiest)**
1. Go to https://app.netlify.com/drop
2. Drag the `frontend/build` folder to the page
3. Wait 30 seconds
4. **Your app is live!**

**Option B: GitHub Integration**
1. Go to https://app.netlify.com
2. Click "New site from Git"
3. Connect GitHub → Select `ai-network-rca`
4. Configure:
   - **Build command:** `npm run build`
   - **Publish directory:** `build`
   - **Base directory:** `frontend`
5. Add environment variable:
   ```
   REACT_APP_API_URL=https://YOUR-BACKEND-URL.onrender.com/api
   ```
6. Deploy!

---

## ✅ STEP 4: VERIFY DEPLOYMENT

### 4.1 Test Backend

```powershell
curl https://YOUR-BACKEND-URL.onrender.com/api/diagnose -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"target":"google.com","service_type":"web"}'
```

Should return diagnostic results.

### 4.2 Test Frontend

1. Open your Netlify URL
2. Enter `google.com`
3. Click "Run Diagnostics"
4. Should see full analysis with AI results!

---

## 🎯 DEPLOYMENT SUMMARY

| Component | Platform | URL |
|-----------|----------|-----|
| **Backend** | Render | `https://YOUR-BACKEND.onrender.com` |
| **Frontend** | Netlify | `https://YOUR-SITE.netlify.app` |
| **GitHub** | GitHub | `https://github.com/Pratikshinde99/ai-network-rca` |

---

## ⚠️ IMPORTANT NOTES

### Render Free Tier:
- Backend spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Perfect for demos and hackathons!

### Environment Variables:
- **Never commit** `local.settings.json` to GitHub
- Always use environment variables in production
- Render and Netlify handle secrets securely

---

## 🐛 TROUBLESHOOTING

### Backend Returns 404:
- Check start command: `gunicorn app_local:app`
- Verify root directory is `backend`
- Check Render logs for errors

### Frontend Can't Connect:
- Verify `REACT_APP_API_URL` is set correctly
- Check CORS is enabled in backend (already done)
- Rebuild frontend after changing env vars

### AI Analysis Fails:
- Verify Azure OpenAI credentials
- Check API key is valid
- Ensure deployment name matches

---

## 🚀 QUICK DEPLOYMENT CHECKLIST

- [ ] Code pushed to GitHub
- [ ] Backend deployed to Render
- [ ] Environment variables added to Render
- [ ] Backend URL copied
- [ ] Frontend `.env.production` updated
- [ ] Frontend built (`npm run build`)
- [ ] Frontend deployed to Netlify
- [ ] Both services tested
- [ ] Demo ready!

---

## 📞 SUPPORT

If you encounter issues:
1. Check Render logs (Dashboard → Logs)
2. Check browser console (F12)
3. Verify environment variables
4. Test backend directly with curl

---

**TOTAL DEPLOYMENT TIME: ~15 MINUTES** ⏱️

**Your app will be live and ready for your hackathon!** 🎉
