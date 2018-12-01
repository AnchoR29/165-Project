from dataweeb import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default ='default.png')
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable = False)
    desc = db.Column(db.String(200), unique=True, nullable = False)
    a_genre = db.relationship('Anime', backref='Genre', lazy = True)
    m_genre = db.relationship('Manga', backref='Genre', lazy = True)

    def __repr__(self):
        return f"Genre('{self.name}')"

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable = False)
    premiered = db.Column(db.String(10),  nullable = False)
    anime_type = db.Column(db.String(10), nullable = False)
    episodes = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    studio = db.Column(db.String(50), db.ForeignKey('studio.name'), nullable=True)
    genre = db.Column(db.String(50), db.ForeignKey('genre.name'), nullable=True)

    
    def __repr__(self):
        return f"Anime('{self.title}','{self.premiered}','{self.anime_type}','{self.episodes}')"

class Manga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable = False)
    premiered = db.Column(db.String(10),  nullable = False)
    status = db.Column(db.String(20), nullable = False)
    rating = db.Column(db.Integer)
    author = db.Column(db.Integer, db.ForeignKey('author.name'), nullable=True)
    genre = db.Column(db.String(50), db.ForeignKey('genre.name'), nullable=True)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable = False)
    writer = db.relationship('Manga', backref='written', lazy = True)

    def __repr__(self):
        return f"Author('{self.name}')"

class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable = False)
    produced = db.relationship('Anime', backref='producer', lazy = True)
    def __repr__(self):
        return f"Studio('{self.name}')"

