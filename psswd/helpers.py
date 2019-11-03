import functools

from flask import(
    abort, g, redirect, url_for
)
from werkzeug.exceptions import abort
from psswd.db import get_db


def get_account(id, check_user=True):
    account = get_db().execute(
        'SELECT * FROM accounts'
        ' INNER JOIN users ON users.id = accounts.user_id'
        ' WHERE accounts.id = ?', (id,)
    ).fetchone()

    if account is None:
        abort(404, 'Account id {0}, does not exist!'.format(id,))
    
    if check_user and account['user_id'] != g.user['id']:
        abort(403)

    return account


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
