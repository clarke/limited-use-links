from flask import Blueprint, request, render_template
from flask import flash, redirect, url_for, abort
from app.mod_link.forms import LinkForm
from app.mod_link.forms import LinkDeleteForm
from app.mod_link.models import Link
from flask_login import login_required
from flask_login import current_user
from app import db
from sqlalchemy import desc
from datetime import datetime
import uuid


mod_link = Blueprint('link', __name__, url_prefix='/links')


@mod_link.route('/')
@login_required
def index():
    links = Link.query.order_by(desc('created_at')).all()

    return render_template('links/index.html', links=links)


@mod_link.route('/<int:link_id>')
@login_required
def link(link_id):
    link = Link.query.get(link_id)
    if link is None:
        abort(404)
    form = LinkDeleteForm()
    return render_template('links/show.html', form=form, link=link)


@mod_link.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = LinkForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            link = Link(original_url=form.original_url.data,
                        visits_allowed=form.visits_allowed.data,
                        unique_id=str(uuid.uuid4()),
                        user_id=current_user.id,
                        comment=form.comment.data)
            db.session.add(link)
            db.session.commit()
            return redirect(url_for('link.index'))
        else:
            flash('Form not validated')
    return render_template('links/create.html', form=form)


@mod_link.route('/delete', methods=['POST'])
@login_required
def delete():
    form = LinkDeleteForm()
    link = Link.query.get(form.link_id.data)
    if form.validate_on_submit():
        if link is not None:
            db.session.delete(link)
            db.session.commit()
        return redirect(url_for('link.index'))
    else:
        flash('Failed to delete link')
    return render_template('links/show.html', form=form, link=link)


@mod_link.route('/reset/<id>', methods=['GET'])
@login_required
def reset(id):
    link = Link.query.get(id)
    if link is not None:
        link.visits_used = 0
        link.is_available = True
        link.updated_at = datetime.utcnow()
        db.session.add(link)
        db.session.commit()
    else:
        flash('Failed to reset link')
    return redirect(url_for('link.link', link_id=link.id))
