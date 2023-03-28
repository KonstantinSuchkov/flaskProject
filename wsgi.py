from flask import redirect, url_for
# from flask_combo_jsonapi import Api
from flask_dance.contrib.github import github
from blog.app import create_app
from blog.models.database import db


# api = Api()
app = create_app()

# login_manager.init_app(app)

@app.cli.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'Amelia'> <User #3 'Varvara'>
    """
    from blog.models import User
    admin = User(username="admin", is_staff=True)
    amelia = User(username="Amelia")
    varvara = User(username='Varvara', img='varvarka.png')
    db.session.add(admin)
    db.session.add(amelia)
    db.session.add(varvara)
    db.session.commit()
    print("done! created users:", admin, amelia, varvara)


@app.cli.command("create-articles")
def create_articles():
    """
    Run in your terminal:
    flask create-articles
    > done! created articles: <>
    """
    from blog.models import Article
    admin = Article(text='Покоряем flask в 36', author='admin')
    amelia = Article(text='Интриги и скандалы', author='Amelia')
    varvara = Article(text='Два месяца в детском садике', author='Varvara')
    db.session.add(admin)
    db.session.add(amelia)
    db.session.add(varvara)
    db.session.commit()
    print("done! created articles:", admin, amelia, varvara)


@app.cli.command("create-tags")
def create_tags():
    """
    Run in your terminal:
    ➜ flask create-tags
    """
    from blog.models import Tag
    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()
    print("created tags")


@app.route("/login/github")
def login_github():
    if not github.authorized:
        return redirect(url_for("github.login"))
    res = github.get("/user")
    username = res.json()["login"]
    return f"You are @{username} on GitHub"


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
    )


