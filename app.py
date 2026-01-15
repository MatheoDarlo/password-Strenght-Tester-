import random
import re
import sys
import os

# Add the project root to the path so we can import backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS

# Create Flask application
app = Flask(__name__)
CORS(app)

# Import the backend routes
try:
    from backend.routes import api
    app.register_blueprint(api)
except ImportError as e:
    print(f"Warning: Could not import backend routes: {e}")
    
    # Fallback implementation if backend is not available
    from backend.checker import evaluate_password
    
    @app.route('/api/evaluate', methods=['POST'])
    def api_evaluate():
        # Get JSON data and evaluate password
        data = request.get_json()
        password = data.get('password', '')
        result = evaluate_password(password)
        return jsonify(result)
    
    @app.route('/api/suggest', methods=['GET'])
    def api_suggest():
        from backend.utils import generate_strong_password
        suggestion = generate_strong_password()
        return jsonify({'suggestion': suggestion})

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# Main application entry point
if __name__ == '__main__':
    print("Starting Password Strength Tester...")
    print("Flask app running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
