from flask import Blueprint, request, jsonify
from .checker import evaluate_password
from .utils import generate_strong_password

api = Blueprint('api', __name__)

@api.route('/api/evaluate', methods=['POST'])
def api_evaluate():
    data = request.get_json()
    password = data.get('password', '')
    result = evaluate_password(password)
    return jsonify(result)

@api.route('/api/suggest', methods=['GET'])
def api_suggest():
    suggestion = generate_strong_password()
    return jsonify({'suggestion': suggestion})
