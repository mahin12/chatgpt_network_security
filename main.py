import requests
import json
from scapy.all import sniff
import tkinter as tk
from tkinter import ttk
from threading import Thread
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


def ask_chatgpt(prompt):
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
        return response.json()['choices'][0]['text'].strip()
    else:
        print(f"Error: {response.status_code}")
        return None


def process_packet(packet, output):
    packet_summary = f"Packet info: {packet.summary()}"

    prompt = f"Analyze the following network packet information for potential threats:\n{packet_summary}"
    chatgpt_response = ask_chatgpt(prompt)

    output.insert(tk.END, f"Packet: {packet_summary}\n")
    output.insert(tk.END, f"ChatGPT analysis: {chatgpt_response}\n\n")
    output.see(tk.END)  # Autoscroll to the bottom


def start_sniffing(output):
    sniff(filter="ip", iface="en0",
          prn=lambda packet: process_packet(packet, output), store=0)


def ask_question(question, output):
    chatgpt_response = ask_chatgpt(question)

    output.insert(tk.END, f"Question: {question}\n")
    output.insert(tk.END, f"ChatGPT response: {chatgpt_response}\n\n")
    output.see(tk.END)


def main():
    root = tk.Tk()
    root.title("Network Security Analysis")
    root.geometry("800x600")
    
    mainframe = ttk.Frame(root, padding="10 10 10 10")
    mainframe.pack(fill=tk.BOTH, expand=True)
    
    output_label = ttk.Label(mainframe, text="Output:", font=("Helvetica", 12))
    output_label.pack(pady=(0, 10))
    
    output = tk.Text(mainframe, wrap=tk.WORD, width=80, height=20)
    output.pack(fill=tk.BOTH, expand=True, padx=(0, 20))
    
    scrollbar = ttk.Scrollbar(mainframe, orient=tk.VERTICAL, command=output.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output["yscrollcommand"] = scrollbar.set
    
    question_label = ttk.Label(mainframe, text="Ask ChatGPT:", font=("Helvetica", 12))
    question_label.pack(pady=(20, 0))

    question_entry = ttk.Entry(mainframe, width=60)
    question_entry.pack(pady=(0, 10))
    
    button_frame = ttk.Frame(mainframe)
    button_frame.pack(pady=(0, 20))
    
    ask_button = ttk.Button(button_frame, text="Ask", command=lambda: ask_question(question_entry.get(), output))
    ask_button.grid(column=0, row=0, padx=(0, 20))
    
    start_button = ttk.Button(button_frame, text="Start Sniffing", command=lambda: Thread(target=start_sniffing, args=(output,)).start())
    start_button.grid(column=1, row=0, padx=(0, 20))
    
    quit_button = ttk.Button(button_frame, text="Quit", command=root.destroy)
    quit_button.grid(column=2, row=0)
    
    root.mainloop()


if __name__ == '__main__':
    app.run(debug=True)
