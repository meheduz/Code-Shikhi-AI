from flask import Flask, request, jsonify, send_from_directory
from multi_ai_assistant import MultiAIAssistant
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
assistant = MultiAIAssistant()

@app.route('/')
def landing():
    return send_from_directory('.', 'landing.html')

@app.route('/chat')
def chat_page():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('message', '')
        image_data = data.get('image', None)
        language = data.get('language', 'any')
        ai_model = data.get('ai_model', 'auto')
        
        response = assistant.chat(user_input, image_data, language, ai_model)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

@app.route('/status')
def status():
    try:
        return jsonify({
            'status': 'online',
            'assistant_type': assistant.get_status(),
            'gemini_enabled': assistant.use_gemini
        })
    except Exception:
        return jsonify({'status': 'error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)