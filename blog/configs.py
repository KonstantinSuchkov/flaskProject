import os

from dotenv import load_dotenv


load_dotenv()
DEBUG = False
TESTING = False
# SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get("SECRET_KEY")
WTF_CSRF_ENABLED = True
FLASK_ADMIN_SWATCH = 'cosmo'
SOCIAL_AUTH_USER_MODEL = 'blog.models.User'
OAUTHLIB_INSECURE_TRANSPORT = os.environ.get("OAUTHLIB_INSECURE_TRANSPORT")


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "abcdefg123456"
    WTF_CSRF_ENABLED = True


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class TestingConfig(BaseConfig):
    TESTING = True
