import requests

from scapy.all import sniff
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_login import current_user

import pymongo

from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your-secret-key'

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
    username = current_user.id  # get the current user's ID
    # pass the username to the template
    return render_template('homePage.html', username=username)



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
    db = client['securifyGPT']
    history = db.search_history.find({'user_id': current_user.id})

    # pass the search history to the template
    return render_template('historyPage.html', history=history)



@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/test')
@login_required
def test():
    return render_template('test.html')


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
