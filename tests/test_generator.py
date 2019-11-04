import pytest

from flask import g, session
from psswd.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert response.headers['Location'] == 'http://localhost/auth/login'

    auth.login()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Log Out' in response.data
    assert b'Test_acc' in response.data
    assert b'123' in response.data
    assert b'12345' in response.data
    assert b'Update' in response.data
    assert b'&times;' in response.data


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
            "SELECT * FROM accounts WHERE account = 'A'" 
        ).fetchone() is not None
    

@pytest.mark.parametrize(('account', 'psswd_min', 'psswd_max', 'message'), (
    ('', '', '', b'Account name required!'),
    ('a', '', '', b'Set password boundaries!'),
    ('a', '5', '3', b'Password minimum length must be smaller than password maximum length!'),
    ('a', '1', '5', b'Password boundaries must be between 2 and 25!'),
    ('a', '3', '26', b'Password boundaries must be between 2 and 25!'),
    ('test_acc', '2', '25', b'already registered'),
))


def test_new_account_validate_input(auth, client, account, psswd_min, psswd_max, message):
    auth.login()
    response = client.post(
        '/new_account',
        data={'account': account, 'psswd_min': psswd_min, 'psswd_max': psswd_max}
    )
    assert message in response.data


def test_update(client, auth, app):
    auth.login()
    resonse = client.post('/1/update')
    assert resonse.headers['Location'] == 'http://localhost/'

    with app.app_context():
        account = get_db().execute(
            'SELECT * FROM accounts WHERE id = 1'
        ).fetchone()
        assert account['updated'] == 0


def test_updated(client, auth, app):
    auth.login()
    response = client.post('/1/updated')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        account = get_db().execute(
            'SELECT * FROM accounts WHERE id = 1'
        ).fetchone()
        assert account['updated'] == 1


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        account = get_db().execute(
            'SELECT * FROM accounts WHERE id = 1'
        ).fetchone()
        assert account is None


def test_user_required(app, client, auth):
    with app.app_context():
        get_db().execute(
            'UPDATE accounts SET user_id = 2 WHERE id = 1'
        )
        get_db().commit()
    
    auth.login()
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/updated').status_code == 403
    assert client.post('/1/delete').status_code == 403


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/updated',
    '/2/delete',
))


def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404
