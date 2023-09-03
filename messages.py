from sqlalchemy.sql import text
from db import db
from flask import session, request

def request(choice, other_id):
    sql = text('INSERT INTO requests (content, sender_id, receiver_id, sent_at) VALUES (:content, :sender, :receiver, NOW())')
    db.session.execute(sql, {'content':choice, 'sender':session['user_id'], 'receiver':other_id})
    db.session.commit()
