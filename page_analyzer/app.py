import os
from flask import Flask, flash, render_template, request, redirect, url_for
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = {
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database_name': os.getenv('DB_NAME'),
}
db_ulr = 'postgresql://{username}:{password}@{host}:{port}/{database_name}'.format(**db)


engine = create_engine(db_ulr)
metadata = MetaData(bind=engine)


urls = Table(
    'urls', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), unique=True),
    Column('created_at', DateTime),
)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('Url is required!')
        elif len(url) > 255:
            flash('Url is too long')
        else:
            return redirect(url_for('urls'))
    return render_template('index.html')


@app.route('/urls')
def urls():
    return 'urls'
