from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from psswd.auth import login_required
from psswd.db import get_db


bp = Blueprint('generator', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    user_id = session.get('user_id')
    accounts = db.execute(
        'SELECT accounts.account as account,'
        ' accounts.password as password,'
        ' accounts.last_password as last_password,'
        ' accounts.updated as updated FROM accounts'
        ' INNER JOIN users ON users.id = accounts.user_id'
        ' WHERE user_id = ?', (user_id,)
    ).fetchall()

    return render_template('generator/index.html', accounts=accounts)
