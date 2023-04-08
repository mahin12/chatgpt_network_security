# import requests
# import json
# from scapy.all import sniff
# import tkinter as tk
# from tkinter import ttk
# from threading import Thread
# import json
# from scapy.all import sniff
# from flask import Flask, render_template, request, jsonify
# from flask import Flask, render_template, request, redirect, url_for

# app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('login.html')


# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     # Check if username and password are correct
#     if username == 'admin' and password == 'password':
#         return redirect(url_for('homePage'))
#     else:
#         return render_template('login.html', error='Invalid username or password')


# @app.route('/homePage')
# def homePage():
#     return render_template('homePage.html')


# if __name__ == '__main__':
#     app.run(debug=True)