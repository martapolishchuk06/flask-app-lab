from flask import render_template, request, redirect, url_for, flash, session, make_response
from . import users_bp

USERS = {
    "user1": "password123",
    "admin": "admin"
}

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type=int)
    return render_template("users/hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Ви успішно увійшли в систему!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Wrong data! Try again!', 'danger')
            return redirect(url_for('users.login'))
            
    return render_template('users/login.html')

@users_bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть у систему!', 'danger')
        return redirect(url_for('users.login'))
    
    theme = request.cookies.get('theme', 'light')
    cookies_list = request.cookies
    return render_template('users/profile.html', username=session['username'], theme=theme, cookies=cookies_list)

@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/add_cookie', methods=['POST'])
def add_cookie():
    key = request.form.get('key')
    val = request.form.get('value')
    max_age = request.form.get('max_age', 3600)
    
    resp = make_response(redirect(url_for('users.profile')))
    if key and val:
        resp.set_cookie(key, val, max_age=int(max_age))
        flash(f'Кукі "{key}" успішно додано!', 'success')
    return resp

@users_bp.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    key = request.form.get('key')
    resp = make_response(redirect(url_for('users.profile')))
    if key:
        resp.delete_cookie(key)
        flash(f'Кукі "{key}" видалено!', 'info')
    return resp

@users_bp.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    resp = make_response(redirect(url_for('users.profile')))
    for key in request.cookies:
        resp.delete_cookie(key)
    flash('Всі кукі видалено!', 'warning')
    return resp

@users_bp.route('/set_theme/<theme_name>')
def set_theme(theme_name):
    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie('theme', theme_name)
    flash(f'Тему змінено на {theme_name}!', 'info')
    return resp