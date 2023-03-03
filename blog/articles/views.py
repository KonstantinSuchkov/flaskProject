from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from blog.models import Article, User

articles_app = Blueprint('articles_app', __name__, url_prefix='/articles', static_folder='../static')


@articles_app.route('/')
def articles_list():
    articles = Article.query.all()
    users = User.query.all()
    return render_template('articles/list.html', articles=articles, users=users)


@articles_app.route('/<int:article_id>')
def get_article(article_id: int):
    article = Article.query.filter_by(id=article_id).one_or_none()
    user = User.query.filter_by(id=article_id).one_or_none()
    print(article)
    try:
        if article is not None:
            return render_template('articles/details.html', article=article, user=user)
        else:
            raise KeyError
    except KeyError:
        raise NotFound(f'Article id {article_id} not found')

