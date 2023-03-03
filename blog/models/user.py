from sqlalchemy import Column, Integer, String, Boolean
from blog.models.database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id: Column = Column(Integer, primary_key=True)
    username: Column = Column(String(80), unique=True, nullable=False)
    is_staff: Column = Column(Boolean, nullable=False, default=False)
    img: Column = Column(String(80), nullable=False, default='None')
    email: Column = Column(String(255), nullable=False, default="", server_default="")

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"
