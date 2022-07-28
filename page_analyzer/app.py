from datetime import datetime
from dotenv import load_dotenv
import os
from flask import Flask, abort, flash, render_template
from flask import request, redirect, url_for
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime  # noqa: E501

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
meta.create_all(engine)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('Url is required!')
        elif len(url) > 255:
            flash('Url is too long')
        else:
            with engine.begin() as connection:
                existed_url = connection.execute(
                    urls_table.select().where(urls_table.c.name == url)).first()
                if existed_url:
                    flash('Url was already added')
                else:
                    connection.execute(urls_table.insert().values(name=url))
                    return redirect(url_for('urls'))

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
    return render_template('urls/url.html', url=url)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
