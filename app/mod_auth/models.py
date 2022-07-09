from app import db
import hashlib
from datetime import datetime


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)


class User(Base):
    __tablename__ = 'users'

    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    links = db.relationship('Link', backref='users', lazy=True)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)

    def hashed_password(self):
        return hashlib.sha512(self.password.encode('utf-8')).hexdigest()

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
