from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet
from datetime import datetime

app = Flask(__name__)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

messages = []  # Store messages in memory - Replace with a database for production
users = {}  # Store user info

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    user_id = request.form['user_id']
    name = users.get(user_id, 'Anonymous')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    encrypted_message = cipher_suite.encrypt(f"{name} ({timestamp}): {message}".encode())
    messages.append(encrypted_message)
    return jsonify({'status': 'Message sent successfully'})

@app.route('/get_messages')
def get_messages():
    decrypted_messages = [cipher_suite.decrypt(msg).decode() for msg in messages]
    return jsonify({'messages': decrypted_messages})

@app.route('/change_name', methods=['POST'])
def change_name():
    user_id = request.form['user_id']
    new_name = request.form['new_name']
    users[user_id] = new_name
    return jsonify({'status': 'Name updated successfully'})

@app.route('/get_users')
def get_users():
    return jsonify({'users': users})

if __name__ == '__main__':
    app.run(debug=True)
