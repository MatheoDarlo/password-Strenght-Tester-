import random
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

try:
    from backend.routes import api
    app.register_blueprint(api)
except ImportError as e:
    print(f"Warning: Could not import backend routes: {e}")
    
    from backend.checker import evaluate_password
    
    @app.route('/api/evaluate', methods=['POST'])
    def api_evaluate():
        data = request.get_json()
        password = data.get('password', '')
        result = evaluate_password(password)
        return jsonify(result)
    
    @app.route('/api/suggest', methods=['GET'])
    def api_suggest():
        from backend.utils import generate_strong_password
        suggestion = generate_strong_password()
        return jsonify({'suggestion': suggestion})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Main application entry point
if __name__ == '__main__':
    print("Starting Password Strength Tester...")
    print("Flask app running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
