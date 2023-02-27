from sqlalchemy import Column, Integer, String
from blog.models.database import db


class Article(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(80), unique=True, nullable=False)
    author = Column(String(80), nullable=False)

    def __repr__(self):
        return f'<User #{self.id} {self.text!r}>'
