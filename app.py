import requests
from scapy.all import sniff
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_login import current_user
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
    return render_template('login.html')



# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         name = request.form['name']

#         # check if username exists in MongoDB
#         user = collection.find_one({'_id': username})
#         if user:
#             message = '*****Username already exists. Try a New One*****'
#             return render_template('register.html', message=message)

#         # if new user, store information in MongoDB
#         collection.insert_one(
#             {'_id': username, 'password': password, 'email': email, 'name': name})
#         message = 'Registration successful'
#         return render_template('login.html', message=message)
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         if username == 'admin' and password == 'password':
#             user = User(username)
#             login_user(user)
#             return redirect(url_for('index'))
#         else:
#             return render_template('login.html', error='Invalid username or password')

#     return render_template('login.html')

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
                user = User(username)
                login_user(user)
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
        user = collection.find_one({'_id': username})
        if user:
            message = '*****Username already exists. Try a New One*****'
            return render_template('registration.html', message=message)

        # if new user, store information in MongoDB
        collection.insert_one(
            {'_id': username, 'password': password, 'email': email, 'name': name})
        message = 'Registration successful'
        return render_template('login.html', message=message)
    return render_template('registration.html')


@app.route('/test')
@login_required
def test():
    return render_template('test.html')


API_KEY = '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'
# API_KEY = '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'
API_URL = 'https://api.openai.com/v1/engines/text-davinci-002/completions'


@app.route('/ask', methods=['POST'])
@login_required
def ask_chatgpt():
    testCode = request.form['packet_summary']
    openai.api_key = API_KEY
    model_engine = "text-davinci-002"
    prompt = (f"Role=system\n"
              f"Content=you are a cyber security expert. List out these parameter for given code: 1. security threat count, 2. threat names 3. Threat level next line \n"
              f"Role=user\n"
              f"Content={testCode}")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }

    data = {
        'prompt': prompt,
        'max_tokens': 500,
        'n': 1,
        'stop': None,
        'temperature': 0,
    }

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    print(session['username'])
    print(response.choices[0].text.strip())
    cluster = MongoClient(
        "mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["securifyGPT"]
    collection = db["history"]
    collection.insert_one({'username': session['username'], 'code': testCode,
                          'result': response.choices[0].text.strip(), 'date': datetime.now()})
    result = response.choices[0].text.strip()
    return jsonify({'response': result})
    # if response.status_code == 200:
    # result = response.json()['choices'][0]['text'].strip()
    # else:
    # result = f"Error: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True)
