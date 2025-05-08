from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from books_app.models import Audience, Book, Author, Genre, User
from books_app.extensions import app, db, bcrypt

class BookForm(FlaskForm):
    """Form to create a book."""
    title = StringField('Book Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    publish_date = DateField('Date Published')
    author = QuerySelectField('Author',
        query_factory=lambda: Author.query, allow_blank=False)
    audience = SelectField('Audience', choices=Audience.choices())
    genres = QuerySelectMultipleField('Genres',
        query_factory=lambda: Genre.query)
    submit = SubmitField('Submit')

class AuthorForm(FlaskForm):
    """Form to create an author."""
    # TODO: Fill out the fields in this class for:
    # - the author's name
    # - the author's biography (hint: use a TextAreaField)
    # - a submit button
    # STRETCH CHALLENGE: Add more fields here as well as in `models.py` to
    # collect more information about the author, such as their birth date,
    # country, etc.
    pass

class GenreForm(FlaskForm):
    """Form to create a genre."""
    # TODO: Fill out the fields in this class for:
    # - the genre's name (e.g. fiction, non-fiction, etc)
    # - a submit button
    pass

class SignUpForm(FlaskForm):
    """Form for user signup."""
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')