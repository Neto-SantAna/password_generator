import pytest

from flask import g, session
from psswd.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').satus_code == 200

    response = client.post(
        '/auth/register',
        data={'username': 'a', 'email': 'a@a.com', 'password': 'a', 'psswd_cf': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM users WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'email', 'password', 'psswd_cf', 'message'), (
    ('', '', '', '', b'Username and password are required!'),
    ('a', '', '', '', b'Username and password are required!'),
    ('', '', 'a', '', b'Username and password are required!'),
    ('a', '', 'a', '', b'Confirm your password!'),
    ('a', '', 'a', 'a', b'Provide an email for possible recover of passwords!'),
    ('a', 'a@a.com', 'a', 'b', b"Password doesn't match its confirmation!"),
    ('test', 'test@test.com', 'test', 'test', b'already registered'),
))


def test_register_validate_input(client, username, email, password, psswd_cf, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'email': email, 'password': password, 'psswd_cf': psswd_cf}
    )

    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username!'),
    ('test', 'a', b'Incorrect password!'),
))


def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)

    assert message in response.data
