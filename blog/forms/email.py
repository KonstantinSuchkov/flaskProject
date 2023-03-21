from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class SendEmail(FlaskForm):

    message = StringField('Message')
    email = StringField('E-mail', [validators.DataRequired(), validators.Email()])

    submit = SubmitField('Send Email')

