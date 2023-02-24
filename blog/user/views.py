from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from blog.articles.views import ARTICLES

user = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')
USERS = {
    1: 'Amelia',
    2: 'Varvara',
    3: 'Papa',
}

@user.route('/')
def user_list():
    return render_template('users/list.html', users=USERS, articles=ARTICLES)


@user.route('/<int:pk>')
def get_user(pk: int):
    try:
        user_name = USERS[pk]
        img = ARTICLES[pk]['img']
    except KeyError:
        raise NotFound(f'User id {pk} not found')
    return render_template('users/details.html', user_name=user_name, img=img)
