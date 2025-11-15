import os
import base64
import io
import requests
import time

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
    
    Supports multiple AI providers with automatic fallback.
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
        self.last_request_time = {}
        self.min_request_interval = 1  # 1 second between requests
        self._initialize_ai()
    
    def _initialize_ai(self):

        if self.gemini_key and genai:
            try:
                genai.configure(api_key=self.gemini_key)
                # Try different Gemini models
                models_to_try = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-flash-latest']
                for model_name in models_to_try:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        break
                    except Exception:
                        continue
                else:
                    raise Exception("No Gemini model available")
                self.active_ai = 'gemini'
                return
            except Exception:
                pass
        

        if self.groq_key:
            try:
                response = requests.post(
                    'https://api.groq.com/openai/v1/chat/completions',
                    headers={'Authorization': f'Bearer {self.groq_key}'},
                    json={'model': 'llama-3.3-70b-versatile', 'messages': [{'role': 'user', 'content': 'Hi'}], 'max_tokens': 10},
                    timeout=5
                )
                if response.status_code == 200:
                    self.active_ai = 'groq'
                    return
            except Exception:
                pass
        

        if self.cohere_key:
            try:
                response = requests.post(
                    'https://api.cohere.ai/v1/chat',
                    headers={'Authorization': f'Bearer {self.cohere_key}'},
                    json={'model': 'command-r-08-2024', 'message': 'Hi', 'max_tokens': 10},
                    timeout=5
                )
                if response.status_code == 200:
                    self.active_ai = 'cohere'
                    return
            except Exception:
                pass
        

        if self.openrouter_key:
            try:
                response = requests.post(
                    'https://openrouter.ai/api/v1/chat/completions',
                    headers={
                        'Authorization': f'Bearer {self.openrouter_key}',
                        'HTTP-Referer': 'https://codeshikhi.ai',
                        'X-Title': 'CodeShikhi AI'
                    },
                    json={'model': 'meta-llama/llama-3.3-70b-instruct:free', 'messages': [{'role': 'user', 'content': 'Hi'}], 'max_tokens': 10},
                    timeout=5
                )
                if response.status_code == 200:
                    self.active_ai = 'openrouter'
                    return
            except Exception:
                pass
        

        if self.deepseek_key and len(self.deepseek_key) > 10:
            try:
                response = requests.post(
                    'https://api.deepseek.com/v1/chat/completions',
                    headers={'Authorization': f'Bearer {self.deepseek_key}'},
                    json={'model': 'deepseek-chat', 'messages': [{'role': 'user', 'content': 'Hi'}], 'max_tokens': 10},
                    timeout=10
                )
                if response.status_code == 200:
                    self.active_ai = 'deepseek'
                    return
            except Exception:
                pass
        

        if self.hf_key:
            self.active_ai = 'huggingface'
            return

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
        
        # Auto mode - try best available with fallback
        if not self.active_ai:
            return "❌ No AI service available. Please add API keys."
        
        # Try primary AI, fallback to others if it fails
        primary_result = None
        try:
            if self.active_ai == 'gemini':
                primary_result = self._chat_gemini(user_input, image_data, language)
            elif self.active_ai == 'groq':
                primary_result = self._chat_groq(user_input, language)
            elif self.active_ai == 'cohere':
                primary_result = self._chat_cohere(user_input, language)
            elif self.active_ai == 'openrouter':
                primary_result = self._chat_openrouter(user_input, language)
            elif self.active_ai == 'deepseek':
                primary_result = self._chat_deepseek(user_input, language)
            elif self.active_ai == 'huggingface':
                primary_result = self._chat_huggingface(user_input, language)
            
            # If primary AI failed, try fallback
            if primary_result and primary_result.startswith('❌'):
                return self._try_fallback(user_input, language, primary_result)
            
            return primary_result
        except Exception as e:
            return self._try_fallback(user_input, language, f"❌ Error: {str(e)}")
    
    def _chat_gemini(self, user_input, image_data, language):
        """Generate response using Gemini API with context-aware prompts."""
        if not self.model:
            genai.configure(api_key=self.gemini_key)
            # Try different Gemini models
            models_to_try = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-flash-latest']
            for model_name in models_to_try:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    break
                except Exception:
                    continue
            else:
                self.model = genai.GenerativeModel('gemini-2.5-flash')  # fallback
        
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
            },
            timeout=30
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
            'https://api.cohere.ai/v1/chat',
            headers={'Authorization': f'Bearer {self.cohere_key}'},
            json={
                'model': 'command-r-08-2024',
                'message': user_input,
                'max_tokens': 2048,
                'temperature': 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['text']
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
            'https://api-inference.huggingface.co/models/gpt2',
            headers={'Authorization': f'Bearer {self.hf_key}'},
            json={'inputs': prompt, 'parameters': {'max_new_tokens': 512}},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').replace(prompt, '').strip()
            return str(result)
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
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ OpenRouter error: {response.status_code}"
    
    def _rate_limit(self, ai_name):
        """Simple rate limiting"""
        current_time = time.time()
        if ai_name in self.last_request_time:
            time_diff = current_time - self.last_request_time[ai_name]
            if time_diff < self.min_request_interval:
                time.sleep(self.min_request_interval - time_diff)
        self.last_request_time[ai_name] = time.time()
    
    def _chat_deepseek(self, user_input, language):
        lang_map = {'cpp': 'C++', 'csharp': 'C#', 'javascript': 'JavaScript', 'typescript': 'TypeScript'}
        lang_name = lang_map.get(language.lower(), language)
        
        system_msg = "You are an expert programming assistant. Provide clear, well-structured responses with proper markdown formatting. Use code blocks with language tags."
        if language != "any":
            system_msg += f" Focus on {lang_name} programming."
        
        try:
            self._rate_limit('deepseek')
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
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 402:
                return "❌ DeepSeek quota exceeded. Try another AI model."
            elif response.status_code == 401:
                return "❌ DeepSeek API key invalid."
            elif response.status_code == 429:
                return "❌ DeepSeek rate limited. Try again later."
            else:
                return f"❌ DeepSeek error: {response.status_code}"
        except requests.exceptions.Timeout:
            return "❌ DeepSeek timeout. Try again."
        except Exception:
            return "❌ DeepSeek connection error."
    
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
    
    def _try_fallback(self, user_input, language, original_error):
        """Try fallback AI models when primary fails"""
        fallback_order = ['groq', 'openrouter', 'gemini', 'cohere', 'huggingface']
        
        for ai_name in fallback_order:
            if ai_name == self.active_ai:
                continue  # Skip the one that already failed
                
            try:
                if ai_name == 'groq' and self.groq_key:
                    result = self._chat_groq(user_input, language)
                    if not result.startswith('❌'):
                        return result
                elif ai_name == 'openrouter' and self.openrouter_key:
                    result = self._chat_openrouter(user_input, language)
                    if not result.startswith('❌'):
                        return result
                elif ai_name == 'gemini' and self.gemini_key:
                    result = self._chat_gemini(user_input, None, language)
                    if not result.startswith('❌'):
                        return result
                elif ai_name == 'cohere' and self.cohere_key:
                    result = self._chat_cohere(user_input, language)
                    if not result.startswith('❌'):
                        return result
            except:
                continue
        
        return original_error
    
    @property
    def use_gemini(self):
        return self.active_ai is not None
