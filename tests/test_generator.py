import pytest

from flask import g, session
from psswd.db import get_db


def test_index(client, auth):
    auth.login()
    assert client.get('/').status_code == 200


def test_new_account(client, auth, app):
    auth.login()
    assert client.get('/new_account').status_code == 200
    
    response = client.post(
        '/new_account',
        data={'account': 'a', 'psswd_min': '5', 'psswd_max': '10'}
    )
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM accounts WHERE account = 'a'" 
        ).fetchone() is not None
    

@pytest.mark.parametrize(('account', 'psswd_min', 'psswd_max', 'message'), (
    ('', '', '', b'Account name required!'),
    ('a', '', '', b'Set password boundaries!'),
    ('a', '5', '3', b'Password minimum length must be smaller than password maximum length!'),
    ('a', '1', '5', b'Password boundaries must be between 2 and 25!'),
    ('a', '3', '26', b'Password boundaries must be between 2 and 25!'),
    ('test_acc', '2', '25', b'already registered!'),
))


def test_new_account_validate_input(auth, client, account, psswd_min, psswd_max, message):
    auth.login()
    response = client.post(
        '/new_account',
        data={'account': account, 'psswd_min': psswd_min, 'psswd_max': psswd_max}
    )
    assert message in response.data
