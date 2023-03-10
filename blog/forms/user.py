from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class UserRegisterForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username')
    email = StringField('E-mail', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Field must be equal to password'),
    ])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField(
        "username",
        [validators.DataRequired()],
    )
    password = PasswordField(
        "Password",
        [validators.DataRequired()],
    )
    submit = SubmitField("Login")