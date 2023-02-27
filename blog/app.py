from flask import Flask
from blog.articles.views import articles_app
from blog.auth.views import auth_app
from blog.models.database import db
from blog.user.views import users_app


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqLite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # from .models import *
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(auth_app, url_prefix="/auth")
    app.register_blueprint(users_app)
    app.register_blueprint(articles_app)


