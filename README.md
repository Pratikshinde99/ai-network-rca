# 🚀 AI-Powered Network RCA Platform

**Real-time network diagnostics with Azure OpenAI intelligence**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

---

## ✨ Features

- 🔍 **Real Network Diagnostics** - DNS, TCP, HTTP, Latency tests
- 🧠 **AI-Powered Analysis** - Azure OpenAI GPT-4 root cause analysis
- 📊 **Enterprise Features** - Incident context, change awareness, responsibility classification
- 📄 **Multi-Format Reports** - Technical, Executive, and JSON reports
- ☁️ **Cloud Storage** - Azure Blob Storage for report persistence

---

## 🏗️ Architecture

```
Frontend (React) → Backend (Python) → Network Diagnostics
                                    ↓
                              Azure OpenAI (GPT-4)
                                    ↓
                              RCA Reports → Blob Storage
```

---

## 📦 Project Structure

```
ai-network-rca/
├── backend/              # Python backend
│   ├── function_app.py   # Main entry point
│   ├── diagnostics.py    # Network tests
│   ├── ai_analyzer.py    # AI integration
│   └── rca_generator.py  # Report generation
├── frontend/             # React frontend
│   ├── src/
│   │   ├── App.js        # Main component
│   │   └── App.css       # Styling
│   └── public/
└── README.md
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Node.js 18+
- Azure OpenAI account
- Azure Storage account

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Create local.settings.json with your credentials
# See CREDENTIALS_NEEDED.md for details

# Run locally
func start --cors http://localhost:3000
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Visit: http://localhost:3000

---

## 🌐 Deploy to Render

### Step 1: Deploy Backend

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `ai-network-rca-backend`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** (leave blank - auto-detected)

5. Add Environment Variables:
   ```
   AZURE_OPENAI_ENDPOINT=your-endpoint
   AZURE_OPENAI_API_KEY=your-key
   AZURE_OPENAI_DEPLOYMENT=your-deployment
   AZURE_STORAGE_CONNECTION_STRING=your-connection-string
   BLOB_CONTAINER_NAME=rca-reports
   ```

6. Click "Create Web Service"
7. Copy your backend URL (e.g., `https://ai-network-rca-backend.onrender.com`)

### Step 2: Deploy Frontend

1. Update `frontend/.env.production`:
   ```
   REACT_APP_API_URL=https://YOUR-BACKEND-URL.onrender.com/api
   ```

2. In Render, click "New +" → "Static Site"
3. Connect your repository
4. Configure:
   - **Name:** `ai-network-rca-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `build`

5. Add Environment Variable:
   ```
   REACT_APP_API_URL=https://YOUR-BACKEND-URL.onrender.com/api
   ```

6. Click "Create Static Site"

**Done! Your app is live!** 🎉

---

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [DEPLOY_TO_RENDER.md](DEPLOY_TO_RENDER.md) - Detailed deployment guide
- [ENTERPRISE_FEATURES.md](ENTERPRISE_FEATURES.md) - Enterprise features documentation
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing guide with 50+ test cases
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [CREDENTIALS_NEEDED.md](CREDENTIALS_NEEDED.md) - Required credentials

---

## 🧪 Testing

### Test Scenarios

1. **Success:** `google.com` → All tests pass
2. **DNS Failure:** `nonexistent-domain.com` → DNS fails
3. **Port Blocked:** `google.com:9999` → TCP fails
4. **Enterprise Context:** Add incident metadata for advanced analysis

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive test cases.

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Azure Functions
- Azure OpenAI (GPT-4)
- Azure Blob Storage

**Frontend:**
- React 18
- Axios
- Modern CSS

**Diagnostics:**
- DNS Resolution (socket)
- TCP Connectivity (socket)
- HTTP/HTTPS Status (requests)
- Latency Measurement

---

## 🔒 Security

- Environment variables for sensitive data
- CORS configuration
- Input validation
- Secure credential storage

---

## 📊 Enterprise Features

1. **Incident Context Awareness** - Capture timing, detection, user impact
2. **Change-Aware RCA** - Correlate recent changes with failures
3. **Dual RCA Output** - Technical, Executive, and JSON reports
4. **Responsibility Classification** - Auto-assign to correct team

---

## 🏆 Perfect for Hackathons!

- ✅ Production-ready code
- ✅ Professional UI/UX
- ✅ Real AI integration
- ✅ Enterprise-grade features
- ✅ Easy to deploy
- ✅ Well-documented

---

## 📝 License

MIT License

---

## 👥 Team

Built for Microsoft Imagine Cup 2026

---

**🚀 Deploy now and win your hackathon!**
