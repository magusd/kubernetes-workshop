from flask import Flask, request, make_response, redirect, url_for
from functools import wraps
app = Flask(__name__)
app.secret_key = 'grapes'

user_db = {
        'whale':{
            'home': '/ocean',
            'password': 'flipers',
            'cursewords': True
        },
        'tiger':{
            'home': '/ocean',
            'password': 'cat',
            'cursewords': True
        },
        'rabbit':{
            'home': '/safeplace',
            'password': 'bitch',
            'cursewords': False
        },
    }

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username in user_db and auth.password == user_db[auth.username]['password']:
            return f(*args, **kwargs)
        return make_response('Could not verify your response.', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})
    return decorated
def logout():
    return make_response('Hello, are you a sea creature? Then <a href="/login">login</a> here!', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})

@app.route('/')
def home():
    return 'Hello, are you a sea creature? Then <a href="/login">login</a> here!'

@app.route('/login')
@auth_required
def login():
    user = request.authorization.username
    if user in user_db:
        return redirect(user_db[user]['home'])
    return 'Yay, you are logged in!'


@app.route('/ocean')
@auth_required
def ocean():
    user = request.authorization.username
    if user_db[user]['home'] != '/ocean':
        return logout()
    img = url_for('static', filename='whale.png')
    return f'<img src="{img}">'

@app.route('/safeplace')
@auth_required
def hole():
    user = request.authorization.username
    if user_db[user]['home'] != '/safeplace':
        return logout()
    img = url_for('static', filename='rabbit.png')
    return f'<img src="{img}">'


    
    


if __name__ == '__main__':
    app.run(debug=True, port=5000)