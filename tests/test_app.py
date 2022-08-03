import pytest
from page_analyzer.app import app as flask_app
from page_analyzer.app import engine, urls_table, meta


@pytest.fixture(scope='session')
def app():
    flask_app.config.update({
        'TESTING': True,
    })

    meta.create_all(engine)
    yield flask_app


@pytest.fixture
def data():
    urls = [
        'http://example.com',
        'http://site.com',
        'http://hexlet.io',
    ]
    yield urls

    engine.execute(urls_table.delete().where(urls_table.c.name.in_(urls)))


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert '<form method="post">' in response.text


def test_add_urls(client, data):
    for url in data:
        response = client.post('/', data={'url': url})
        assert response.status_code == 302
    with engine.begin() as conn:
        url1 = conn.execute(
            urls_table.select().where(urls_table.c.name == 'http://example.com')
        ).first()
        url2 = conn.execute(
            urls_table.select().where(urls_table.c.name == 'http://site.com')
        ).first()
        url3 = conn.execute(
            urls_table.select().where(urls_table.c.name == 'http://hexlet.io')
        ).first()
    assert url1.name == 'http://example.com'
    assert url2.name == 'http://site.com'
    assert url3.name == 'http://hexlet.io'


def test_data_flushes():
    with engine.begin() as conn:
        data = conn.execute(
            urls_table.select().where(urls_table.c.name == 'http://example.com')
        ).first()
        assert data is None


def test_urls_view(client, data):
    for url in data:
        response = client.post('/', data={'url': url})
        assert response.status_code == 302
    response = client.get('/urls')
    print(response.text)
    assert response.status_code == 200
    assert 'http://example.com' in response.text
    assert 'http://site.com' in response.text
    assert 'http://hexlet.io' in response.text
