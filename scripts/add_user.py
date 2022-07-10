from app import db
from app.mod_auth.models import User
from getpass import getpass
import hashlib


print("Adding a new administrative user\n")

username = input("Enter username: ")
email = input("Enter email: ")
password = getpass("Password: ")

if username is not None and email is not None and password is not None:
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    u = User(username=username, email=email, password=hashed_password)
    db.session.add(u)
    db.session.commit()
else:
    print("One of the values was empty")
