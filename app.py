from flask import Flask
from sqlalchemy.exc import IntegrityError
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.secret_key = getenv('SECRET_KEY')
db = SQLAlchemy(app)

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
    sql = text('SELECT id, password FROM users WHERE username=:username')
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if not user:
        return render_template('index.html', no_user=True)
    else:
        password_hash = user.password
        if check_password_hash(password_hash, password):
            session['username'] = username
            return redirect('/')
        else:
            return render_template('index.html', wrong_password=True)

@app.route('/create', methods=['POST'])
def create():
    username = request.form['username']
    displayname = request.form['displayname']
    password = request.form['password']
    password_hash = generate_password_hash(password)
    sql = text('INSERT INTO users (username, displayname, password) VALUES (:username, :displayname, :password)')
    try:
        db.session.execute(sql, {'username':username, 'displayname': displayname, 'password':password_hash})
        db.session.commit()
    except IntegrityError:
        return render_template('register.html', error=True)

    return redirect('/')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')