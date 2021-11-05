from flask import render_template, flash, request, redirect, url_for
from web_app import app, login
from web_app.forms import LoginForm
from web_app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from flask_autoindex import AutoIndex
import os


idx = AutoIndex(app,
                browse_root=app.config['UPLOAD_FOLDER'],
                add_url_rules=True)


@login.user_loader
def load_user(id):
    u = app.config['USERS']
    return User(u['id'], u['name'], u['password'], u['active'])


@app.route('/')
@login_required
def root_page():
    return redirect(url_for('index'))


@app.route('/home')
def index():
    posts = [
        {
            'key': 'Home',
            'body': 'Home page'
        },
        {
            'key': 'Files',
            'body': 'Show uploaded files'
        },
        {
            'key': 'Upload',
            'body': 'Upload file'
        },
        {
            'key': 'Login',
            'body': 'Login to app'
        },
        {
            'key': 'Logout',
            'body': 'Logout from app'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=current_user,
                           posts=posts)


@app.route('/check')
@login_required
def check():
    if current_user.is_authenticated:
        return render_template('check.html',
                               title='Check user',
                               user=current_user)


@app.route('/signin', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    u = app.config['USERS']
    form = LoginForm()
    if form.validate_on_submit():
        user_ = User(u['id'], u['name'], u['password'], u['active'])
        if user_ is not None:
            if user_.name == form.username.data \
               and user_.password == form.password.data:
                login_user(user_)
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password')
                return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signout')
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('login'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # check if the post request has the file part
        if file and not allowed_file(file.filename):
            flash('Incorrect file type')
            return redirect(url_for('index'))
        # empty file without a filename.
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File was uploaded')
            return redirect(url_for('index'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/files')
@app.route('/files/<path:path>')
@login_required
def files_list(path='.'):
    return idx.render_autoindex(path)
