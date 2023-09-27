import secrets
from datetime import date
from flask import session, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import likes

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
        if user.displayname:
            session['displayname'] = user.displayname
            return True
        return 'new'

    return False

def create_user(username, password1, password2):
    if password1 != password2:
        return 'pass_missmatch'
    password_hash = generate_password_hash(password1)
    sql = text('INSERT INTO users (username, password, visible) \
                VALUES (:username, :password, True)')

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
    try:
        del session['displayname']
    except:
        pass

def update_info(new_info):
    updated_info, date_error, missing_info = compile_info(new_info)
    failed = False
    sql = text('UPDATE users SET displayname=:displayname, gender=:gender, \
        f_interest=:f_interest,' 'm_interest=:m_interest, \
        o_interest=:o_interest, dob = :dob WHERE id=:id')
    db.session.execute(sql, {'displayname':updated_info[0], 'gender':updated_info[1],
        'f_interest':updated_info[2], 'm_interest':updated_info[3],
        'o_interest':updated_info[4], 'dob':updated_info[5], 'id':session['user_id']})
    db.session.commit()

    if not missing_info:
        session['displayname'] = updated_info[0]
    return (date_error, missing_info, failed)

def compile_info(new_info):
    old_info = get_info()
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

    for i , old_item in enumerate(old_info):
        if new_info[i] is None or new_info[i] == '':
            updated_info.append(old_item)
        else:
            updated_info.append(new_info[i])
    for value in updated_info:
        if value is None:
            missing_info = True

    return updated_info, date_error, missing_info

def convert_date(old_date, is_dob=False):
    try:
        date_temp = (list(map(int, old_date.split('.'))))
    except:
        return False
    date_final = date(date_temp[2], date_temp[1], date_temp[0])
    if is_dob:
        age = calculate_age(date_final)
        if age < 18 or age > 120:
            return False

    return date_final

def calculate_age(dob):
    today = date.today()
    age = today.year - dob.year - ((dob.month, dob.day) > (today.month, today.day))
    return age

def check_csrf():
    if session['csrf_token'] != request.form['csrf_token']:
        abort(403)

def get_info(uid = -1):
    if uid == -1:
        uid = session['user_id']
    sql = text('SELECT displayname, gender, f_interest, m_interest, \
                o_interest, dob FROM users WHERE id=:uid')
    result = db.session.execute(sql, {'uid':uid})
    return result.fetchone()

def translate_gender(character):
    if character == 'f':
        return 'Nainen'
    if character == 'm':
        return 'Mies'
    if character == 'o':
        return 'Muu'

def get_likes(uid=-1):
    return likes.get_likes(uid)

def update_like(item, like):
    return likes.update_like(item, like)

def block(uid):
    sql = text('INSERT INTO blocks (blocker_id, blocked_id) VALUES (:blocker, :blocked)')
    db.session.execute(sql, {'blocker':session['user_id'], 'blocked':uid})
    db.session.commit()
