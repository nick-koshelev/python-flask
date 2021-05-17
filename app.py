import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SignUpForm, CreateAlbumForm, EditAlbumForm
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'not so long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./my_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=20)
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()

from models import User, Album


@app.route('/')
def home():
    albums = Album.query.all()
    return render_template('home.html', albums=albums)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/history/')
def history():
    return render_template('history.html')


@app.route('/album/<int:album_id>/')
def album(album_id):
    album = Album.query.filter_by(id=album_id)
    return render_template('album.html', album=album)


@app.route('/create/', methods=['get', 'post'])
def create():
    if not session.get('user'):
        return redirect(url_for('home'))
    form = CreateAlbumForm()
    if form.validate_on_submit():
        title = request.form.get('title')
        description = request.form.get('description')
        date = datetime.datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        new_album = Album(title=title, description=description, date=date)
        db.session.add(new_album)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create.html', form=form)


@app.route('/edit/<int:album_id>/', methods=['get', 'post'])
def edit(album_id):
    if not session.get('user'):
        return redirect(url_for('home'))
    album = Album.query.filter_by(id=album_id).first()
    form = EditAlbumForm(obj=album)
    if form.validate_on_submit():
        title = request.form.get('title')
        description = request.form.get('description')
        date = datetime.datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        album.title = title
        album.description = description
        album.date = date
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form)


@app.route('/delete/<int:album_id>/', methods=['get'])
def delete(album_id):
    if not session.get('user'):
        return redirect(url_for('home'))
    album = Album.query.filter_by(id=album_id).first()
    if album:
        db.session.delete(album)
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/login/', methods=['get', 'post'])
def login():
    if session.get('user'):
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            session['user'] = user.email
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    if session.get('user'):
        session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/sign-up/', methods=['get', 'post'])
def signup():
    if session.get('user'):
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            return redirect(url_for('signup'))

        new_user = User(name=name, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.before_request
def make_session_permanent():
    session.permanent = True
