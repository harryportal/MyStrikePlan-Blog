import os
from flask import url_for
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, render_template
from package.database import User
from .edit_username import edit_google_username
from package import db
from flask_login import login_user
from flask import redirect


gauth = Blueprint('gauth', __name__)
oauth = OAuth()

google = oauth.register(
    name='google',
    client_id= '54930374214-398p4r3fo8dqm03hu9j7etafhj0ijrfb.apps.googleusercontent.com',
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

# Google login route
@gauth.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('gauth.google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@gauth.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    user = google.get('userinfo').json()

    # check if user is in database, else add user and generate token
    check_user = User.query.filter_by(email=user['email']).first()
    if check_user:
        login_user(check_user)
        return redirect(url_for('main.home'))
    else:
        new_name = edit_google_username(user['given_name'])
        print(f"\n{user}\n")
        new_user = User(username=new_name, email=user['email'])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main.home'))