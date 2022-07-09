from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import redirect
from flask import url_for
from flask_login import LoginManager
from flask_login import current_user
from flask import render_template


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from app.mod_auth.controllers import mod_auth as auth_module # noqa E402


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


app.register_blueprint(auth_module)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('auth.login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
