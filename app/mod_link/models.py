from app import db
from datetime import datetime
import pytz


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)


class Link(Base):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(120), unique=True, nullable=False)
    original_url = db.Column(db.Text, nullable=False)
    visits_used = db.Column(db.Integer, nullable=False, default=0)
    visits_allowed = db.Column(db.Integer, nullable=False, default=1)
    clicks = db.relationship('Click', backref='links', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    comment = db.Column(db.Text)


class Click(Base):
    __tablename__ = 'clicks'

    ip_address = db.Column(db.String(80), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def local_timestamp(self):
        utc = pytz.utc
        central = pytz.timezone('US/Central')
        # Sat Jul 9 20:07:01 2022
        time_format = '%A %B %d, %Y %I:%M:%S %p'
        return utc.localize(self.created_at).astimezone(central).strftime(time_format)
