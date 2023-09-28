from sqlalchemy.sql import text
from flask import session
from db import db
import users

def request(choice, other_id):
    sql = text('INSERT INTO requests (content, sender_id, receiver_id, sent_at) VALUES \
                (:content, :sender, :receiver, NOW())')
    db.session.execute(sql, {'content':choice, 'sender':session['user_id'], 'receiver':other_id})
    db.session.commit()

def next_request():
    sql = text(f'SELECT sender_id FROM requests WHERE receiver_id={session["user_id"]} \
                AND content=True AND answer IS NULL')
    result = db.session.execute(sql).fetchone()
    if result:
        other_info = users.get_info(result.sender_id)
        other_likes = users.get_likes(result.sender_id)
        return other_info, other_likes, result.sender_id
    return None

def answer_request(choice, other_id):
    if choice == 'block':
        users.block(other_id)
    sql = text('UPDATE requests SET answer=:choice, sent_at=NOW() \
                WHERE receiver_id=:user_id AND sender_id=:other_id')
    db.session.execute(sql, {'user_id':session['user_id'], 'choice':choice, 'other_id':other_id})
    db.session.commit()
    sql = text('SELECT id FROM requests WHERE receiver_id=:user_id AND sender_id=:other_id')
    convo_id = db.session.execute(sql, {'user_id':session['user_id'],
                'other_id':other_id}).fetchone().id
    send_message('Pyyntö hyväksytty', other_id, convo_id)

def send_message(content, receiver_id, convo_id):
    sql = text('INSERT INTO messages (content, receiver_id, convo_id, sender_id, sent_at) VALUES \
                (:content, :receiver, :convo_id, :sender, NOW())')
    db.session.execute(sql, {'content':content, 'receiver':receiver_id,
                        'convo_id':convo_id, 'sender':session['user_id']})
    db.session.commit()

def get_convos():
    sql = text('SELECT DISTINCT u.displayname, m.convo_id, \
                (SELECT content FROM messages WHERE \
                convo_id=m.convo_id ORDER BY sent_at DESC LIMIT 1), u.id \
                FROM users u, messages m WHERE \
                (u.id=m.receiver_id AND m.sender_id=:user_id) \
                OR (u.id=m.sender_id AND m.receiver_id=:user_id)')
    result = db.session.execute(sql, {'user_id':session['user_id']}).fetchall()
    return result

def check_permission(convo_id):
    sql = text('SELECT sender_id, receiver_id FROM messages WHERE \
                convo_id=:convo_id AND \
                (sender_id=:user_id OR receiver_id=:user_id)')
    result = db.session.execute(sql, {'convo_id':convo_id, 'user_id':session['user_id']}).fetchone()
    if result:
        return True
    else:
        return False

def get_messages(convo_id):
    sql = text('SELECT u.displayname, m.content, m.sent_at FROM \
                users u, messages m WHERE \
                m.convo_id=:convo_id AND u.id=sender_id ORDER BY sent_at')
    result = db.session.execute(sql, {'convo_id':convo_id}).fetchall()
    return result
