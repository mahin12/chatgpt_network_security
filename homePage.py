# from flask import Flask, render_template, redirect, url_for

# app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('homepage.html')


# @app.route('/testCode', methods=['POST'])
# def test_your_code():
#     # Add your code to test here
#     return redirect(url_for('test'))


# @app.route('/history', methods=['POST'])
# def access_history():
#     # Add your code to access history here
#     return "Access history page"


# @app.route('/logout', methods=['POST'])
# def logout():
#     # Add your code to logout here
#     return redirect(url_for('login'))

# @app.route('/test')
# def test():
#     return render_template('index.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

# if __name__ == '__main__':
#     app.run(debug=True)
