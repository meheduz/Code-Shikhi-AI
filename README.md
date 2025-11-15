# CodeShikhi AI - Programming Learning Assistant

[![Kaggle](https://img.shields.io/badge/Kaggle-Capstone-20BEFF?logo=kaggle)](https://www.kaggle.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://www.python.org)
[![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> An intelligent AI agent that helps you learn ANY programming language through conversational AI, powered by Google Gemini.

## 📸 Demo Screenshots

### Landing Page
![Landing Page](screenshots/Landing%20page.png)

### Programming Language Selection
![Language Selection](screenshots/Programming%20Language%20selection.png)

### AI Model Selection
![AI Model Selection](screenshots/Select%20ai%20Model.png)

### Conversation Interface
![Conversation Start](screenshots/Conversation%20start.png)

### AI Assistant in Action
![Conversation with Agent](screenshots/Conversation%20with%20agent.png)

### Chat History Feature
![Chat History](screenshots/Chat%20History.png)

---

## What is CodeShikhi AI?

CodeShikhi AI is an **agentic AI system** designed for programming education. It combines:
- **Multi-AI Backend**: Gemini, Groq, Cohere, DeepSeek
- **Intelligent Planning**: Context-aware responses
- **Tool Use**: Image analysis, code generation
- **Multi-turn Conversations**: Maintains learning context

---

## Features

### Core Capabilities
- **10+ Programming Languages**: Java, Python, JavaScript, C++, Go, Rust, PHP, Ruby, Swift, Kotlin
- **AI-Powered Explanations**: Clear, beginner-friendly teaching
- **Image Analysis**: Upload code screenshots for instant help
- **Chat History**: Never lose your learning progress
- **Fast Responses**: Optimized prompts with Gemini Flash
- **Modern UI**: Clean, responsive interface

### Agent Architecture
```
User Input → Flask API → MultiAIAssistant → Gemini API → Response
                              ↓
                        Fallback Models
                    (Groq/Cohere/DeepSeek)
```

---

## Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key (free tier available)

### Installation

```bash
# Clone repository
git clone https://github.com/meheduz/Code-Shikhi-AI.git
cd Code-Shikhi-AI

# Install dependencies
pip install -r requirements.txt

# Set up API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run application
python app.py
```

### Get Your Free Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy and paste into `.env` file

---

## Usage

### Web Interface
```bash
python app.py
# Open browser: http://localhost:8080
```

### Example Interactions

**Python Learning**:
```
You: explain list comprehension with examples
AI: List comprehension is a concise way to create lists...
    [code example with explanation]
```

**JavaScript Async**:
```
You: show me async/await example
AI: Here's a practical async/await example...
    [complete working code]
```

**Image Analysis**:
```
1. Upload code screenshot
2. AI analyzes and explains the code
3. Get suggestions for improvements
```

---

## Project Structure

```
Project-Alfa/
├── app.py                    # Flask web server
├── multi_ai_assistant.py     # Agent core logic
├── index.html                # Frontend UI
├── static/
│   ├── features.js           # JavaScript logic
│   └── improved-styles.css   # Styling
├── requirements.txt          # Python dependencies
├── .env                      # API keys (not in git)
├── README.md                 # This file
├── KAGGLE_SUBMISSION.md      # Capstone write-up
└── DEMO_CHECKLIST.md         # Submission guide
```

---

## Supported Languages

<div align="center">

![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![C](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![C#](https://img.shields.io/badge/C%23-239120?style=for-the-badge&logo=csharp&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white)
![Ruby](https://img.shields.io/badge/Ruby-CC342D?style=for-the-badge&logo=ruby&logoColor=white)
![Swift](https://img.shields.io/badge/Swift-FA7343?style=for-the-badge&logo=swift&logoColor=white)
![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=for-the-badge&logo=kotlin&logoColor=white)

</div>

---

## API Endpoints

### POST /chat
```json
{
  "message": "explain Python decorators",
  "language": "python",
  "ai_model": "auto",
  "image": "base64_encoded_image"
}
```

### GET /status
```json
{
  "status": "online",
  "assistant_type": "Gemini",
  "gemini_enabled": true
}
```

---

## Technical Details

### AI Models
- **Primary**: Google Gemini 1.5 Flash (fast, free)
- **Fallback**: Groq, Cohere, DeepSeek, OpenRouter
- **Vision**: Gemini Vision for image analysis

### Performance
- Response Time: < 2 seconds
- Image Processing: < 3 seconds
- Uptime: 99%+
- Cost: $0 (free tier)

---

## Use Cases

1. **Students**: Learn programming fundamentals
2. **Bootcamp Learners**: Get instant help with assignments
3. **Self-taught Developers**: Clarify complex concepts
4. **Career Switchers**: Explore new languages quickly
5. **Code Review**: Upload screenshots for feedback

---

## Future Enhancements

- [ ] Code execution sandbox
- [ ] Progress tracking dashboard
- [ ] AI-generated quizzes
- [ ] Voice input support
- [ ] Mobile app
- [ ] Cloud deployment (AWS/Vercel)

---

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Acknowledgments

- Google Gemini API for free AI access
- Kaggle for the Capstone challenge
- Open source community

---

## Contact

- **GitHub**: [@meheduz](https://github.com/meheduz)
- **Kaggle**: [@mdmeheduzzaman](https://www.kaggle.com/mdmeheduzzaman)
- **Project**: [Code-Shikhi-AI](https://github.com/meheduz/Code-Shikhi-AI)

---

## Star This Project

If CodeShikhi AI helped you learn programming, please star this repository!

---

**Built for Kaggle Capstone Project**