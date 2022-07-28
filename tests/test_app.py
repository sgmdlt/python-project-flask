import pytest
from page_analyzer.app import app as flask_app
from page_analyzer.app import engine, urls_table, meta


@pytest.fixture(scope='session')
def app():
    flask_app.config.update({
        'TESTING': True,
        'DATABASE_URL': 'sqlite:///:memory:',
    })

    meta.create_all(engine)
    yield flask_app
    meta.drop_all(engine)


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert '<form method="post">' in response.text


def test_add_url(client):
    response = client.post('/', data={'url': 'http://example.com'})
    assert response.status_code == 302
    with engine.begin() as conn:
        url = conn.execute(
            urls_table.select().where(urls_table.c.name == 'http://example.com')
        ).first()
    assert url.name == 'http://example.com'


def test_url_view(client):
    response = client.get('/urls/1')
    assert response.status_code == 200
    assert 'http://example.com' in response.text


def test_urls_view(client):
    client.post('/', data={'url': 'http://example.com'})
    client.post('/', data={'url': 'http://site.com'})
    client.post('/', data={'url': 'http://hexlet.io'})
    response = client.get('/urls')
    print(response.text)
    assert response.status_code == 200
    assert 'http://example.com' in response.text
    assert 'http://site.com' in response.text
    assert 'http://hexlet.io' in response.text
