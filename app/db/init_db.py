from app import db


db.create_all()
db.session.commit()
