from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash
from blog.forms.user import UserRegisterForm
from blog.models import User, db

users_app = Blueprint('user_app', __name__, url_prefix='/users', static_folder='../static')


@users_app.route('register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.profile', pk=current_user.id))

    form = UserRegisterForm(request.form)
    errors = []
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append('email already exists')
            return render_template('users/register.html', form=form)

        _user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=generate_password_hash(form.password.data),
        )

        db.session.add(_user)
        db.session.commit()

        login_user(_user)

    return render_template(
        'users/register.html',
        form=form,
        errors=errors,
    )


@users_app.route('/')
def user_list():
    users = User.query.all()
    return render_template(
        'users/list.html',
        users=users,
    )


@users_app.route('/<int:pk>')
@login_required
def details(pk: int):
    selected_user = User.query.filter_by(id=pk).one_or_none()
    if not selected_user:
        raise NotFound(f"User #{pk} doesn't exist!")

    return render_template(
        'users/details.html',
        user=selected_user,
    )
