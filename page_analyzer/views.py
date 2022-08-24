from flask import Blueprint
from bs4 import BeautifulSoup
from flask import abort, flash, render_template
from flask import request, redirect, url_for
from itertools import zip_longest
import requests
from urllib.parse import urlparse
from sqlalchemy import desc
from page_analyzer.db import get_db, get_table


bp = Blueprint('urls', __name__)


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


def parse_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find('title').text
    h1 = soup.find('h1').text
    description = soup.find('meta', attrs={'name': 'description'})
    if description:
        description = description['content']
    return {
        'title': title,
        'h1': h1,
        'description': description,
    }


@bp.route('/', methods=['GET', 'POST'])
def index():
    engine = get_db()
    urls_table = get_table('urls')
    if request.method == 'POST':
        url = request.form['url']

        if not validate_url(url):
            flash('Некорректный URL', 'danger')
            return redirect(url_for('urls.index'))

        normalized_url = normalize(url)
        with engine.begin() as connection:
            existed_url = connection.execute(
                urls_table.select().
                where(urls_table.c.name == normalized_url)).first()
            if existed_url:
                url_id = existed_url.id
                flash('Страница уже существует', 'info')

            else:
                new_url = connection.execute(
                    urls_table.insert().values(
                        name=normalized_url,))
                print('Value inserted!')

                url_id = new_url.inserted_primary_key[0]
            return redirect(url_for('urls.get_url', id=url_id))

    return render_template('index.html')


@bp.route('/urls')
def urls():
    engine = get_db()
    urls_table = get_table('urls')
    urls_checks = get_table('urls_checks')
    with engine.begin() as conn:
        url_list = conn.execute(urls_table.select().order_by('id')).fetchall()
        print('URL_LIST ====> ', url_list)
        checks = conn.execute(
            urls_checks.select().
            distinct('url_id').
            order_by('url_id').
            order_by(desc('created_at'))
        ).fetchmany()
        print('CHECKS ====> ', checks)

    return render_template(
        'urls/index.html',
        urls=zip_longest(url_list, checks),
    )


@bp.route('/urls/<int:id>')
def get_url(id):
    engine = get_db()
    urls_table = get_table('urls')
    urls_checks = get_table('urls_checks')
    with engine.begin() as connection:
        url = connection.execute(
            urls_table.select().
            where(urls_table.c.id == id)).first()
        print('URL ==== ', url)
        if url is None:
            abort(404)
        checks = connection.execute(
            urls_checks.select().where(urls_checks.c.url_id == id)
        )
        checks = sorted(checks, key=lambda x: x.created_at, reverse=True)

    return render_template('urls/url.html', url=url, checks=checks)


@bp.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks(id):
    engine = get_db()
    urls_table = get_table('urls')
    urls_checks = get_table('urls_checks')
    with engine.begin() as connection:
        url = connection.execute(
            urls_table.select().
            where(urls_table.c.id == id)).first()
        try:
            response = requests.get(url.name)
        except requests.ConnectionError:
            flash('Не удалось получить данные', 'danger')
            return redirect(url_for('urls.get_url', id=id))

        page = response.text
        parsed_page = parse_page(page)
        connection.execute(
            urls_checks.insert().values(
                url_id=id,
                status_code=response.status_code,
                h1=parsed_page['h1'],
                title=parsed_page['title'],
                description=parsed_page['description'],
            )
        )
        flash('Страница успешно проверена', 'info')

        return redirect(url_for('urls.get_url', id=id))
