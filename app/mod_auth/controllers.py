from flask import Blueprint, request, render_template, flash, redirect, url_for
from app import login_manager
from app.mod_auth.forms import LoginForm
from app.mod_auth.models import User
from werkzeug.exceptions import abort
from flask_login import login_required, login_user, logout_user
from urllib.parse import urlparse, urljoin
import hashlib


mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


def get_user(user_form):
    username = user_form.username.data
    password = user_form.password.data
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    user = User.query.filter_by(username=username,
                                password=hashed_password).first()
    return user


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and (ref_url.netloc ==
                                                     test_url.netloc)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form)
        if user is None:
            flash('Login failed', category='error')
            return redirect('/')
        login_user(user)
        flash('Logged in successfully.', category='success')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('index'))
    return render_template('auth/login.html', form=form)


@mod_auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    return redirect(url_for('index'))
