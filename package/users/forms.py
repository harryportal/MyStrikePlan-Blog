from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from package.database import User
from flask_login import current_user
from .utils import  school_list


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    school = SelectField('School', choices=school_list)
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already in use!')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class Updateform(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image = FileField('Upload Picture', validators=[FileAllowed(['png', 'jpg','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and username.data != current_user.username:
            raise ValidationError('Username already in use!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and email.data != current_user.email:
            raise ValidationError('Email already in use!')


class ResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data)
        if user is None:
            raise ValidationError('There is no account with this email')

class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

