# 🎯 WHAT YOU NEED TO PROVIDE

## ✅ Setup Complete!

I've successfully set up your project:
- ✅ Python virtual environment created
- ✅ Backend dependencies installed
- ✅ Frontend dependencies installed
- ✅ Configuration files created

---

## 🔑 REQUIRED: Azure OpenAI Credentials

To run the application, you need to provide **Azure OpenAI credentials**.

### Where to Get Them:

#### Option 1: If You Have Azure OpenAI Already
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Go to "Keys and Endpoint" section
4. Copy the following:
   - **Endpoint** (looks like: `https://your-resource.openai.azure.com/`)
   - **API Key** (a long string of characters)
   - **Deployment Name** (usually `gpt-4` or `gpt-35-turbo`)

#### Option 2: If You Don't Have Azure OpenAI
You need to create an Azure OpenAI resource:

1. **Sign up for Azure** (if you don't have an account):
   - Go to [Azure Free Account](https://azure.microsoft.com/free/)
   - Students get $100 free credits

2. **Create Azure OpenAI Resource**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Click "Create a resource"
   - Search for "Azure OpenAI"
   - Click "Create"
   - Fill in the details:
     - Resource group: Create new (e.g., "rg-network-rca")
     - Region: Choose closest to you (e.g., "East US")
     - Name: Choose a unique name (e.g., "openai-network-rca")
     - Pricing tier: Standard S0
   - Click "Review + Create"

3. **Deploy GPT-4 Model**:
   - Go to your Azure OpenAI resource
   - Click "Go to Azure OpenAI Studio"
   - Go to "Deployments" → "Create new deployment"
   - Select model: `gpt-4` (or `gpt-35-turbo` if GPT-4 not available)
   - Deployment name: `gpt-4`
   - Click "Create"

4. **Get Credentials**:
   - Go back to Azure Portal
   - Your Azure OpenAI resource → "Keys and Endpoint"
   - Copy Endpoint and Key

---

## 📝 HOW TO PROVIDE THE CREDENTIALS

### Step 1: Open Configuration File
The file is already created at:
```
backend/local.settings.json
```

### Step 2: Replace These Values

Open `backend/local.settings.json` and replace:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_OPENAI_ENDPOINT": "REPLACE_WITH_YOUR_ENDPOINT",     ← Replace this
    "AZURE_OPENAI_API_KEY": "REPLACE_WITH_YOUR_API_KEY",       ← Replace this
    "AZURE_OPENAI_DEPLOYMENT": "gpt-4",                        ← Replace if different
    "AZURE_STORAGE_CONNECTION_STRING": "",                     ← Leave empty for now
    "BLOB_CONTAINER_NAME": "rca-reports"
  }
}
```

### Example (with fake values):
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_OPENAI_ENDPOINT": "https://my-openai-resource.openai.azure.com/",
    "AZURE_OPENAI_API_KEY": "abc123def456ghi789jkl012mno345pqr678stu901vwx234",
    "AZURE_OPENAI_DEPLOYMENT": "gpt-4",
    "AZURE_STORAGE_CONNECTION_STRING": "",
    "BLOB_CONTAINER_NAME": "rca-reports"
  }
}
```

**Important Notes:**
- The endpoint must end with `/`
- The API key is a long string (32+ characters)
- The deployment name must match what you created in Azure OpenAI Studio
- You can leave `AZURE_STORAGE_CONNECTION_STRING` empty for now (blob storage is optional)

---

## 🚀 HOW TO RUN THE APPLICATION

Once you've added your Azure OpenAI credentials:

### Terminal 1: Start Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
func start
```

**Expected output:**
```
Functions:
    diagnose: [POST] http://localhost:7071/api/diagnose
    health: [GET] http://localhost:7071/api/health
```

### Terminal 2: Start Frontend
```powershell
cd frontend
npm start
```

**Expected output:**
```
Compiled successfully!
Local: http://localhost:3000
```

### Browser
- Open: http://localhost:3000
- Enter: `google.com`
- Click: "Run Diagnostics"
- See results in ~5 seconds!

---

## 🧪 TEST WITHOUT AZURE OPENAI (Temporary)

If you don't have Azure OpenAI credentials yet, the system will use **rule-based fallback** analysis instead of AI. It will still work, but won't use GPT-4.

To test:
1. Leave the placeholder values in `local.settings.json`
2. Start the backend and frontend as shown above
3. The diagnostics will run, but AI analysis will use simple rules instead of GPT-4

---

## ❓ TROUBLESHOOTING

### "Azure Functions Core Tools not found"
Install from: https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local

### "Invalid API key" error
- Double-check you copied the entire key
- Make sure there are no extra spaces
- Verify the endpoint ends with `/`

### "Deployment not found" error
- Check the deployment name in Azure OpenAI Studio
- Make sure it matches exactly (case-sensitive)

### Backend won't start
- Make sure you activated the virtual environment: `.\venv\Scripts\Activate.ps1`
- Check if port 7071 is available

### Frontend won't start
- Check if port 3000 is available
- Try: `npm install --force` if there are dependency issues

---

## 📞 WHAT TO TELL ME

If you need help, provide:

1. **Do you have Azure OpenAI?**
   - Yes/No

2. **If Yes, provide:**
   - Endpoint (e.g., `https://xxx.openai.azure.com/`)
   - Deployment name (e.g., `gpt-4`)
   - (Don't share the API key publicly - just confirm you have it)

3. **If No:**
   - Do you have an Azure account?
   - Are you a student (for free credits)?
   - Do you want to create one, or run without AI for now?

---

## 🎯 NEXT STEPS

1. **Get Azure OpenAI credentials** (see above)
2. **Edit `backend/local.settings.json`** with your credentials
3. **Run the application** (see commands above)
4. **Test it** with `google.com`
5. **Practice your demo** using `DEMO_SCRIPT.md`

---

**You're almost there! Just need those Azure OpenAI credentials and you're ready to go! 🚀**
