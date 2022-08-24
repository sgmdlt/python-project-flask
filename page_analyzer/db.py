from sqlalchemy import create_engine, MetaData
from flask import current_app, g


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        print('DATABASE_URL ===>', current_app.config['DATABASE_URL'])
        db = g._database = create_engine(current_app.config['DATABASE_URL'], echo=True)
    return db


def get_table(name):
    engine = get_db()
    meta = MetaData()
    meta.reflect(bind=engine)
    tables = meta.tables
    return tables.get(name)
