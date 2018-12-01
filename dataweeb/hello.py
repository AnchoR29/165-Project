from flask import Flask,render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '42eb82acb1aa84c3323ca02625d421a0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default ='default.jpg')
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable = False)
    premiered = db.Column(db.String(10),  nullable = False)
    anime_type = db.Column(db.String(10), nullable = False)
    episodes = db.Column(db.Integer)

    
    def __repr__(self):
        return f"Anime('{self.title}','{self.premiered}','{self.anime_type}','{self.episodes}')"

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable = False)

    def __repr__(self):
        return f"Author('{self.name}')"

class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable = False)

    def __repr__(self):
        return f"Studio('{self.name}')"

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable = False)
    desc = db.Column(db.String(200), unique=True, nullable = False)

    def __repr__(self):
        return f"Studio('{self.name}')"
@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', title='Index')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('anime'))
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
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

@app.route("/anime")
def anime():
    return render_template('anime.html')

@app.route("/manga")
def manga():
    return render_template('manga.html')    

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)