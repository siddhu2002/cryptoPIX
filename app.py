from flask import Flask, request, render_template, jsonify, session, redirect, url_for, flash
from utils.encrypt import encrypt_text

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/text/encrypt', methods=['POST'])
def api_encrypt():
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({'success': False, 'error': 'All fields (username, email, password) are required'}), 400

    result = encrypt_text(username, password)

    if result['success']:
        session['latest_result'] = {'metadata': 'Encryption successful'} 
        return result, 200
    else:
        return jsonify(result), 400

