import requests
from scapy.all import sniff
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import pymongo
from pymongo import MongoClient
import openai
from flask import Flask, request, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'
username = None
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
@login_required
def index():
    username = session['username']
    return render_template('homePage.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cluster = MongoClient(
            "mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
        db = cluster["securifyGPT"]
        collection = db["userinfo"]
        results = collection.find({"_id": username})
        for result in results:
            if result["password"] == password:
                user = User(1)
                login_user(user)
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Invalid username or password. Try Again.')
    return render_template('login.html')


@app.route('/testCode', methods=['POST'])
@login_required
def test_your_code():
    return redirect(url_for('test'))


@app.route('/history', methods=['POST'])
@login_required
def access_history():
    # connect to MongoDB and retrieve search history for the current user
    client = MongoClient(
        "mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
    db = client["securifyGPT"]
    collection = db["history"]
    history = collection.find({'username': session['username']})

    print(history)

    return render_template('historyPage.html', results=history)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cluster = MongoClient(
            "mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
        db = cluster["securifyGPT"]
        collection = db["userinfo"]
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']

        # check if username exists in MongoDB
        user = collection.find


API_KEY = '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'
API_URL = 'https://api.openai.com/v1/engines/text-davinci-002/completions'


@app.route('/ask', methods=['POST'])
@login_required
def ask_chatgpt():
    packet_summary = request.form['packet_summary']
    prompt = f"Analyze the following network packet information for potential threats:\n{packet_summary}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }

    data = {
        'prompt': prompt,
        'max_tokens': 100,
        'n': 1,
        'stop': None,
        'temperature': 0,
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()['choices'][0]['text'].strip()
    else:
        result = f"Error: {response.status_code}"

    return jsonify({'response': result})


if __name__ == '__main__':
    app.run(debug=True)