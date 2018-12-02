import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from dataweeb import app, db, bcrypt
from dataweeb.forms import *
from dataweeb.models import User, Anime, Manga, Episodes
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/index")
def index():
    anime = Anime.query.all()
    return render_template('index.html', title='Index',anime=anime)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now Log In', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/ppics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='ppics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/anime")
def anime():
    anime = Anime.query.all()
    return render_template('anime.html', anime=anime)

@app.route("/anime/new", methods=['GET', 'POST'])
@login_required
def new_anime():
    form = AddAnime()
    if form.validate_on_submit():
        post = Anime(title=form.title.data, premiered=form.premiered.data, anime_type = form.anime_type.data, rating = form.rating.data, studio = form.studio.data, genre = form.genre.data )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('anime'))
    return render_template('addanime.html', title='New Anime',
                           form=form, legend='New Post')

@app.route("/anime/<int:anime_id>/update", methods=['GET', 'POST'])
@login_required
def update_anime(anime_id):
    post = Anime.query.get_or_404(anime_id)
    form = UpdateAnime()
    if form.validate_on_submit():
        post.title = form.title.data
        post.premiered=form.premiered.data
        post.anime_type = form.anime_type.data
        post.rating = form.rating.data
        post.studio = form.studio.data
        post.genre = form.genre.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('anime'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.premiered.data = post.premiered
        form.anime_type.data = post.anime_type
        form.rating.data = post.rating
        form.studio.data = post.studio
        form.genre.data = post.genre
    return render_template('addanime.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/anime/<int:anime_id>/delete", methods=['POST'])
@login_required
def delete_anime(anime_id):
    post = Anime.query.get_or_404(anime_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('anime'))


#################################EPISODES##########################

@app.route("/anime/<int:anime_id>")
def viewepisode(anime_id):
    anime = Anime.query.get_or_404(anime_id)
    episodes = Episodes.query.filter_by(anime_id = anime_id).order_by(Episodes.no)
    return render_template('episodes.html', anime=anime,episodes = episodes)

@app.route("/anime/<int:anime_id>/new", methods=['GET', 'POST'])
@login_required
def new_episode(anime_id):
    form = AddEpisode()
    if form.validate_on_submit():
        post = Episodes(title=form.title.data, premiered=form.premiered.data, no = form.no.data,anime_id = anime_id )
        db.session.add(post)
        db.session.commit()
        flash('Your episode has been created!', 'success')
        return redirect(url_for('viewepisode', anime_id=post.anime_id))
    return render_template('addepisode.html', title='New Anime',
                           form=form, legend='New Post')   

@app.route("/anime/<int:anime_id>/update/<int:episode_id>", methods=['GET', 'POST'])
@login_required
def update_episode(anime_id,episode_id):
    post = Episodes.query.get_or_404(episode_id)
    form = AddEpisode()
    if form.validate_on_submit():
        post.title = form.title.data
        post.premiered=form.premiered.data
        post.no = form.no.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('viewepisode', anime_id=post.anime_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.premiered.data = post.premiered
        form.no.data = post.no
    return render_template('addepisode.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/anime/<int:anime_id>/delete/<int:episode_id>", methods=['POST'])
@login_required
def delete_episode(anime_id,episode_id):
    post = Episodes.query.get_or_404(episode_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('viewepisode', anime_id=post.anime_id))


@app.route("/manga")
def manga():
    manga = Manga.query.all()
    return render_template('manga.html', manga=manga)  

@app.route("/manga/new", methods=['GET', 'POST'])
@login_required
def new_manga():
    form = AddManga()
    if form.validate_on_submit():
        post = Manga(title=form.title.data, premiered=form.premiered.data, status = form.status.data, rating = form.rating.data, author = form.author.data, genre = form.genre.data )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('manga'))
    return render_template('addmanga.html', title='New Manga',
                           form=form, legend='New Post')

@app.route("/manga/<int:manga_id>/update", methods=['GET', 'POST'])
@login_required
def update_manga(manga_id):
    post = Manga.query.get_or_404(manga_id)
    form = UpdateManga()
    if form.validate_on_submit():
        post.title = form.title.data
        post.premiered=form.premiered.data
        post.status = form.status.data
        post.rating = form.rating.data
        post.author = form.author.data
        post.genre = form.genre.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('manga'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.premiered.data = post.premiered
        form.status.data = post.status
        form.rating.data = post.rating
        form.author.data = post.author
        form.genre.data = post.genre
    return render_template('addmanga.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/manga/<int:manga_id>/delete", methods=['POST'])
@login_required
def delete_manga(manga_id):
    post = Manga.query.get_or_404(manga_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('manga'))

@app.route("/about")
def about():
    return render_template('about.html')