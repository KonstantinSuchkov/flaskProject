from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from blog.models.database import db


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="author")
    articles = relationship("Article", back_populates="author")

    def __init__(self, id, username, is_staff, img, email, password):
        self.id = id
        self.username = username
        self.is_staff = is_staff
        self.img = img
        self.email = email
        self.password = password

    def __str__(self):
        return self.user.username
