import requests
import json
from scapy.all import sniff
from flask import Flask, render_template, request, jsonify

API_KEY = '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'
API_URL = 'https://api.openai.com/v1/engines/text-davinci-002/completions'

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
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
        'temperature': 1,
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()['choices'][0]['text'].strip()
    else:
        result = f"Error: {response.status_code}"

    return jsonify({'response': result})


if __name__ == '__main__':
    app.run()
