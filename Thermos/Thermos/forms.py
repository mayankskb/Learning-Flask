from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Regexp, EqualTo, Email

from models import User

class BookmarkForm(Form):
    url = URLField('The URL for your bookmark : ')
    description = StringField('Add an optional description')

    def validate(self):

        if not (self.url.data.startswith("http://") or self.url.data.startswith("https://")):
            self.url.data = "https://" + self.url.data

        if not Form.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.url.data

        return True


class LoginForm(Form):
    username = StringField("Your Username:", validators = [DataRequired()])
    password = PasswordField("Password:", validators = [DataRequired()])
    remember_me = BooleanField('Keep me Logged in')
    submit = SubmitField('Log In')


class SignUp(Form):
    username = StringField('Username',
                        validators = [
                        DataRequired(), Length(3,80),
                        Regexp('^[A-Za-z0-9_]{3,}$',
                        message = 'Username consists of numbers, letters,'
                                   'and underscores.')])
    password = PasswordField('Password',
                              validators = [
                              DataRequired(),
                              EqualTo('password2', message = 'Passwords must match')])
    password2 = PasswordField('Confirm Password', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Length(1,120), Email()])

    def validate_email(self,email_field):
        if User.query.filter_by(email = email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self,username_field):
        if User.query.filter_by(username = username_field.data).first():
            raise ValidationError('This username is already taken.')
