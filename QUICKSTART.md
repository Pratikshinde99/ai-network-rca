# ⚡ QUICK START GUIDE
## Get the demo running in 10 minutes

---

## 🔧 Prerequisites

Install these first:
- Python 3.9+ ([Download](https://www.python.org/downloads/))
- Node.js 16+ ([Download](https://nodejs.org/))
- Azure Functions Core Tools ([Install Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local))
- Git

---

## 🚀 LOCAL SETUP (Without Azure - For Testing)

### Step 1: Backend Setup (5 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create local settings (IMPORTANT!)
# Copy the example file
copy local.settings.json.example local.settings.json

# Edit local.settings.json and add your Azure OpenAI credentials:
# - AZURE_OPENAI_ENDPOINT
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_DEPLOYMENT

# Start Azure Function locally
func start
```

**Expected output:**
```
Functions:
    diagnose: [POST] http://localhost:7071/api/diagnose
    health: [GET] http://localhost:7071/api/health
```

### Step 2: Frontend Setup (3 minutes)

Open a NEW terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
copy .env.example .env

# The default API URL (http://localhost:7071/api) should work

# Start React app
npm start
```

**Expected output:**
```
Compiled successfully!
Local: http://localhost:3000
```

### Step 3: Test! (2 minutes)

1. Open browser: http://localhost:3000
2. Enter: `google.com`
3. Click "Run Diagnostics"
4. See results in ~5 seconds

---

## ☁️ AZURE SETUP (For Production Demo)

### Prerequisites

```bash
# Login to Azure
az login

# Set subscription (if you have multiple)
az account set --subscription "Your-Subscription-Name"
```

### 1. Create Azure Resources

```bash
# Set variables
$RESOURCE_GROUP="rg-network-rca"
$LOCATION="eastus"
$STORAGE_ACCOUNT="stnetworkrca$(Get-Random -Maximum 9999)"
$FUNCTION_APP="func-network-rca-$(Get-Random -Maximum 9999)"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create storage account
az storage account create `
  --name $STORAGE_ACCOUNT `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --sku Standard_LRS

# Create Function App
az functionapp create `
  --resource-group $RESOURCE_GROUP `
  --consumption-plan-location $LOCATION `
  --runtime python `
  --runtime-version 3.9 `
  --functions-version 4 `
  --name $FUNCTION_APP `
  --storage-account $STORAGE_ACCOUNT `
  --os-type Linux
```

### 2. Create Azure OpenAI Resource

**Option A: Azure Portal**
1. Go to portal.azure.com
2. Create "Azure OpenAI" resource
3. Deploy GPT-4 model
4. Copy endpoint and key

**Option B: CLI** (if available in your region)
```bash
az cognitiveservices account create `
  --name "openai-network-rca" `
  --resource-group $RESOURCE_GROUP `
  --location "eastus" `
  --kind OpenAI `
  --sku S0
```

### 3. Create Blob Container

```bash
# Get connection string
$CONNECTION_STRING=$(az storage account show-connection-string `
  --name $STORAGE_ACCOUNT `
  --resource-group $RESOURCE_GROUP `
  --query connectionString -o tsv)

# Create container
az storage container create `
  --name "rca-reports" `
  --connection-string $CONNECTION_STRING `
  --public-access blob
```

### 4. Configure Function App

```bash
az functionapp config appsettings set `
  --name $FUNCTION_APP `
  --resource-group $RESOURCE_GROUP `
  --settings `
    AZURE_OPENAI_ENDPOINT="https://your-openai.openai.azure.com/" `
    AZURE_OPENAI_API_KEY="your-api-key" `
    AZURE_OPENAI_DEPLOYMENT="gpt-4" `
    AZURE_STORAGE_CONNECTION_STRING="$CONNECTION_STRING" `
    BLOB_CONTAINER_NAME="rca-reports"
```

### 5. Deploy Function

```bash
cd backend
func azure functionapp publish $FUNCTION_APP
```

### 6. Update Frontend

```bash
cd frontend

# Update .env with production URL
# REACT_APP_API_URL=https://func-network-rca-xxxx.azurewebsites.net/api

# Build for production
npm run build

# Deploy to Azure Static Web Apps or App Service
# (See Azure Portal for deployment options)
```

---

## 🧪 TESTING

### Test Backend Directly

```bash
# Health check
curl http://localhost:7071/api/health

# Run diagnostic
curl -X POST http://localhost:7071/api/diagnose `
  -H "Content-Type: application/json" `
  -d '{"target": "google.com", "service_type": "web"}'
```

### Test Frontend

1. Open http://localhost:3000
2. Try these targets:
   - `google.com` (should pass)
   - `github.com` (should pass)
   - `nonexistent-xyz.com` (DNS fail)
   - `google.com:9999` (port fail)

---

## 🐛 TROUBLESHOOTING

### Backend won't start
- Check Python version: `python --version` (need 3.9+)
- Check Azure Functions Core Tools: `func --version`
- Verify `local.settings.json` exists
- Check if port 7071 is available

### Frontend won't start
- Check Node version: `node --version` (need 16+)
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

### Diagnostics fail
- Check internet connectivity
- Try a different target domain
- Check Azure OpenAI credentials in `local.settings.json`
- Look at backend console for error messages

### AI analysis not working
- Verify Azure OpenAI endpoint and key
- Check deployment name matches your GPT-4 deployment
- Look for error messages in backend console
- System will fall back to rule-based analysis if AI fails

### CORS errors
- Make sure backend is running on port 7071
- Check `.env` in frontend has correct API URL
- Verify CORS headers in `function_app.py`

---

## 📝 CONFIGURATION CHECKLIST

Before demo:
- [ ] Azure OpenAI credentials configured
- [ ] Backend running on port 7071
- [ ] Frontend running on port 3000
- [ ] Internet connectivity working
- [ ] Tested with `google.com`
- [ ] Tested with fake domain
- [ ] Download report works

---

## 🎯 DEMO-READY CHECKLIST

- [ ] Both backend and frontend running
- [ ] No errors in console
- [ ] Tested all three demo scenarios
- [ ] Browser cache cleared
- [ ] Full screen mode ready
- [ ] Zoom level at 100%
- [ ] Backup plan ready (screenshots/video)

---

## 📞 NEED HELP?

Common issues and solutions:

**"Module not found" errors:**
```bash
# Backend
pip install -r requirements.txt --force-reinstall

# Frontend
npm install --force
```

**"Port already in use":**
```bash
# Change backend port in host.json
# Change frontend port: set PORT=3001 && npm start
```

**"Azure OpenAI quota exceeded":**
- Use rule-based fallback (already implemented)
- Or use a different Azure OpenAI resource

---

**You're ready to demo! 🎉**
