from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import redirect
from flask import url_for
from flask_login import LoginManager
from flask_login import current_user
from flask import render_template
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from app.mod_auth.controllers import mod_auth as auth_module # noqa E402
from app.mod_link.controllers import mod_link as link_module # noqa E402
from app.mod_link.models import Link # noqa E402


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


app.register_blueprint(auth_module)
app.register_blueprint(link_module)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('auth.login'))


@app.route('/r/<unique_id>')
def deliver_link(unique_id):
    link = Link.query.filter_by(unique_id=unique_id).first()

    if link and link.is_available:
        current_visits = link.visits_used + 1
        if current_visits >= link.visits_allowed:
            link.is_available = False
        link.visits_used = current_visits
        link.updated_at = datetime.utcnow()
        db.session.add(link)
        db.session.commit()
        return(f"We found: {link.original_url}")
    else:
        return("Did not find it")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
