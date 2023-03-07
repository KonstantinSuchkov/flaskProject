from flask_login import LoginManager
from flask_migrate import Migrate
from flask import Flask
from flask_wtf import CSRFProtect
from blog import User
from blog.articles.views import articles_app
from blog.auth.views import auth_app
from blog.models.database import db
from blog.security import flask_bcrypt, csrf
from blog.user.views import users_app
import os



# os.environ['CONFIG_NAME'] = 'DevConfig'


login_manager = LoginManager()
migrate = Migrate()


def create_app() -> Flask:
    print('start!')
    app = Flask(__name__)
    app.config.from_object('blog.configs')

    register_extensions(app)
    register_blueprints(app)
    create_init_user(app)
    create_articles(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)

    flask_bcrypt.init_app(app)

    login_manager.login_view = 'auth_app.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    app.register_blueprint(auth_app, url_prefix='/auth')
    app.register_blueprint(users_app)
    app.register_blueprint(articles_app)


def create_init_user(app):
    from blog.models import User
    print('starting create users...')
    with app.app_context():
        db.create_all()
        admin = User(username="admin", is_staff=True, password='123')
        # admin.password = os.environ.get("123") or "adminpass"
        amelia = User(username="Amelia")
        varvara = User(username='Varvara', img='varvarka.png')
        db.session.add(admin)
        db.session.add(amelia)
        db.session.add(varvara)
        db.session.commit()
        print("done! created users:", admin, amelia, varvara)


def create_articles(app):
    from blog.models import Article
    print('starting create articles...')
    with app.app_context():
        admin = Article(text='Покоряем flask в 36', author='admin')
        amelia = Article(text='Интриги и скандалы', author='Amelia')
        varvara = Article(text='Два месяца в детском садике', author='Varvara')
        db.session.add(admin)
        db.session.add(amelia)
        db.session.add(varvara)
        db.session.commit()
        print("done! created articles:", admin, amelia, varvara)
