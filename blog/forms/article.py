from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators, SelectMultipleField


class CreateArticleForm(FlaskForm):
    title = StringField(
        "Title",
        [validators.DataRequired()],
    )
    text = TextAreaField(
        "Body",
        [validators.DataRequired()],
    )
    submit = SubmitField("Publish")
    tags = SelectMultipleField("Tags", coerce=int)
