import os

import flask
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from blog.forms.user import UserRegisterForm, LoginForm
from blog.models import User, db
from authlib.integrations.flask_client import OAuth


auth_app = Blueprint("auth_app", __name__)
login_manager = LoginManager()
# login_manager.init_app()
login_manager.login_view = "auth_app.login"
app = flask.current_app
oauth = OAuth(app)



# @vk_app.route('/vk')
# def vk():

@auth_app.route('/vk')
def vk():
    # Facebook Oauth Config
    VK_ID = os.environ.get('VK_ID')
    VK_SECRET = os.environ.get('VK_SECRET')

    oauth.register(
        name='vk',
        client_id=VK_ID,
        client_secret=VK_SECRET,
        redirect_uri='https://oauth.vk.com/authorize',
        response_type='code',
        authorize_url='https://oauth.vk.com/authorize',
        request_token_params=None,
        access_token_params=None,
        authorize_params=None,
        client_kwargs=None,
        display='page',
        revoke=1,
        scope='12',
    )
    redirect_uri = url_for('auth_app.login', _external=True)
    if oauth.vk:
        print('CODE')
        print(oauth.vk)
    return oauth.vk.authorize_redirect(redirect_uri)


@auth_app.route('/auth/')
def vk_auth():
    print('vk_auth start')
    token = oauth.vk.authorize_access_token()
    print('1')
    resp = oauth.vk.get(
        'https://graph.vk.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("VK User ", profile)
    return redirect(url_for('auth_app.login'))



# from flask import Flask, request, make_response, render_template
# from authomatic.adapters import WerkzeugAdapter
# from authomatic import Authomatic
# from authomatic.providers import oauth2
# CONFIG = {
#     'google': {
#         'class_': oauth2.Google,
#         'consumer_key': '########################',
#         'consumer_secret': '########################',
#         'scope': oauth2.Google.user_info_scope + ['https://gdata.youtube.com'],
#     },
# }
# app = Flask(__name__)
# authomatic = Authomatic(CONFIG, 'random secret string for session signing')
# @app.route('/login/<provider_name>/', methods=['GET', 'POST'])
# def login(provider_name):
#     response = make_response()
#     # Authenticate the user
#     result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
#     if result:
#         videos = []
#         if result.user:
#             # Get user info
#             result.user.update()
#             # Talk to Google YouTube API
#             if result.user.credentials:
#                 response = result.provider.access('https://gdata.youtube.com/'
#                     'feeds/api/users/default/playlists?alt=json')
#                 if response.status == 200:
#                     videos = response.data.get('feed', {}).get('entry', [])
#         return render_template(user_name=result.user.name,
#                                user_email=result.user.email,
#                                user_id=result.user.id,
#                                youtube_videos=videos)



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