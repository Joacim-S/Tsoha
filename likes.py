from db import db
from flask import session
from sqlalchemy.sql import text

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

def get_likes(id=-1):
    if id == -1:
        id = session['user_id']
    sql = text('SELECT item FROM things, likes WHERE things.id=likes.item_id AND likes.user_id=:id AND likes.likes=:like')
    result = db.session.execute(sql, {'id':id, 'like':True})
    likes = result.fetchall()
    result = db.session.execute(sql, {'id':id, 'like':False})
    dislikes = result.fetchall()
    return likes, dislikes
