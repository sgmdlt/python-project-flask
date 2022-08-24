from time import strftime
from flask import Flask, render_template


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.template_filter()
    def format_datetime(value):
        return strftime('%Y-%m-%d %H:%M:%S', value.timetuple())

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    from page_analyzer import views
    app.register_blueprint(views.bp)
    return app
