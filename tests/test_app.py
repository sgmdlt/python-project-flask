import pytest
from page_analyzer.app import app as flask_app
from page_analyzer.app import meta, urls_table


@pytest.fixture(scope='session')
def app():
    flask_app.config.update({
        'TESTING': True,
    })
    meta.create_all()
    yield flask_app

    meta.drop_all()


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
    url = urls_table.select().where(urls_table.c.name == 'http://example.com').execute().first()  # noqa: E501
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
    assert response.status_code == 100
    assert 'http://example.com' in response.text
    assert 'http://site.com' in response.text
    assert 'http://hexlet.io' in response.text
