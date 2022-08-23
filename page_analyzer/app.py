from time import strftime
from flask import Flask, render_template
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey  # noqa: E501
from datetime import datetime


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.template_filter()
    def format_datetime(value):
        return strftime('%Y-%m-%d %H:%M:%S', value.timetuple())

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    app.config['db'] = create_engine(app.config['DATABASE_URL'], echo=True)
    meta = MetaData(bind=app.config['db'])
    urls = Table(
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
    meta.create_all(app.config['db'])  # noqa: E501

    app.config['urls'] = urls
    app.config['urls_checks'] = urls_checks

    from page_analyzer import views
    app.register_blueprint(views.bp)
    return app
