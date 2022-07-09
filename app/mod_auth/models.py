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


class Link(Base):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(120), unique=True, nullable=False)
    original_url = db.Column(db.Text, nullable=False)
    visits_used = db.Column(db.Integer, nullable=False, default=0)
    visits_allowed = db.Column(db.Integer, nullable=False, default=1)
    clicks = db.relationship('Click', backref='links', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def is_available(self):
        if self.visits_used < self.visits_allowed:
            return True
        else:
            return False


class Click(Base):
    __tablename__ = 'clicks'

    ip_address = db.Column(db.String(80), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
