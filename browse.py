from flask import session
from sqlalchemy.sql import text
import users
from db import db
import messages

def fetch_next():
    own_info = users.get_info()
    required_interest = own_info.gender + '_interest'
    applicable_genders = []
    genders = 'fmo'
    for i in range(3):
        if own_info[2+i]:
            applicable_genders.append(genders[i])
    #The next line makes sure the tuple has more than one item so the query works
    applicable_genders.append('x')

    sql = text(f'SELECT u.id FROM users u WHERE u.{required_interest}=True \
        AND u.gender IN {tuple(applicable_genders)} \
        AND u.id != {session["user_id"]} \
        AND NOT EXISTS (SELECT * FROM requests r WHERE u.id=r.sender_id AND r.receiver_id={session["user_id"]}) \
        AND NOT EXISTS (SELECT * FROM requests r WHERE u.id=r.receiver_id AND r.sender_id={session["user_id"]}) \
        AND NOT EXISTS (SELECT * FROM blocks b WHERE u.id=b.blocker_id AND b.blocked_id={session["user_id"]}) \
        AND NOT EXISTS (SELECT * FROM blocks b WHERE u.id=b.blocked_id AND b.blocker_id={session["user_id"]})')

    result = db.session.execute(sql).fetchone()
    if result:
        other_info = users.get_info(result.id)
        other_likes = users.get_likes(result.id)
        return other_info, other_likes, result.id
    return None

def handle_choice(choice, other_id):
    if choice == 'block':
        users.block(other_id)
    else:
        messages.request(choice, other_id)
