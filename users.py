import secrets
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from flask import session
from datetime import datetime, timedelta, date

def login(username, password):
    sql = text('SELECT * FROM users WHERE username=:username')
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if not user:
        return False

    password_hash = user.password
    if check_password_hash(password_hash, password):
        session['user_id'] = user[0]
        session['username'] = username
        session['csrf_token'] = secrets.token_hex(16)
        if user.displayname == None:
            return 'new'

        return True
    
    return False
    
def create_user(username, password1, password2):
    if password1 != password2:
        return 'pass_missmatch'
    password_hash = generate_password_hash(password1)
    sql = text('INSERT INTO users (username, password) VALUES (:username, :password)')

    try:
        db.session.execute(sql, {'username':username, 'password':password_hash})
        db.session.commit()
    except IntegrityError:
        return 'user_exists'

    return login(username, password1)

def logout():
    del session['username']
    del session['user_id']
    del session['csrf_token']

def update_info(new_info):
    updated_info, date_error, missing_info = compile_info(new_info)
    failed = False
    sql = text('UPDATE users SET displayname=:displayname, gender=:gender, f_interest=:f_interest,' \
    'm_interest=:m_interest, o_interest=:o_interest, dob = :dob WHERE id=:id')
    db.session.execute(sql, {'displayname':updated_info[0], 'gender':updated_info[1], 'f_interest':updated_info[2], \
    'm_interest':updated_info[3], 'o_interest':updated_info[4], 'dob':updated_info[5], 'id':session['user_id']})
    db.session.commit()
    return (date_error, missing_info, failed)

def compile_info(new_info):
    sql = text('SELECT displayname, gender, f_interest, m_interest, o_interest, dob FROM users WHERE id=:id')
    result = db.session.execute(sql, {'id':session['user_id']})
    old_info = result.fetchone()
    updated_info = []
    missing_info = False
    date_error = False

    if new_info[5]:
        new_date = convert_date(new_info[5], True)
        if new_date:
            new_info[5] = new_date
        else:
            new_info[5] = None
            date_error = True
    
    for i in range(len(old_info)):
        if new_info[i] == None or new_info[i] == '':
            updated_info.append(old_info[i])
        else:
            updated_info.append(new_info[i])
    for value in updated_info:
        if value == None:
            missing_info = True
    
    return updated_info, date_error, missing_info

def convert_date(old_date, is_dob=False):
    try:
        date_temp = (list(map(int, old_date.split('.'))))
        date_final = date(date_temp[2], date_temp[1], date_temp[0])
        if is_dob and (date_final.year < 1900 or (date.today() - date_final).days < 18*365):
            return False
        else:
            return date_final
    except:
        return False
