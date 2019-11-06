import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from psswd.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        psswd_cf = request.form.get('psswd_cf')
        email = request.form.get('email')
        error = None

        if not username or not password:
            error = 'Username and password are required!'
        elif not psswd_cf:
            error = 'Confirm your password!'
        elif not email:
            error = 'Provide an email for possible recover of passwords!'
        elif password != psswd_cf:
            error = 'Password does not match its confirmation!'
        elif get_db().execute(
            'SELECT id from users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered!'.format(username)

        if error is None:
            get_db().execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, generate_password_hash(password))
            )
            get_db().commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        user = get_db().execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username!'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password!'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
