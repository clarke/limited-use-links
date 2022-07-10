from flask import Blueprint, request, render_template
from flask import flash, redirect, url_for, abort
from app.mod_file.forms import FileForm
from flask_login import login_required
from flask_login import current_user
from app import db
import uuid
from werkzeug.utils import secure_filename
from app.mod_link.models import Link
import os
import app
from urllib.parse import urlparse
import zipfile


mod_file = Blueprint('file', __name__, url_prefix='/files')


@mod_file.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = FileForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            zipfile_name = f'{str(uuid.uuid4())}.zip'
            with zipfile.ZipFile(zipfile_name, mode='w') as archive:
                for f in form.photo.data:
                    filename = secure_filename(f.filename)

                    f.save(filename)
                    archive.write(filename)
                    os.remove(filename)

                os.rename(zipfile_name, os.path.join(
                    app.app.instance_path, 'photos', zipfile_name
                ))

            parsed_url = urlparse(request.base_url)
            hostname = f'{parsed_url.scheme}://{parsed_url.hostname}'
            if parsed_url.port not in [80, 443]:
                hostname = f'{hostname}:{parsed_url.port}'
            file_url = f'{hostname}/instance/photos/{zipfile_name}'

            link = Link(original_url=file_url,
                        visits_allowed=form.visits_allowed.data,
                        unique_id=str(uuid.uuid4()),
                        user_id=current_user.id,
                        comment=form.comment.data)
            db.session.add(link)
            db.session.commit()
            return redirect(url_for('link.link', link_id=link.id))
        else:
            flash('Form not validated')
    return render_template('files/upload.html', form=form)
