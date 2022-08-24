import os
import pytest
import sqlite3


from datetime import datetime
from page_analyzer import create_app


DATABASE_URL = 'test_db'
URL = {
    'id': 12,
    'name': 'http://example.com',
    'created_at': datetime.now(),
}

URL_CHECK = {
    'url_id': 12,
    'status_code': 200,
    'h1': 'Example.com best site ever!',
    'title': 'Hello from example.com',
    'description': 'Examples.com is your friend in testing',
    'created_at': datetime.now(),
}


def prepare_db():
    connection = sqlite3.connect(DATABASE_URL)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'schema.sql')) as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()


@pytest.fixture()
def db():
    connect = sqlite3.connect(DATABASE_URL)
    yield connect
    connect.rollback()


@pytest.fixture(scope='session')
def app():
    prepare_db()
    flask_app = create_app()
    flask_app.config.update({
        'TESTING': True,
        'DATABASE_URL': f'sqlite:///{DATABASE_URL}',
    })

    yield flask_app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_urls(client, db):
    client.post('/', data={'url': 'https://ru.code-basics.com'})
    response = client.get('/urls')
    assert response.status_code == 200
    assert 'https://ru.code-basics.com' in response.text


PAGE_CONTENT = '''
<html>
    <head>
        <meta name="description" content="Super courses here!">
        <title>Hexlet</title>
    </head>
    <body>
        <h1>Hexlet Courses</h1>
    </body>
</html>'''


def test_url_checks(client, requests_mock, db):
    url = 'https://ru.code-basics.com'
    requests_mock.get(url, status_code=205, text=PAGE_CONTENT)
    client.post('/', data={'url': url})
    id = db.execute('SELECT id FROM urls WHERE name = ?', (url,)).fetchone()[0]
    client.post(f'/urls/{id}/checks')
    response = client.get(f'urls/{id}')
    assert response.status_code == 200
    assert 'Super courses here!' in response.text
    assert 'Hexlet' in response.text
    assert 'Hexlet Courses' in response.text
