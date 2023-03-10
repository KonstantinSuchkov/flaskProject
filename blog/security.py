from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect

csrf = CSRFProtect()
flask_bcrypt = Bcrypt()

__all__ = [
    "flask_bcrypt",
    'csrf',
]
