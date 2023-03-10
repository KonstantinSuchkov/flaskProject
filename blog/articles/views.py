from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from blog import Author
from blog.forms.article import CreateArticleForm
from blog.models import Article, User
from blog.models.database import db

articles_app = Blueprint('articles_app', __name__, url_prefix='/articles', static_folder='../static')


@articles_app.route("/", endpoint="list")
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


@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), text=form.text.data)
        db.session.add(article)
        if current_user.author:
            # use existing author if present
            article.author = current_user.author
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author = author
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("articles_app.get_article", article_id=article.id))
    return render_template("articles/create.html", form=form, error=error)
