# MediWise AI Assistant

**AI-Powered Medical Diagnosis Assistant for ERPNext Healthcare**

MediWise is an intelligent medical assistant that integrates with ERPNext Healthcare to provide doctors with AI-powered patient analysis, diagnosis support, and clinical decision-making assistance.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           MediWise Architecture                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────────────┐      ┌──────────────────┐      ┌──────────────┐  │
│   │                  │      │                  │      │              │  │
│   │  Web Interface   │◄────►│  Frappe Server   │◄────►│  n8n Cloud   │  │
│   │  (HTML/JS/CSS)   │      │  Script (API)    │      │  (AI Core)   │  │
│   │                  │      │                  │      │              │  │
│   └────────┬─────────┘      └────────┬─────────┘      └──────────────┘  │
│            │                         │                                   │
│            │                         ▼                                   │
│            │                ┌──────────────────┐                        │
│            │                │                  │                        │
│            └───────────────►│  ERPNext         │                        │
│                             │  Healthcare      │                        │
│                             │  Database        │                        │
│                             │                  │                        │
│                             └──────────────────┘                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Overview

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Web Interface** | HTML, CSS, JavaScript | User-facing medical assistant UI |
| **Server Script** | Python (Frappe API) | Data retrieval & AI orchestration |
| **Database** | ERPNext Healthcare | Patient records, encounters, appointments |
| **AI Core** | n8n Workflow | RAG-based intelligent responses |

---

## 💡 Why Frappe + HTML? The Power of Simplicity

### The Problem with Traditional Approaches

Building web applications with complex backend logic typically requires:
- **Separate frontend frameworks** (React, Vue, Angular)
- **Separate backend APIs** (Node.js, Django, FastAPI)
- **Complex deployment pipelines** (Docker, Kubernetes, CI/CD)
- **Multiple repositories** and tech stacks to maintain
- **CORS configuration** and authentication headaches
- **Significant development overhead** for simple use cases

### The Frappe + HTML Solution

MediWise demonstrates that **you don't need a complex frontend framework** to build sophisticated web applications. By leveraging Frappe's native capabilities with plain HTML/CSS/JavaScript, you get:

#### ✅ **Zero Build Process**
- No webpack, vite, or bundler configuration
- No `npm install` with thousands of dependencies
- No build errors or version conflicts
- Just paste HTML and it works

#### ✅ **Native Authentication & Security**
- Frappe handles user sessions automatically
- CSRF protection built-in
- Role-based access control inherited from ERPNext
- No separate auth system to maintain

#### ✅ **Direct Database Access**
- Server Scripts can query any ERPNext doctype
- Full access to Frappe ORM
- No need for separate API development
- Real-time data without complex integrations

#### ✅ **Single Deployment**
- UI and backend deploy together
- No separate hosting for frontend
- No CORS issues (same origin)
- Updates are instant—just edit and save

#### ✅ **Complex Backend, Simple Frontend**
```
┌─────────────────────────────────────────────────────────────────┐
│                    Traditional Approach                          │
├─────────────────────────────────────────────────────────────────┤
│  React App → REST API → Django → PostgreSQL → External Services │
│     ↓           ↓          ↓          ↓              ↓          │
│  Build      Auth       ORM       Migrations     Integrations    │
│  Deploy     CORS       Routes    Hosting        More APIs       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Frappe + HTML Approach                        │
├─────────────────────────────────────────────────────────────────┤
│  HTML Page → Server Script → ERPNext Database → n8n Webhook     │
│     ↓              ↓               ↓                 ↓          │
│  Paste &      frappe.*        Already there     One URL         │
│  Done         methods         with data                          │
└─────────────────────────────────────────────────────────────────┘
```

### When This Approach Shines

| Use Case | Why Frappe + HTML Works |
|----------|-------------------------|
| **Internal Tools** | Users already logged into ERPNext |
| **Data-Heavy Apps** | Direct access to ERPNext data |
| **AI/Chatbot Interfaces** | Simple UI, complex backend logic |
| **Dashboards** | Quick deployment, easy updates |
| **Form-Based Apps** | Frappe handles validation |
| **Portal Extensions** | Extend ERPNext without custom apps |

### MediWise as a Case Study

MediWise proves this architecture works for **production applications**:

- **~3000 lines of HTML/CSS/JS** — handles complex medical UI
- **~600 lines of Python** — Server Script for all backend logic
- **Zero external dependencies** — no node_modules, no package.json
- **Complex features**: Real-time search, file uploads, AI chat, markdown rendering
- **Enterprise-grade**: Works with ERPNext Healthcare's complex data model
- **Maintainable**: Single file to update, no build process

### The Bottom Line

> **"You don't always need a React app. Sometimes, HTML + a good backend is all you need."**

Frappe's Server Script + Web Page combination lets you build sophisticated applications while:
- Reducing complexity by 10x
- Eliminating frontend build tooling
- Leveraging existing ERPNext infrastructure
- Deploying in minutes, not hours

This approach is ideal for teams already using ERPNext who need custom interfaces without the overhead of modern frontend frameworks.

---

## 🖥️ Web Interface (`ai-bot-interface.html`)

### Overview

The web interface is a single-page application (SPA) built with vanilla HTML, CSS, and JavaScript. It provides a professional medical-grade UI for doctors to interact with patient data and the AI assistant.

### Key Features

- **Two-Panel Layout**: Patient information (left) + AI Chat (right)
- **Real-time Patient Search**: Search and select patients from ERPNext
- **Patient Information Display**: Demographics, encounters, appointments, lab tests
- **AI Chat Interface**: Conversational interface with markdown support
- **File Upload**: Upload medical images and documents for AI analysis
- **Responsive Design**: Works on desktop and tablet devices

### Deployment with Frappe

The HTML interface can be deployed in Frappe/ERPNext in several ways:

#### Option 1: Web Page (Recommended)

1. Go to **ERPNext → Website → Web Page → New**
2. Set the Route (e.g., `mediwise`)
3. Enable "Show Title" = No
4. In the "Main Section HTML" field, paste the entire HTML content
5. Save and publish
6. Access at: `https://your-site.com/mediwise`

#### Option 2: Custom App Page

1. Create a custom Frappe app
2. Add the HTML file to `{app}/www/mediwise.html`
3. The page will be available at `/mediwise`

#### Option 3: Portal Page

1. Add as a portal page in your custom app
2. Configure in `hooks.py` under `website_route_rules`

### Technologies Used

- **Google Fonts**: Inter (UI) + JetBrains Mono (code)
- **Marked.js**: Markdown rendering for AI responses
- **Lottie**: Loading animations
- **Frappe API**: Communication with backend

---

## ⚙️ Server Script (`server_script.py`)

### Overview

The server script is a Frappe API Server Script that acts as the middleware between the web interface and both the ERPNext database and the n8n AI workflow.

### Purpose

1. **Data Retrieval**: Fetch patient data from ERPNext Healthcare
2. **AI Orchestration**: Send queries to n8n and return AI responses
3. **Authentication**: Handle API authentication and CSRF tokens
4. **Data Transformation**: Prepare patient context for AI analysis

### Deployment in Frappe

1. Navigate to **ERPNext → Server Script → New**
2. Configure:
   - **Script Name**: MediWise AI Bot
   - **Script Type**: API
   - **API Method**: `mediwise_bot.query`
3. Paste the entire `server_script.py` content
4. Update `N8N_WEBHOOK_URL` with your n8n webhook URL
5. Enable and Save

### API Endpoints

The server script exposes a single API endpoint that handles multiple query types:

```
POST /api/method/mediwise_bot.query
```

| Query Type | Description |
|------------|-------------|
| `ai_query` | Send query to AI with patient context |
| `search_patients` | Search patients by name/ID |
| `get_patient_summary` | Get comprehensive patient data |
| `get_patient_details` | Get basic patient information |
| `get_patient_encounters` | Get patient encounter history |
| `get_active_prescriptions` | Get current medications |
| `get_lab_tests` | Get lab test results |
| `get_vital_signs_history` | Get vital signs history |

### Request Format

```json
{
  "query_type": "ai_query",
  "parameters": {
    "patient_id": "PAT-001",
    "user_query": "What are the key concerns for this patient?",
    "patient_context": { ... },
    "session_id": "unique-session-id"
  }
}
```

### Response Format

```json
{
  "status": "success",
  "query_type": "ai_query",
  "data": {
    "ai_response": "Based on the patient's history...",
    "model_used": "RAG (n8n)"
  }
}
```

---

## 🤖 AI Core (n8n)

### Overview

The AI intelligence is powered by **n8n**, a workflow automation platform. The n8n workflow implements a RAG (Retrieval-Augmented Generation) system that processes patient data and generates intelligent medical insights.

### Why n8n?

- **Visual Workflow Builder**: Easy to modify AI logic without code
- **Flexible LLM Integration**: Connect to OpenAI, Anthropic, or custom models
- **Memory Management**: Built-in session memory for conversational context
- **Scalability**: Cloud-hosted with automatic scaling
- **Extensibility**: Easy to add tools, functions, and integrations

### Webhook Configuration

The server script communicates with n8n via a webhook:

```python
N8N_WEBHOOK_URL = "https://your-n8n-instance/webhook/your-webhook-id"
```

### Expected Webhook Interface

**Request** (from Server Script):
```json
{
  "sessionId": "patient_PAT001_1234567890",
  "chatInput": "COMPLETE PATIENT DATA (RAW JSON):\n{...}\n\nDOCTOR'S QUESTION:\nWhat are the key concerns?"
}
```

**Response** (from n8n):
```json
{
  "output": "Based on the patient's medical history, here are the key concerns..."
}
```

### n8n Workflow Structure (Recommended)

```
Webhook Trigger → AI Agent Node → Response Node
                       ↓
              Memory (Session-based)
                       ↓
              LLM (OpenAI/Anthropic)
```

---

## 📊 Data Flow

```
1. Doctor selects patient in Web Interface
                    ↓
2. Interface calls Server Script API (get_patient_summary)
                    ↓
3. Server Script fetches data from ERPNext Healthcare
                    ↓
4. Patient data displayed in Interface
                    ↓
5. Doctor asks question or requests analysis
                    ↓
6. Interface sends query + patient context to Server Script
                    ↓
7. Server Script forwards to n8n webhook
                    ↓
8. n8n processes with RAG/LLM
                    ↓
9. AI response returned through chain
                    ↓
10. Response displayed in chat interface
```

---

## 🚀 Quick Start Deployment

### Prerequisites

- ERPNext with Healthcare module installed
- n8n cloud account (or self-hosted n8n)
- API credentials for ERPNext

### Step 1: Deploy Server Script

```bash
# In ERPNext
1. Go to Server Script → New
2. Name: MediWise AI Bot
3. Type: API
4. Method: mediwise_bot.query
5. Paste server_script.py content
6. Save & Enable
```

### Step 2: Configure n8n Webhook

1. Create n8n workflow with webhook trigger
2. Copy webhook URL
3. Update `N8N_WEBHOOK_URL` in server script
4. Build your RAG workflow in n8n

### Step 3: Deploy Web Interface

```bash
# In ERPNext
1. Go to Web Page → New
2. Route: mediwise
3. Paste ai-bot-interface.html content
4. Update API credentials in CONFIG section
5. Save & Publish
```

### Step 4: Configure API Credentials

In `ai-bot-interface.html`, update:

```javascript
const CONFIG = {
    FRAPPE_BASE_URL: window.location.origin,
    API_METHOD: '/api/method/mediwise_bot.query',
    API_KEY: 'your-api-key',
    API_SECRET: 'your-api-secret'
};
```

Generate API keys:
```python
# In bench console
user = frappe.get_doc("User", "your@email.com")
api_key, api_secret = user.generate_keys()
print(f"API Key: {api_key}, API Secret: {api_secret}")
```

---

## 🔒 Security Considerations

1. **API Authentication**: Uses Frappe's token-based authentication
2. **CSRF Protection**: Handled via Frappe's CSRF token system
3. **Role-Based Access**: Respects ERPNext user permissions
4. **Data Privacy**: Patient data stays within your infrastructure
5. **n8n Security**: Use HTTPS webhook URLs, consider IP whitelisting

---

## 📁 File Structure

```
medi-wise/
├── README.md                 # This file
├── ai-bot-interface.html     # Web UI (deploy to Frappe Web Page)
└── server_script.py          # API Server Script (deploy to Frappe)
```

---

## 🛠️ Customization

### Modifying the UI

Edit `ai-bot-interface.html`:
- CSS variables in `:root` for theming
- HTML structure for layout changes
- JavaScript functions for behavior

### Extending the API

Edit `server_script.py`:
- Add new `query_type` handlers
- Modify data fetching logic
- Customize AI prompts

### Enhancing AI Capabilities

Modify n8n workflow:
- Add knowledge bases for RAG
- Integrate medical databases
- Add specialized medical tools

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | Dec 2024 | RAG integration via n8n |
| 2.0.0 | Nov 2024 | Enhanced patient data display |
| 1.0.0 | Oct 2024 | Initial release |

---

## 📄 License

Proprietary - All rights reserved.

---

## 👥 Support

For support and questions, contact the MediWise Development Team.

