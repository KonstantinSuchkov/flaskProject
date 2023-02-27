from blog.app import create_app, db
from blog.auth import login_manager

app = create_app()
app.secret_key = b'amelia'
login_manager.init_app(app)


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


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
    )
