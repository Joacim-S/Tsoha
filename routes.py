from flask import redirect, render_template, request
from app import app
import users
import browse as b
import messages as m

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
    result = users.login(username, password)
    if not result:
        return render_template('index.html', credential_error=True)
    if result == 'new':
        return redirect ('/update_info')
    return redirect('/')

@app.route('/create', methods=['POST'])
def create():
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    create_result = users.create_user(username, password1, password2)
    if create_result != 'new':
        return render_template('register.html', error=create_result)
    return redirect('/update_info')

@app.route('/my_profile', methods=['GET'])
def my_profile():
    info = users.get_info()
    likes, dislikes = users.get_likes()
    return render_template('my_profile.html', displayname = info[0],
        gender = users.translate_gender(info[1]),
        f_interest = info[2], m_interest = info[3], o_interest = info[4],
        dob = info[5].strftime('%d.%m.%Y'),
        likes = likes, dislikes = dislikes)

@app.route('/my_likes', methods=['GET', 'POST'])
def my_likes():
    if request.method == 'POST':
        users.check_csrf()
        item = request.form['item']
        like = request.form['like']
        users.update_like(item, like)

    likes, dislikes = users.get_likes()
    return render_template('my_likes.html', likes = likes, dislikes = dislikes)


@app.route('/update_info', methods=['GET', 'POST'])
def update_info():
    if request.method == 'POST':
        users.check_csrf()
        displayname = request.form['displayname']
        radiovalues = []
        radios = ['gender', 'f_interest', 'm_interest', 'o_interest']
        for i in range(4):
            try:
                radiovalues.append(request.form[radios[i]])
            except:
                radiovalues.append(None)

        dob = request.form['dob']
        result = users.update_info([displayname, radiovalues[0], radiovalues[1],
            radiovalues[2], radiovalues[3], dob])
        if result[0] or result[1] or result[2]:
            return render_template('update_info.html', date_error = result[0],
                                    missing_info = result[1], failed = result[2])
        return redirect('/my_profile')

    return render_template('update_info.html')

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    if request.method == 'POST':
        users.check_csrf()
        choice = request.form['choice']
        other_id = request.form['id']
        b.handle_choice(choice, other_id)

    profile = b.fetch_next()
    if not profile:
        return render_template('browse.html', not_found = True)
    age = users.calculate_age(profile[0].dob)
    return render_template('browse.html', displayname = profile[0][0],
                            gender = users.translate_gender(profile[0][1]),
                            age = age, likes = profile[1][0],
                            dislikes = profile[1][1], id = profile[2])


@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')

@app.route('/requests', methods=['GET', 'POST'])
def requests():
    if request.method == 'POST':
        users.check_csrf()
        choice = request.form['choice']
        other_id = request.form['id']
        m.answer_request(choice, other_id)

    profile = m.next_request()
    if not profile:
        return render_template('browse.html', not_found = True, mode=True)
    age = users.calculate_age(profile[0].dob)
    return render_template('browse.html', displayname = profile[0][0],
                            gender = users.translate_gender(profile[0][1]),
                            age = age, likes = profile[1][0],
                            dislikes = profile[1][1],
                            id = profile[2], mode=True)

@app.route('/convos', methods=['GET'])
def convos():
    convolist = m.get_convos()
    return render_template('convos.html', convos=convolist)

@app.route('/messages/<int:convo_id>/<name>/<int:uid>', methods=['GET', 'POST'])
def messages(convo_id, name, uid):
    if not m.check_permission(convo_id):
        return render_template('index.html', message='''Palasit etusivulle, yritit
        avata sivun, jonka katseluun sinulla ei ole oikeutta.''')

    if request.method == 'POST':
        users.check_csrf()
        m.send_message(request.form['content'], uid, convo_id)

    msgs = m.get_messages(convo_id)
    block_status = users.check_block(uid)
    return render_template('messages.html', msgs=msgs, convo_id=convo_id,
                            name=name, uid=uid, block_status=block_status)

@app.route('/block/<int:uid>/<name>', methods=['GET', 'POST'])
def block(uid, name):
    if request.method == 'GET':
        return render_template('block.html', uid=uid, name=name)

    if request.method == 'POST':
        users.check_csrf()
        if request.form['block'] == 'True':
            users.block(uid)
            return render_template('index.html', message='Käyttäjä estettiin.')

        users.cancel_block(uid)
        return render_template('index.html', message='Esto peruttiin.')

@app.route('/reset')
def reset():
    users.reset_skips()
    return render_template('index.html', message='Ohitukset nollattiin.')
