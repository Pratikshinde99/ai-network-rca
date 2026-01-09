# 🏗️ SYSTEM ARCHITECTURE
## AI-Powered Network RCA Platform

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    React Frontend                         │  │
│  │  - Input form (domain/IP)                                │  │
│  │  - Real-time results display                             │  │
│  │  - AI analysis visualization                             │  │
│  │  - Report download                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                         HTTP POST                               │
│                              ▼                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      AZURE FUNCTIONS                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  function_app.py (HTTP Trigger)                          │  │
│  │  - Request validation                                     │  │
│  │  - Orchestration logic                                    │  │
│  │  - Response formatting                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│              ┌───────────────┼───────────────┐                 │
│              ▼               ▼               ▼                 │
│  ┌─────────────────┐ ┌──────────────┐ ┌──────────────────┐   │
│  │  diagnostics.py │ │ai_analyzer.py│ │rca_generator.py  │   │
│  │                 │ │              │ │                  │   │
│  │ - DNS check     │ │ - AI prompt  │ │ - Report format  │   │
│  │ - TCP check     │ │ - OpenAI API │ │ - Blob upload    │   │
│  │ - HTTP check    │ │ - Fallback   │ │ - JSON/Text      │   │
│  │ - Latency test  │ │   logic      │ │                  │   │
│  └─────────────────┘ └──────────────┘ └──────────────────┘   │
│                              │                     │            │
└──────────────────────────────┼─────────────────────┼────────────┘
                               │                     │
                               ▼                     ▼
                    ┌──────────────────┐  ┌──────────────────┐
                    │  Azure OpenAI    │  │  Azure Blob      │
                    │                  │  │  Storage         │
                    │  - GPT-4 Model   │  │                  │
                    │  - Analysis      │  │  - RCA Reports   │
                    │  - Reasoning     │  │  - Audit Trail   │
                    └──────────────────┘  └──────────────────┘
```

---

## 🔄 REQUEST FLOW

### 1. User Input
```
User enters: "google.com"
Frontend validates and sends POST to /api/diagnose
```

### 2. Azure Function Receives Request
```python
{
  "target": "google.com",
  "service_type": "web"
}
```

### 3. Network Diagnostics Execution
```
Step 1: DNS Resolution
├─ Success → Continue
└─ Failure → Infer downstream failures

Step 2: TCP Connectivity (port 443)
├─ Success → Continue
└─ Failure → Infer HTTP failure

Step 3: HTTP/HTTPS Request
├─ Success → Continue
└─ Failure → Log error

Step 4: Latency Measurement
└─ Multiple samples for accuracy
```

### 4. Diagnostic Results Structure
```json
[
  {
    "test_name": "DNS_RESOLUTION",
    "status": "PASS",
    "latency_ms": 12.5,
    "details": {
      "hostname": "google.com",
      "ip_address": "142.250.185.46"
    },
    "failure_reason": null
  },
  {
    "test_name": "TCP_CONNECTIVITY",
    "status": "PASS",
    "latency_ms": 45.2,
    "details": {
      "hostname": "google.com",
      "port": 443
    },
    "failure_reason": null
  }
  // ... more tests
]
```

### 5. AI Analysis
```
Azure OpenAI receives:
- Target domain
- Structured diagnostic results
- System prompt (network engineer persona)

Returns:
- Root cause identification
- Confidence percentage
- Detailed reasoning
- Evidence list
- Remediation steps
```

### 6. RCA Report Generation
```
Combines:
- Diagnostic results
- AI analysis
- Timestamp
- Severity classification

Outputs:
- Formatted text report
- JSON structure
- Blob storage upload
```

### 7. Response to Frontend
```json
{
  "target": "google.com",
  "timestamp": "2026-01-08T11:30:00Z",
  "diagnostics": [...],
  "ai_analysis": {
    "root_cause": "No issues detected",
    "confidence_percentage": 95,
    "reasoning": "...",
    "evidence": [...],
    "remediation_steps": [...]
  },
  "rca_report": "=== FULL TEXT REPORT ===",
  "report_url": "https://storage.blob.core.windows.net/..."
}
```

---

## 🧩 COMPONENT DETAILS

### Frontend (React)
**Technology:** React 18, Axios  
**Responsibilities:**
- User input collection
- API communication
- Results visualization
- Report download
- Error handling

**Key Features:**
- Real-time loading states
- Responsive design
- Color-coded status indicators
- Confidence meter visualization
- One-click report download

---

### Backend (Azure Functions)
**Technology:** Python 3.9, Azure Functions v4  
**Responsibilities:**
- HTTP request handling
- Diagnostic orchestration
- AI integration
- Report generation
- Blob storage management

**Key Features:**
- Serverless auto-scaling
- CORS support
- Error handling
- Structured logging
- Health check endpoint

---

### Diagnostics Module
**Technology:** Python socket, requests library  
**Responsibilities:**
- DNS resolution (socket.gethostbyname)
- TCP connectivity (socket.connect_ex)
- HTTP status (requests.get)
- Latency measurement (timing)

**Intelligence:**
- Failure inference (DNS fail → all fail)
- Multiple latency samples
- Timeout handling
- SSL/TLS support

---

### AI Analyzer
**Technology:** Azure OpenAI GPT-4  
**Responsibilities:**
- Root cause identification
- Confidence scoring
- Evidence extraction
- Remediation suggestions

**Features:**
- Deterministic prompting (low temperature)
- JSON response format
- Rule-based fallback
- Context-aware reasoning

---

### RCA Generator
**Technology:** Python, Azure Blob Storage SDK  
**Responsibilities:**
- Report formatting
- Blob upload
- URL generation
- Audit trail

**Output Formats:**
- Plain text (primary)
- JSON (API response)
- PDF (future enhancement)

---

## 🔐 SECURITY ARCHITECTURE

### Authentication & Authorization
```
Frontend → Azure Function: Public (demo)
Azure Function → OpenAI: API Key (env var)
Azure Function → Blob: Connection String (env var)
```

**Production Recommendations:**
- Azure AD authentication
- Managed Identity for Azure resources
- API key rotation
- Rate limiting
- Input validation

---

### Data Flow Security
```
User Input → Validation → Sanitization → Processing
                ↓
         No PII stored
                ↓
    Reports stored in private blob
                ↓
         Audit logging enabled
```

---

## 📈 SCALABILITY

### Current Architecture
- **Concurrent Users:** 100+ (Azure Functions auto-scale)
- **Response Time:** 3-10 seconds
- **Cost:** Pay-per-execution (serverless)

### Optimization Strategies
1. **Caching:** Redis for frequent targets
2. **Batch Processing:** Queue-based for bulk diagnostics
3. **CDN:** Static frontend hosting
4. **Multi-Region:** Geo-distributed diagnostics

---

## 🎯 DESIGN DECISIONS

### Why Azure Functions?
✅ Serverless (no infrastructure management)  
✅ Auto-scaling  
✅ Pay-per-use pricing  
✅ Built-in monitoring  
✅ Easy CI/CD integration  

### Why Azure OpenAI?
✅ Enterprise-grade security  
✅ Data residency compliance  
✅ Integration with Azure ecosystem  
✅ GPT-4 access  
✅ Deterministic API  

### Why Blob Storage?
✅ Cheap, durable storage  
✅ Direct URL access  
✅ Audit trail capability  
✅ Lifecycle management  
✅ Easy integration  

### Why React?
✅ Fast development  
✅ Component reusability  
✅ Rich ecosystem  
✅ Easy deployment  
✅ Great for demos  

---

## 🔮 FUTURE ENHANCEMENTS

### Phase 2
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Historical trend analysis
- [ ] Multi-target batch diagnostics

### Phase 3
- [ ] More protocols (SSH, FTP, SMTP)
- [ ] Database connectivity checks
- [ ] Custom diagnostic plugins
- [ ] Webhook integrations

### Phase 4
- [ ] Machine learning for anomaly detection
- [ ] Predictive failure analysis
- [ ] Integration with monitoring tools
- [ ] Mobile app

---

## 📊 MONITORING & OBSERVABILITY

### Application Insights
```
Metrics tracked:
- Request count
- Response time
- Failure rate
- AI API latency
- Diagnostic success rate
```

### Logging Strategy
```
INFO:  Successful operations
WARN:  Fallback to rule-based analysis
ERROR: API failures, timeouts
DEBUG: Detailed diagnostic data
```

---

## 💰 COST ESTIMATION

### Azure Resources (Monthly)
```
Azure Functions:     $0-10   (1M executions free tier)
Azure OpenAI:        $10-50  (depends on usage)
Blob Storage:        $1-5    (minimal storage)
Bandwidth:           $5-20   (depends on traffic)
─────────────────────────────
Total:               $16-85/month
```

**Hackathon Demo:** Essentially FREE (free tiers)

---

**This architecture is production-ready and demo-optimized! 🚀**
