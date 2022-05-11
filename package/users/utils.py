import os
from package import mail, create_app
from flask_mail import Message
from flask import render_template
from cloudinary.uploader import upload
from cloudinary import config

config(
    cloud_name="mystrikeplans",
    api_key=os.environ.get('api_key'),
    api_secret=os.environ.get('api_secret'),
    secure=True
)
app = create_app()


def cloudinary_file_upload(image):
    data = upload(image)
    return data.get('url')


def reset_token(user):
    token = user.get_token()
    msg = Message('Password Reset Request', sender='My Strike Plans', recipients=[user.email])
    msg.html = render_template('mail/passwordreset.html', user=user, token=token)
    mail.send(msg)


def email_token(user):
    token = user.get_token()
    msg = Message('Confirm your Email', sender='My Strike Plans', recipients=[user.email])
    msg.html = render_template('mail/mail.html', user=user, token=token)
    mail.send(msg)
