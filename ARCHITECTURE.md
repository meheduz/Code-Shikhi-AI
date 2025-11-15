# CodeShikhi AI - System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Browser    │  │   Mobile     │  │   Desktop    │     │
│  │   (Chrome)   │  │   (Future)   │  │   (Future)   │     │
│  └──────┬───────┘  └──────────────┘  └──────────────┘     │
└─────────┼───────────────────────────────────────────────────┘
          │ HTTP/HTTPS
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Frontend (index.html)                   │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │  │
│  │  │ Language   │  │   Chat     │  │   Image    │    │  │
│  │  │ Selector   │  │ Interface  │  │  Upload    │    │  │
│  │  └────────────┘  └────────────┘  └────────────┘    │  │
│  │  ┌────────────────────────────────────────────┐    │  │
│  │  │      localStorage (Chat History)           │    │  │
│  │  └────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────┼───────────────────────────────────────────────────┘
          │ POST /chat, GET /status
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Flask Web Server (app.py)               │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │  │
│  │  │   Route    │  │   Route    │  │   Route    │    │  │
│  │  │    /       │  │   /chat    │  │  /status   │    │  │
│  │  └────────────┘  └────────────┘  └────────────┘    │  │
│  │  ┌────────────────────────────────────────────┐    │  │
│  │  │      Request Validation & Parsing          │    │  │
│  │  └────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────┼───────────────────────────────────────────────────┘
          │ Function Call
          ▼
┌─────────────────────────────────────────────────────────────┐
│                      AGENT LAYER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        MultiAIAssistant (Agent Core)                 │  │
│  │  ┌────────────────────────────────────────────┐     │  │
│  │  │         Planning & Reasoning               │     │  │
│  │  │  • Analyze user intent                     │     │  │
│  │  │  • Select appropriate AI model             │     │  │
│  │  │  • Generate context-aware prompts          │     │  │
│  │  └────────────────────────────────────────────┘     │  │
│  │  ┌────────────────────────────────────────────┐     │  │
│  │  │            Tool Selection                  │     │  │
│  │  │  • Text generation                         │     │  │
│  │  │  • Image analysis                          │     │  │
│  │  │  • Code generation                         │     │  │
│  │  └────────────────────────────────────────────┘     │  │
│  │  ┌────────────────────────────────────────────┐     │  │
│  │  │         Memory Management                  │     │  │
│  │  │  • Chat history tracking                   │     │  │
│  │  │  • Context window management               │     │  │
│  │  └────────────────────────────────────────────┘     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────┼───────────────────────────────────────────────────┘
          │ API Calls
          ▼
┌─────────────────────────────────────────────────────────────┐
│                      AI MODEL LAYER                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Primary: Google Gemini                  │  │
│  │  ┌────────────────────────────────────────────┐     │  │
│  │  │      gemini-1.5-flash (Text)               │     │  │
│  │  │      gemini-1.5-flash (Vision)             │     │  │
│  │  └────────────────────────────────────────────┘     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Fallback Models                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │  Groq    │  │ Cohere   │  │DeepSeek  │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow

### 1. User Interaction Flow
```
User Types Question
    ↓
Frontend Captures Input
    ↓
JavaScript Validates Input
    ↓
POST Request to /chat
    ↓
Flask Receives Request
    ↓
MultiAIAssistant Processes
    ↓
Gemini API Call
    ↓
Response Generated
    ↓
JSON Returned to Frontend
    ↓
UI Updates with Response
    ↓
localStorage Saves History
```

### 2. Image Analysis Flow
```
User Uploads Image
    ↓
Frontend Converts to Base64
    ↓
POST Request with Image Data
    ↓
Flask Validates Image
    ↓
MultiAIAssistant Processes
    ↓
Gemini Vision API Call
    ↓
Image Analysis Response
    ↓
JSON Returned to Frontend
    ↓
UI Displays Analysis
```

---

## 🧠 Agent Components

### 1. Planning Module
**Location**: `multi_ai_assistant.py`

**Responsibilities**:
- Analyze user intent
- Determine programming language context
- Select appropriate AI model
- Generate optimized prompts

**Example**:
```python
def chat(self, user_input, image_data, language, ai_model):
    # Planning phase
    if language != 'any':
        system_prompt = f"You are an expert {language} tutor..."
    
    # Reasoning phase
    if image_data:
        return self._analyze_image(image_data, user_input)
    
    # Execution phase
    return self._generate_response(user_input, system_prompt)
```

### 2. Tool Use Module
**Available Tools**:
- Text generation (Gemini API)
- Image analysis (Gemini Vision)
- Model fallback (Groq/Cohere)

### 3. Memory Module
**Storage**:
- Client-side: localStorage (chat history)
- Server-side: In-memory (session context)

---

## 🔐 Security Architecture

### API Key Management
```
.env file (not in git)
    ↓
python-dotenv loads
    ↓
Environment variables
    ↓
Used in API calls
```

### Input Validation
- Max content length: 16MB
- Image format validation
- XSS prevention in frontend

---

## 📊 Data Flow Diagram

```
┌─────────┐
│  User   │
└────┬────┘
     │ 1. Question
     ▼
┌─────────────┐
│  Frontend   │
└────┬────────┘
     │ 2. HTTP POST
     ▼
┌─────────────┐
│   Flask     │
└────┬────────┘
     │ 3. Function Call
     ▼
┌─────────────┐
│   Agent     │
└────┬────────┘
     │ 4. API Request
     ▼
┌─────────────┐
│   Gemini    │
└────┬────────┘
     │ 5. AI Response
     ▼
┌─────────────┐
│   Agent     │
└────┬────────┘
     │ 6. JSON Response
     ▼
┌─────────────┐
│   Flask     │
└────┬────────┘
     │ 7. HTTP Response
     ▼
┌─────────────┐
│  Frontend   │
└────┬────────┘
     │ 8. Display
     ▼
┌─────────┐
│  User   │
└─────────┘
```

---

## 🚀 Deployment Architecture

### Current: Localhost
```
┌──────────────────┐
│  Local Machine   │
│  ┌────────────┐  │
│  │   Flask    │  │
│  │ Port 8080  │  │
│  └────────────┘  │
└──────────────────┘
```

### Future: Cloud Deployment
```
┌─────────────────────────────────────┐
│           AWS/Vercel                │
│  ┌─────────────┐  ┌─────────────┐  │
│  │   Lambda    │  │     S3      │  │
│  │  (Backend)  │  │ (Frontend)  │  │
│  └─────────────┘  └─────────────┘  │
│  ┌─────────────┐                    │
│  │  API Gateway│                    │
│  └─────────────┘                    │
└─────────────────────────────────────┘
```

---

## 🔧 Technology Stack

### Backend
- **Framework**: Flask 3.0+
- **AI SDK**: google-generativeai
- **Image Processing**: Pillow
- **Environment**: python-dotenv

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling
- **JavaScript**: Vanilla JS (no frameworks)

### AI Models
- **Primary**: Gemini 1.5 Flash
- **Fallback**: Groq, Cohere, DeepSeek

---

## 📈 Scalability Considerations

### Current Limitations
- Single-threaded Flask server
- In-memory session storage
- No database persistence

### Future Improvements
- Gunicorn/uWSGI for production
- Redis for session management
- PostgreSQL for user data
- CDN for static assets
- Load balancer for high traffic

---

## 🧪 Testing Architecture

### Unit Tests (Future)
```python
def test_chat_endpoint():
    response = client.post('/chat', json={
        'message': 'test',
        'language': 'python'
    })
    assert response.status_code == 200
```

### Integration Tests (Future)
- API endpoint testing
- Gemini API mocking
- Frontend E2E tests

---

## 📝 Configuration Management

### Environment Variables
```bash
GEMINI_API_KEY=<key>
GROQ_API_KEY=<key>
COHERE_API_KEY=<key>
PORT=8080
```

### Application Config
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['DEBUG'] = True  # Development only
```

---

**This architecture supports the Kaggle Capstone requirement for agentic AI systems with planning, tool use, and multi-turn conversations.**
