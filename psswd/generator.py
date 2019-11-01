from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from psswd import create_app
from werkzeug.exceptions import abort
from psswd.auth import login_required
from psswd.db import get_db


bp = Blueprint('generator', __name__)


@bp.route('/')
@login_required
def index():
    accounts = get_db().execute(
        'SELECT accounts.account as account,'
        ' accounts.password as password,'
        ' accounts.last_password as last_password,'
        ' accounts.updated as updated FROM accounts'
        ' INNER JOIN users ON users.id = accounts.user_id'
        ' WHERE user_id = ?', (session.get('user_id'),)
    ).fetchall()

    return render_template('generator/index.html', accounts=accounts)


@bp.route('/new_account', methods=['GET', 'POST'])
def new_account():
    if request.method == 'POST':
        account = request.form.get('account')
        psswd_min = request.form.get('psswd_min')
        psswd_max = request.form.get('psswd_max')
        error = None

        if not account:
            error = 'Account name required!'
        elif not psswd_min or not psswd_max:
            error = 'Set password boundaries!'
        elif psswd_min < 2 or psswd_max > 25:
            error = 'Password boundaries must be between 2 and 25!'
        elif psswd_min > psswd_max:
            error = 'Password minimum length must be bigger than password maximum length!'
        elif get_db().execute(
            'SELECT id FROM accounts WHERE account = ? AND user_id = ?', (account, session.get('user_id'),)
        ).fetchone() is not None:
            error = 'Account already registered!'
        
        if error is None:
            password = 'TODO'
            get_db().execute(
                'INSERT INTO accounts (user_id, account, password, updated) VALUES (?, ?, ?, ?)',
                (session.get('user_id'), account, password, 1)
            )
            get_db().commit()

            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('generator/new_account.html')
