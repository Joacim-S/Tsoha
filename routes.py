from app import app
from flask import redirect, render_template, request
import users

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if users.login(username, password):
        return redirect('/')
    else:
        return render_template('index.html', credential_error=True)

@app.route('/create', methods=['POST'])
def create():
    username = request.form['username']
    displayname = request.form['displayname']
    password1 = request.form['password1']
    password2 = request.form['password2']
    create_result = users.create_user(username, displayname, password1, password2)
    if create_result:
        return render_template('register.html', error=create_result)
    return render_template('/my_profile.html', first_login = True)

@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')