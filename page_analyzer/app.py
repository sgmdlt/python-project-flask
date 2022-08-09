from datetime import datetime
from dotenv import load_dotenv
import os
from flask import Flask, abort, flash, render_template
from flask import request, redirect, url_for
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey  # noqa: E501
from urllib.parse import urlparse

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = {
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database_name': os.getenv('DB_NAME'),
}
app.config['DATABASE_URL'] = os.getenv(
    'DATABASE_URL',
    'postgresql://{username}:{password}@{host}/{database_name}'.format(**db),  # noqa: E501
).replace('postgres://', 'postgresql://')

engine = create_engine(app.config['DATABASE_URL'])
meta = MetaData()


urls_table = Table(
    'urls', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), unique=True),
    Column('created_at', DateTime, default=datetime.now),
)

urls_checks = Table(
    'urls_checks', meta,
    Column('id', Integer, primary_key=True),
    Column('url_id', Integer, ForeignKey('urls.id', ondelete='CASCADE', onupdate='CASCADE')),  # noqa: E501
    Column('status_code', Integer),
    Column('h1', String(255)),
    Column('title', String(255)),
    Column('description', String(255)),
    Column('created_at', DateTime, default=datetime.now),
)

meta.create_all(engine)


def validate_url(url):
    if not url:
        return False
    if len(url) > 255:
        return False
    o = urlparse(url)
    if not (o.netloc and o.scheme):
        return False
    return True


def normalize(url):
    o = urlparse(url)
    return f'{o.scheme}://{o.netloc}'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']

        if not validate_url(url):
            flash('Некорректный URL', 'danger')
            return redirect(url_for('index'))

        normalized_url = normalize(url)
        with engine.begin() as connection:
            existed_url = connection.execute(
                urls_table.select().where(
                    urls_table.c.name == normalized_url)
            ).first()
            if existed_url:
                id = existed_url.id
                flash('Страница уже существует', 'info')
            else:
                new_url = connection.execute(
                    urls_table.insert().values(name=normalized_url))
                id = new_url.inserted_primary_key[0]
            return redirect(url_for('get_url', id=id))

    return render_template('index.html')


@app.route('/urls')
def urls():
    with engine.begin() as connection:
        url_list = connection.execute(urls_table.select())
    return render_template('urls/index.html', urls=url_list)


@app.route('/urls/<int:id>')
def get_url(id):
    with engine.begin() as connection:
        url = connection.execute(
            urls_table.select().where(urls_table.c.id == id)
        ).first()
        if url is None:
            abort(404)
        checks = connection.execute(
            urls_checks.select().where(urls_checks.c.url_id == id)
        )

    return render_template('urls/url.html', url=url, checks=checks)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks(id):
    with engine.begin() as connection:
        connection.execute(
            urls_checks.insert().values(
                url_id=id,
                created_at=datetime.now(),
            ))
    return redirect(url_for('get_url', id=id))
