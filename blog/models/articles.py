from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime

from blog.models.database import db


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(80), unique=True, nullable=False)
    text = db.Column(db.Text, default="", server_default="")
    dt_created = db.Column(DateTime, default=datetime.utcnow, server_default=func.now())
    dt_updated = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="articles")


    def __repr__(self):
        return f'<User #{self.id} {self.text!r}>'
