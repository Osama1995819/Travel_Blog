from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField , TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from Flask_app.models import *
from flask_login import login_user , current_user , logout_user , login_required
from flask_wtf.file import FileField , FileAllowed
from Flask_app import mail
from flask_mail import Message
from flask import url_for
import os
from email_validator import validate_email , EmailNotValidError

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
        msg = Message('Congratulations on registering for Travel Blog',
                    sender=os.environ.get('EMAIL_USER'), 
                    recipients=[email.data])
        msg.body = f'''You are now registered on the Travel Blog Forum {url_for('login', _external=True)}'''
        try:
            mail.send(msg)
        except Exception as exc:
            raise ValidationError(f"Please select valid email to register to  {exc}")
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
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg','jfif'])])
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
            
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = MultipleFileField('Add photos for post if you want ', validators=[FileAllowed(['jpg', 'png', 'jpeg','jfif']), Length(max=5)])
    video = MultipleFileField("Add videos for post if you want", validators=[FileAllowed(['mp4','avi','mov','wmv','m4p','webm','3gp','mpg','mpeg','swf','amv','ogv','vob']), Length(max=5)])

    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')