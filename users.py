import secrets
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from flask import session, request
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
        if user.displayname:
            session['displayname'] = user.displayname
            return True
        return 'new'
    
    return False
    
def create_user(username, password1, password2):
    if password1 != password2:
        return 'pass_missmatch'
    password_hash = generate_password_hash(password1)
    sql = text('INSERT INTO users (username, password, visible) VALUES (:username, :password, True)')

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
    sql = text('UPDATE users SET displayname=:displayname, gender=:gender, f_interest=:f_interest,' \
    'm_interest=:m_interest, o_interest=:o_interest, dob = :dob WHERE id=:id')
    db.session.execute(sql, {'displayname':updated_info[0], 'gender':updated_info[1], 'f_interest':updated_info[2], \
    'm_interest':updated_info[3], 'o_interest':updated_info[4], 'dob':updated_info[5], 'id':session['user_id']})
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
    age = today.year - dob.year - ((dob.month, dob.day) < (today.month, today.day))
    return age

def check_csrf():
    if session['csrf_token'] != request.form['csrf_token']:
        abort(403)

def get_info(id = -1):
    if id == -1:
        id = session['user_id']
    sql = text('SELECT displayname, gender, f_interest, m_interest, o_interest, dob FROM users WHERE id=:id')
    result = db.session.execute(sql, {'id':id})
    return result.fetchone()

def get_likes(id = -1):
    if id == -1:
        id = session['user_id']
    sql = text('SELECT item FROM things, likes WHERE things.id=likes.item_id AND likes.user_id=:id AND likes.likes=:like')
    result = db.session.execute(sql, {'id':id, 'like':True})
    likes = result.fetchall()
    result = db.session.execute(sql, {'id':id, 'like':False})
    dislikes = result.fetchall()
    return likes, dislikes

def translate_gender(character):
    if character == 'f':
        return 'Nainen'
    if character == 'm':
        return 'Mies'
    if character == 'o':
        return 'Muu'

def get_item_id(item):
    item = item.lower()
    sql = text('SELECT id FROM things WHERE things.item=:item')
    result = db.session.execute(sql, {'item':item})
    return result.fetchone()

def add_thing(item):
    item = item.lower()
    item_id = get_item_id(item)

    if item_id:
        return item_id

    sql = text('INSERT INTO things (item) VALUES (:item)')
    db.session.execute(sql, {'item':item})
    db.session.commit()
    return get_item_id(item)

def update_like(item, like):
    item_id = add_thing(item)
    sql = text('SELECT id FROM likes WHERE item_id=:item_id AND user_id=:user_id')
    result = db.session.execute(sql, {'item_id':item_id.id, 'user_id':session['user_id']})
    like_id = result.fetchone()

    if like_id:
        sql = text('UPDATE likes SET likes=:like WHERE id=:like_id')
        db.session.execute(sql, {'like_id':like_id.id, 'like':like})
        db.session.commit()
        return
    
    sql = text('INSERT INTO likes (user_id, item_id, likes) VALUES (:user_id, :item_id, :likes)')
    db.session.execute(sql, {'user_id':session['user_id'], 'item_id':item_id.id, 'likes':like})
    db.session.commit()