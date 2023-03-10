from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from sqlalchemy.orm import relationship

from blog.models.database import db
from flask_login import UserMixin

from blog.security import flask_bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: db.Column = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(String(120), unique=False, nullable=False, default="", server_default="")
    last_name = db.Column(String(120), unique=False, nullable=False, default="", server_default="")

    username: db.Column = db.Column(db.String(80), unique=True, nullable=False)
    is_staff: db.Column = db.Column(db.Boolean, nullable=False, default=False)
    img: db.Column = db.Column(db.String(80), nullable=False, default='None')
    email: db.Column = db.Column(db.String(255), nullable=False, unique=False, default="", server_default="")
    _password = db.Column(LargeBinary, nullable=True,)

    author = relationship("Author", uselist=False, back_populates="user")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = flask_bcrypt.generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return flask_bcrypt.check_password_hash(self._password, password)

    # def __init__(self, id, username, is_staff, img, email, password):
    #     self.id = id
    #     self.username = username
    #     self.is_staff = is_staff
    #     self.img = img
    #     self.email = email
    #     self.password = password

    def __repr__(self):
        return f"User #{self.id} {self.username!r}>"
