import flask_migrate
from flask import Flask
from blog.articles.views import articles_app
from blog.auth.views import auth_app
from blog.models.database import db
from blog.user.views import users_app
import os

os.environ['CONFIG_NAME'] = 'DevConfig'
migrate = flask_migrate.Migrate()


def create_app() -> Flask:
    app = Flask(__name__)
    cfg_name = os.environ.get('CONFIG_NAME')
    app.config.from_object(f'blog.configs.{cfg_name}')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(auth_app, url_prefix='/auth')
    app.register_blueprint(users_app)
    app.register_blueprint(articles_app)
