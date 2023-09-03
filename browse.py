from flask import session
from sqlalchemy.sql import text
from flask import session
import users
from db import db
import messages

def fetch_next():
    own_info = users.get_info()
    required_interest = own_info.gender + '_interest'
    applicable_genders = []
    genders = ('fmo')
    for i in range(3):
        if own_info[2+i]:
            applicable_genders.append(genders[i])
    applicable_genders.append('x')

    print(tuple(applicable_genders))
    sql = text(f'SELECT id FROM users WHERE {required_interest}=True AND gender IN {tuple(applicable_genders)} AND id!={session["user_id"]}')
    result = db.session.execute(sql).fetchone()
    if result:
        other_info = users.get_info(result.id)
        other_likes = users.get_likes(result.id)
        return other_info, other_likes, result.id
    return

def handle_choice(choice, other_id):
    if choice == 'block':
        users.block(other_id)
        return
    
    messages.request(choice, other_id)