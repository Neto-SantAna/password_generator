import random
import string

from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from psswd import create_app
from werkzeug.exceptions import abort
from psswd.helpers import (
    login_required, get_account
)
from psswd.db import get_db


bp = Blueprint('generator', __name__)
chars = string.ascii_lowercase + string.ascii_uppercase + string.punctuation + string.digits


@bp.route('/')
@login_required
def index():
    accounts = get_db().execute(
        'SELECT accounts.id as id,'
        ' accounts.account as account,'
        ' accounts.password as password,'
        ' accounts.last_password as last_password,'
        ' accounts.updated as updated FROM accounts'
        ' INNER JOIN users ON users.id = accounts.user_id'
        ' WHERE user_id = ?', (session.get('user_id'),)
    ).fetchall()
        
    return render_template('generator/index.html', accounts=accounts)


@bp.route('/new_account', methods=['GET', 'POST'])
@login_required
def new_account():
    if request.method == 'POST':
        account = request.form.get('account').capitalize()
        psswd_min = request.form.get('psswd_min')
        psswd_max = request.form.get('psswd_max')
        error = None

        if not account:
            error = 'Account name required!'
        elif not psswd_min or not psswd_max:
            error = 'Set password boundaries!'
        elif int(psswd_min) > int(psswd_max):
            error = 'Password minimum length must be smaller than password maximum length!'
        elif int(psswd_min) < 2 or int(psswd_max) > 25:
            error = 'Password boundaries must be between 2 and 25!'

        elif get_db().execute(
            'SELECT id FROM accounts WHERE account = ? AND user_id = ?', (account, session.get('user_id'),)
        ).fetchone() is not None:
            error = 'Account already registered!'
        
        if error is None:
            psswd_len = random.SystemRandom().randint(int(psswd_min), int(psswd_max))
            password = ''.join(random.SystemRandom().choice(chars) for x in range(psswd_len))
            last_password = 'No password record!'

            get_db().execute(
                'INSERT INTO accounts (user_id, account, psswd_min, psswd_max, password, last_password, updated) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (session.get('user_id'), account, psswd_min, psswd_max, password, last_password, 1)
            )
            get_db().commit()

            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('generator/new_account.html')


@bp.route('/<int:id>/updated', methods=['POST'])
@login_required
def updated(id):
    get_account(id)
    get_db().execute(
        'UPDATE accounts SET updated = 1 WHERE id = ?', (id,)
    )
    get_db().commit()

    return redirect(url_for('index'))


@bp.route('/<int:id>/update', methods=['POST'])
@login_required
def update(id):
    account = get_account(id)
    psswd_len = random.SystemRandom().randint(int(account['psswd_min']), int(account['psswd_max']))
    password = ''.join(random.SystemRandom().choice(chars) for x in range(psswd_len))
    last_password = account['password']
 
    get_db().execute(
        'UPDATE accounts SET last_password = ?, password = ?, updated = 0 WHERE id = ?', (last_password, password, id,)
    )
    get_db().commit()

    return redirect(url_for('index'))


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    get_account(id)
    get_db().execute('DELETE FROM accounts WHERE id = ?', (id,))
    get_db().commit()

    return redirect(url_for('index'))
