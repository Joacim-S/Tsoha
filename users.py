import secrets
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from flask import session

def login(username, password):
    sql = text('SELECT id, password FROM users WHERE username=:username')
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if not user:
        return False

    password_hash = user.password
    if check_password_hash(password_hash, password):
        session['user_id'] = user[0]
        session['username'] = username
        session['csrf_token'] = secrets.token_hex(16)
        return True
    
    return False
    
def create_user(username, displayname, password1, password2):
    """ Returns an error or False. False means success"""
    if password1 != password2:
        return 'pass_missmatch'
    password_hash = generate_password_hash(password1)
    sql = text('INSERT INTO users (username, displayname, password) VALUES (:username, :displayname, :password)')

    try:
        db.session.execute(sql, {'username':username, 'displayname': displayname, 'password':password_hash})
        db.session.commit()
    except IntegrityError:
        return 'user_exists'

    login(username, password1)

    return False

def logout():
    del session['username']
    del session['user_id']
    del session['csrf_token']