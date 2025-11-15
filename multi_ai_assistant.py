import os
import base64
import io
import requests

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from PIL import Image
except ImportError:
    Image = None

class MultiAIAssistant:
    """Multi-AI Assistant with intelligent fallback system.
    
    Supports 6 AI providers: Gemini, Groq, Cohere, OpenRouter, DeepSeek, HuggingFace.
    Automatically selects best available model and falls back on failures.
    """
    
    def __init__(self):
        self.gemini_key = os.environ.get('GEMINI_API_KEY')
        self.groq_key = os.environ.get('GROQ_API_KEY')
        self.cohere_key = os.environ.get('COHERE_API_KEY')
        self.hf_key = os.environ.get('HUGGINGFACE_API_KEY')
        self.deepseek_key = os.environ.get('DEEPSEEK_API_KEY')
        self.openrouter_key = os.environ.get('OPENROUTER_API_KEY')
        
        self.active_ai = None
        self.model = None
        self._initialize_ai()
    
    def _initialize_ai(self):
        # Try Gemini first
        if self.gemini_key and genai:
            try:
                genai.configure(api_key=self.gemini_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.active_ai = 'gemini'
                print("✅ Gemini AI ready")
                return
            except Exception as e:
                print(f"⚠️ Gemini failed: {e}")
        
        # Try Groq (Free, very fast)
        if self.groq_key:
            try:
                response = requests.post(
                    'https://api.groq.com/openai/v1/chat/completions',
                    headers={'Authorization': f'Bearer {self.groq_key}'},
                    json={'model': 'llama-3.3-70b-versatile', 'messages': [{'role': 'user', 'content': 'Hi'}], 'max_tokens': 10}
                )
                if response.status_code == 200:
                    self.active_ai = 'groq'
                    print("✅ Groq AI ready")
                    return
            except Exception as e:
                print(f"⚠️ Groq failed: {e}")
        
        # Try Cohere (Free tier)
        if self.cohere_key:
            try:
                response = requests.post(
                    'https://api.cohere.ai/v1/generate',
                    headers={'Authorization': f'Bearer {self.cohere_key}'},
                    json={'model': 'command', 'prompt': 'Hi', 'max_tokens': 10}
                )
                if response.status_code == 200:
                    self.active_ai = 'cohere'
                    print("✅ Cohere AI ready")
                    return
            except Exception as e:
                print(f"⚠️ Cohere failed: {e}")
        
        # Try OpenRouter (Free, multiple models)
        if self.openrouter_key:
            try:
                response = requests.post(
                    'https://openrouter.ai/api/v1/chat/completions',
                    headers={
                        'Authorization': f'Bearer {self.openrouter_key}',
                        'HTTP-Referer': 'https://codeshikhi.ai',
                        'X-Title': 'CodeShikhi AI'
                    },
                    json={'model': 'meta-llama/llama-3.3-70b-instruct:free', 'messages': [{'role': 'user', 'content': 'Hi'}], 'max_tokens': 10}
                )
                if response.status_code == 200:
                    self.active_ai = 'openrouter'
                    print("✅ OpenRouter AI ready")
                    return
            except Exception as e:
                print(f"⚠️ OpenRouter failed: {e}")
        
        # Try DeepSeek (Free, powerful)
        if self.deepseek_key:
            try:
                response = requests.post(
                    'https://api.deepseek.com/v1/chat/completions',
                    headers={'Authorization': f'Bearer {self.deepseek_key}'},
                    json={'model': 'deepseek-chat', 'messages': [{'role': 'user', 'content': 'Hi'}], 'max_tokens': 10}
                )
                if response.status_code == 200:
                    self.active_ai = 'deepseek'
                    print("✅ DeepSeek AI ready")
                    return
            except Exception as e:
                print(f"⚠️ DeepSeek failed: {e}")
        
        # Try HuggingFace (Free)
        if self.hf_key:
            self.active_ai = 'huggingface'
            print("✅ HuggingFace AI ready")
            return
        
        print("❌ No AI available")

    def chat(self, user_input, image_data=None, language="any", ai_model="auto"):
        if not user_input and not image_data:
            return "Please provide a question or upload an image."
        
        # Image analysis only works with Gemini
        if image_data:
            if not self.gemini_key or not genai:
                return "❌ Image analysis requires Gemini API and google-generativeai library. Please install dependencies and add GEMINI_API_KEY."
            if not Image:
                return "❌ Image processing requires Pillow library. Please install: pip install Pillow"
            return self._chat_gemini(user_input, image_data, language)
        
        # If specific model selected, try that first
        if ai_model != "auto":
            try:
                if ai_model == 'gemini' and self.gemini_key:
                    return self._chat_gemini(user_input, image_data, language)
                elif ai_model == 'groq' and self.groq_key:
                    return self._chat_groq(user_input, language)
                elif ai_model == 'cohere' and self.cohere_key:
                    return self._chat_cohere(user_input, language)
                elif ai_model == 'openrouter' and self.openrouter_key:
                    return self._chat_openrouter(user_input, language)
                elif ai_model == 'deepseek' and self.deepseek_key:
                    return self._chat_deepseek(user_input, language)
                elif ai_model == 'huggingface' and self.hf_key:
                    return self._chat_huggingface(user_input, language)
                else:
                    return f"❌ {ai_model.title()} not available. Please check API key."
            except Exception as e:
                return f"❌ {ai_model.title()} error: {str(e)}"
        
        # Auto mode - try best available
        if not self.active_ai:
            return "❌ No AI service available. Please add API keys."
        
        try:
            if self.active_ai == 'gemini':
                return self._chat_gemini(user_input, image_data, language)
            elif self.active_ai == 'groq':
                return self._chat_groq(user_input, language)
            elif self.active_ai == 'cohere':
                return self._chat_cohere(user_input, language)
            elif self.active_ai == 'openrouter':
                return self._chat_openrouter(user_input, language)
            elif self.active_ai == 'deepseek':
                return self._chat_deepseek(user_input, language)
            elif self.active_ai == 'huggingface':
                return self._chat_huggingface(user_input, language)
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _chat_gemini(self, user_input, image_data, language):
        """Generate response using Gemini API with context-aware prompts."""
        if not self.model:
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Map language codes to full names
        lang_map = {
            'cpp': 'C++',
            'csharp': 'C#',
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'python': 'Python',
            'java': 'Java',
            'go': 'Go',
            'rust': 'Rust',
            'php': 'PHP',
            'ruby': 'Ruby',
            'swift': 'Swift',
            'kotlin': 'Kotlin',
            'c': 'C'
        }
        
        lang_name = lang_map.get(language.lower(), language)
        
        system_prompt = f"You are an expert programming assistant. Provide clear, well-structured responses with proper markdown formatting. Always use code blocks with language tags (```{language.lower() if language != 'any' else 'language'}). Be concise but thorough."
        
        if language != "any":
            system_prompt += f" Focus on {lang_name} programming."
        
        try:
            if image_data and Image:
                # Validate and process image
                if not image_data.startswith('data:image/'):
                    return "❌ Invalid image format. Please upload a valid image file."
                
                try:
                    image_bytes = base64.b64decode(image_data.split(',')[1])
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    # Compress large images
                    if image.size[0] > 1024 or image.size[1] > 1024:
                        image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                    
                    prompt = f"{system_prompt}\n\n{user_input or 'Analyze this code image and explain what it does'}"
                    response = self.model.generate_content([prompt, image])
                except Exception as img_error:
                    return f"❌ Image processing error: {str(img_error)}"
            else:
                prompt = f"{system_prompt}\n\n{user_input}"
                response = self.model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            return f"❌ Gemini API error: {str(e)}"
    
    def _chat_groq(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript'}
        lang_name = lang_map.get(language.lower(), language)
        
        system_msg = "You are an expert programming assistant. Provide clear, well-structured responses with proper markdown formatting. Use code blocks with language tags."
        if language != "any":
            system_msg += f" Focus on {lang_name} programming."
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': f'Bearer {self.groq_key}'},
            json={
                'model': 'llama-3.3-70b-versatile',
                'messages': [
                    {'role': 'system', 'content': system_msg},
                    {'role': 'user', 'content': user_input}
                ],
                'max_tokens': 2048,
                'temperature': 0.7
            }
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ Groq error: {response.status_code}"
    
    def _chat_cohere(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript'}
        lang_name = lang_map.get(language.lower(), language)
        
        if language != "any":
            lang_context = f"You MUST write code in {lang_name} programming language ONLY."
        else:
            lang_context = "programming"
        
        prompt = f"You are a {lang_context} assistant. Answer: {user_input}"
        
        response = requests.post(
            'https://api.cohere.ai/v1/generate',
            headers={'Authorization': f'Bearer {self.cohere_key}'},
            json={
                'model': 'command',
                'prompt': prompt,
                'max_tokens': 2048,
                'temperature': 0.7
            }
        )
        
        if response.status_code == 200:
            return response.json()['generations'][0]['text']
        else:
            return f"❌ Cohere error: {response.status_code}"
    
    def _chat_huggingface(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript'}
        lang_name = lang_map.get(language.lower(), language)
        
        if language != "any":
            lang_context = f"You MUST write code in {lang_name} programming language ONLY."
        else:
            lang_context = "programming"
        
        prompt = f"Answer this {lang_context} question: {user_input}"
        
        response = requests.post(
            'https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1',
            headers={'Authorization': f'Bearer {self.hf_key}'},
            json={'inputs': prompt, 'parameters': {'max_new_tokens': 2048}}
        )
        
        if response.status_code == 200:
            return response.json()[0]['generated_text'].replace(prompt, '').strip()
        else:
            return f"❌ HuggingFace error: {response.status_code}"
    
    def _chat_openrouter(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript'}
        lang_name = lang_map.get(language.lower(), language)
        
        system_msg = "You are an expert programming assistant. Provide clear, well-structured responses with proper markdown formatting. Use code blocks with language tags."
        if language != "any":
            system_msg += f" Focus on {lang_name} programming."
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {self.openrouter_key}',
                'HTTP-Referer': 'https://codeshikhi.ai',
                'X-Title': 'CodeShikhi AI'
            },
            json={
                'model': 'meta-llama/llama-3.3-70b-instruct:free',
                'messages': [
                    {'role': 'system', 'content': system_msg},
                    {'role': 'user', 'content': user_input}
                ],
                'max_tokens': 2048,
                'temperature': 0.7
            }
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ OpenRouter error: {response.status_code}"
    
    def _chat_deepseek(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript'}
        lang_name = lang_map.get(language.lower(), language)
        
        system_msg = "You are an expert programming assistant. Provide clear, well-structured responses with proper markdown formatting. Use code blocks with language tags."
        if language != "any":
            system_msg += f" Focus on {lang_name} programming."
        
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {self.deepseek_key}'},
            json={
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': system_msg},
                    {'role': 'user', 'content': user_input}
                ],
                'max_tokens': 2048,
                'temperature': 0.7
            }
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ DeepSeek error: {response.status_code}"
    
    def get_status(self):
        if self.active_ai == 'gemini':
            return "Gemini AI"
        elif self.active_ai == 'groq':
            return "Groq AI"
        elif self.active_ai == 'cohere':
            return "Cohere AI"
        elif self.active_ai == 'openrouter':
            return "OpenRouter AI"
        elif self.active_ai == 'deepseek':
            return "DeepSeek AI"
        elif self.active_ai == 'huggingface':
            return "HuggingFace AI"
        else:
            return "Offline"
    
    @property
    def use_gemini(self):
        return self.active_ai is not None
