from app import app
from flask import redirect, render_template, request
import users
import browse as b

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
    return render_template('my_profile.html', displayname = info[0], gender = users.translate_gender(info[1]), f_interest = info[2], 
                            m_interest = info[3], o_interest = info[4], dob = info[5], likes = likes, dislikes = dislikes)

@app.route('/my_likes', methods=['GET', 'POST'])
def my_likes():

    if request.method == 'GET':
        likes, dislikes = users.get_likes()
        return render_template('my_likes.html', likes = likes, dislikes = dislikes)

    if request.method == 'POST':
        users.check_csrf()
        item = request.form['item']
        like = request.form['like']
        users.update_like(item, like)
        likes, dislikes = users.get_likes()
        return render_template('my_likes.html', likes = likes, dislikes = dislikes)


@app.route('/update_info', methods=['GET', 'POST'])
def update_info():
    if request.method == 'GET':
        return render_template('update_info.html')

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
        result = users.update_info([displayname, radiovalues[0], radiovalues[1], radiovalues[2], radiovalues[3], dob])
        if result[0] or result[1] or result[2]:
            return render_template('update_info.html', date_error = result[0], missing_info = result[1], failed = result[2])
        return redirect('/my_profile')

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
    return render_template('browse.html', user = profile[0], likes = profile[1], id = profile[2])


@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')