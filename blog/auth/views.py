import os

import flask
from flask import Blueprint, render_template, request, redirect, url_for, current_app, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from blog.forms.user import UserRegisterForm, LoginForm
from blog.models import User, db
from authlib.integrations.flask_client import OAuth


auth_app = Blueprint("auth_app", __name__)
login_manager = LoginManager()
# login_manager.init_app()
login_manager.login_view = "auth_app.login"
app = flask.current_app
oauth = OAuth(app)

github = oauth.register(
    name='flaskProject',
    client_id=os.getenv("GITHUB_ID"),
    client_secret=os.getenv("GITHUB_SECRET"),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@auth_app.route('/login')
def registro():
    github = oauth.create_client('flaskProject')
    redirect_uri = url_for('auth_app.authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@auth_app.route('/authorize')
def authorize():
    github = oauth.create_client('flaskProject')
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    profile = resp.json()
    print(profile, token)
    info = github.get("/user")
    if info.ok:
        account_info = info.json()
        username = account_info["login"]
        img = account_info["avatar_url"]
        query = User.query.filter_by(username=username)
        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username, img=img)
            db.session.add(user)
            db.session.commit()
        login_user(user)
    return redirect(url_for('user_app.details', pk=current_user.id))


@auth_app.route('/')
def vk():
    VK_ID = os.environ.get('VK_ID')
    VK_SECRET = os.environ.get('VK_SECRET')
    name='flaskProject'
    client_id=VK_ID
    client_secret=VK_SECRET
    redirect_uri='https://oauth.vk.com/authorize'
    response_type='code'
    authorize_url='https://oauth.vk.com/authorize'
    access_token_url='https://oauth.vk.com/access_token'
    token_endpoint_auth_method='none'
    display='page'
    revoke=1
    scope='12'
    return redirect(f'{redirect_uri}?client_id={client_id}&display={display}&redirect_uri=http://127.0.0.1:5000/auth/response_type=code&v=5.131')


@auth_app.route("/register/", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect("index")
    error = None
    form = UserRegisterForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append("username already exists!")
            return render_template("auth/register.html", form=form)
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("auth/register.html", form=form)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            is_staff=False,
        )
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for('user_app.details', pk=current_user.id))
    return render_template("auth/register.html", form=form, error=error)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_app.login"))

@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if current_user.is_authenticated:
        return redirect("users")
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user is None:
            return render_template("auth/login.html", form=form, error="username doesn't exist")
        if not user.validate_password(form.password.data):
            return render_template("auth/login.html", form=form, error="invalid username or password")
        login_user(user)
        return redirect(url_for('user_app.details', pk=current_user.id))
    return render_template("auth/login.html", form=form)


@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_app.login"))


@auth_app.route("/secret/")
@login_required
def secret_view():
    return "Super secret data"

__all__ = [
    "login_manager",
    "auth_app",
]