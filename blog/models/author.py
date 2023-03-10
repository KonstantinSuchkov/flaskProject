from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from blog.models.database import db


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="author")
    articles = relationship("Article", back_populates="author")
