from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dataweeb.models import User, Anime, Manga

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class AddManga(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    premiered = StringField('Date Premiered',validators=[DataRequired()])
    status = RadioField('Status',choices = [('Ongoing','Ongoing'),('Finished','Finished')],validators=[DataRequired()])
    rating = IntegerField('Rating',validators=[DataRequired()])
    author = StringField('Author')
    submit = SubmitField('Add')

    def validate_title(self, title):
        user = Manga.query.filter_by(title=title.data).first()
        if user:
            raise ValidationError('That title is taken. Please choose a different one.')



class AddAnime(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    premiered = StringField('Date Premiered',validators=[DataRequired()])
    anime_type = RadioField('Anime Type',choices = [('TV','TV'),('OVA','OVA'),('Movie','Movie'),('Special','Special'),('ONA','ONA')],validators=[DataRequired()])
    episodes = IntegerField('Number of Episodes',validators=[DataRequired()])
    rating = IntegerField('Rating',validators=[DataRequired()])
    studio = StringField('Studio')
    submit = SubmitField('Add')

    def validate_title(self, title):
        user = Anime.query.filter_by(title=title.data).first()
        if user:
            raise ValidationError('That title is taken. Please choose a different one.')
    

class UpdateManga(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    premiered = StringField('Date Premiered',validators=[DataRequired()])
    status = RadioField('Status',choices = [('Ongoing','Ongoing'),('Finished','Finished')],validators=[DataRequired()])
    rating = IntegerField('Rating',validators=[DataRequired()])
    author = StringField('Author')
    submit = SubmitField('Update')


class UpdateAnime(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    premiered = StringField('Date Premiered',validators=[DataRequired()])
    anime_type = RadioField('Anime Type',choices = [('TV','TV'),('OVA','OVA'),('Movie','Movie'),('Special','Special'),('ONA','ONA')],validators=[DataRequired()])
    episodes = IntegerField('Number of Episodes',validators=[DataRequired()])
    rating = IntegerField('Rating',validators=[DataRequired()])
    studio = StringField('Studio')
    submit = SubmitField('Update')


