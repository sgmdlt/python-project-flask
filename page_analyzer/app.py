from datetime import datetime
import os
from flask import Flask, flash, render_template, request, redirect, url_for
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime  # noqa: E501

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = {
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database_name': os.getenv('DB_NAME'),
}
db_ulr = os.getenv(
    'DATABASE_URL',
    'postgresql://{username}:{password}@{host}:{port}/{database_name}'.format(**db),  # noqa: E501
)

engine = create_engine(db_ulr)
meta = MetaData(bind=engine)
urls = Table(
    'urls', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), unique=True),
    Column('created_at', DateTime),
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
            existed_url = engine.execute(
                urls.select().where(urls.c.name == url)
            ).first()
            if existed_url:
                flash('Url was already added')
            else:
                engine.execute(urls.insert().values(
                    name=url,
                    created_at=datetime.now()))
            return redirect(url_for('get_urls'))

    return render_template('index.html')


@app.route('/urls')
def get_urls():
    url_list = engine.execute(urls.select())
    return render_template('urls/index.html', urls=url_list)
