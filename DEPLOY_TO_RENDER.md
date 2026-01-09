# 🚀 DEPLOY TO RENDER - EASIEST SOLUTION

## ✅ YOUR PROJECT IS READY!

Forget Azure - let's use **Render.com** which is 100x easier!

---

## 📋 STEP-BY-STEP DEPLOYMENT (10 MINUTES):

### **STEP 1: Create Render Account**

1. Go to: https://render.com
2. Click "Get Started"
3. Sign up with GitHub (use your Pratikshinde99 account)

---

### **STEP 2: Deploy Backend (Python)**

1. **In Render Dashboard**, click "New +" → "Web Service"

2. **Connect GitHub:**
   - Select your repository: `ai-network-rca`
   - Click "Connect"

3. **Configure Backend:**
   - **Name:** `ai-network-rca-backend`
   - **Region:** Singapore (closest to India)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m uvicorn function_app:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"
   
   Add these (get values from your `backend/local.settings.json`):
   ```
   AZURE_OPENAI_ENDPOINT = YOUR_AZURE_OPENAI_ENDPOINT
   AZURE_OPENAI_API_KEY = YOUR_AZURE_OPENAI_API_KEY
   AZURE_OPENAI_DEPLOYMENT = YOUR_DEPLOYMENT_NAME
   AZURE_STORAGE_CONNECTION_STRING = YOUR_STORAGE_CONNECTION_STRING
   BLOB_CONTAINER_NAME = rca-reports
   ```

5. **Select Free Plan**

6. **Click "Create Web Service"**

7. **Wait 5 minutes** for deployment

8. **Copy your backend URL** (e.g., `https://ai-network-rca-backend.onrender.com`)

---

### **STEP 3: Update Frontend**

1. **Update `.env.production`:**
   ```
   REACT_APP_API_URL=https://YOUR-RENDER-BACKEND-URL.onrender.com/api
   ```

2. **Rebuild frontend:**
   ```powershell
   cd frontend
   npm run build
   ```

---

### **STEP 4: Deploy Frontend to Netlify**

1. **Go to:** https://app.netlify.com/drop

2. **Drag the `frontend/build` folder**

3. **Your app is live!**

---

## 🎯 ALTERNATIVE: DEPLOY BOTH TO RENDER

### **Deploy Frontend to Render:**

1. **In Render**, click "New +" → "Static Site"

2. **Connect GitHub** → Select `ai-network-rca`

3. **Configure:**
   - **Name:** `ai-network-rca-frontend`
   - **Branch:** `main`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `build`

4. **Add Environment Variable:**
   ```
   REACT_APP_API_URL = https://YOUR-BACKEND-URL.onrender.com/api
   ```

5. **Click "Create Static Site"**

6. **Wait 3 minutes**

7. **Your app is live!**

---

## ✅ THAT'S IT!

**Render handles everything automatically:**
- ✅ Auto-deploys on git push
- ✅ Free SSL certificates
- ✅ No CORS issues
- ✅ Simple environment variables
- ✅ Free tier available

---

## 🚨 IMPORTANT NOTE:

**Render's free tier:**
- Backend spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Perfect for hackathon demos!

---

**START WITH STEP 1 - CREATE RENDER ACCOUNT!** 🚀
