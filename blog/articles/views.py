from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

articles_app = Blueprint('articles_app', __name__, url_prefix='/articles', static_folder='../static')

ARTICLES = {
    1: {
        'text': 'Как не убираться дома',
        'author': 'Amelia',
        'img': 'None',
        },
    2: {
        'text': 'Как пойти в садик в 1,5 года',
        'author': 'Varvara',
        'img': 'varvarka.png',
        },
    3: {
        'text': 'Покоряем flask в 36',
        'author': 'Papa',
        'img': 'None',
        },
}


@articles_app.route("/")
def articles_list():
    return render_template("articles/list.html", articles=ARTICLES)


@articles_app.route('/<int:pk>')
def get_article(pk: int):
    try:
        article = ARTICLES[pk]
    except KeyError:
        raise NotFound(f'Article id {pk} not found')
    return render_template('articles/details.html', article=article, )
