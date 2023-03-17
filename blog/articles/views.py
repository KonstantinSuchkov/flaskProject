from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from blog import Author, Tag
from blog.forms.article import CreateArticleForm
from blog.models import Article, User
from blog.models.database import db

articles_app = Blueprint('articles_app', __name__, url_prefix='/articles', static_folder='../static')


@articles_app.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    users = User.query.all()
    authors = Author.query.all()
    return render_template('articles/list.html', articles=articles, users=users, authors=authors)


@articles_app.route('/<int:article_id>')
def get_article(article_id: int):
    article = Article.query.filter_by(id=article_id).options(joinedload(Article.tags)).one_or_none()  # подгружаем связанные теги!
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
    # добавляем доступные теги в форму
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), text=form.text.data)
        db.session.add(article)
        if form.tags.data:  # если в форму были переданы теги (были выбраны)
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)  # добавляем выбранные теги к статье
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


@articles_app.route("/<text>", endpoint="text")
def text_to_mp3(text='тест один два три', language='ru'):
    from gtts import gTTS
    from langdetect import detect
    if detect(text) != 'ru':
        language = 'en'
    text = text.replace('\n', '')
    my_audio = gTTS(text=text, lang=language, slow=False)
    my_audio.save('text1.mp3')
    return redirect(request.referrer)


@articles_app.route("/audio", endpoint="audio")
def audio():
    import vlc
    import time
    p = vlc.MediaPlayer("file:///text1.mp3")
    p.play()
    time.sleep(10)
    return redirect(request.referrer)
