import os
import tempfile
import pytest
import app


def login(client, username, password):
    return client.post('/auth/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


@pytest.fixture
def client():
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True
    app.app.config['SQLALCHEMY_DATABASE_URI'] = tempfile.mkstemp()

    with app.app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])


def test_redirect_to_login(client):
    rv = client.get('/')
    assert b'<a href="/auth/login">' in rv.data
    assert 302 == rv.status_code


def pending_test_login_logout(client):
    """Make sure login and logout works."""

    username = 'test'
    password = 'testpass'

    rv = login(client, username, password)
    assert b'You were logged in' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, username + 'x', password)
    assert b'Invalid username' in rv.data

    rv = login(client, username, password + 'x')
    assert b'Invalid password' in rv.data
