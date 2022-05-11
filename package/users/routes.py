from . import users
from flask import render_template, flash, redirect, url_for, request
from .forms import RegistrationForm, LoginForm, Updateform, ResetForm, ResetPassword
from package.database import User
from package import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from .utils import cloudinary_file_upload, reset_token, email_token


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login not Successful, Check login details', 'warning')
            return redirect(url_for('users.login'))
    return render_template('login.html', title='LOG IN', form=form)


@users.route('/login/<token>', methods=['GET', 'POST'])
@login_required
def token_login(token):
    user = current_user.verify_user(token)
    if current_user.confirm:
        flash('Your account has been verified', 'success')
        return redirect(url_for('main.home'))
    if user:
        current_user.confirm = True
        db.session.commit()
        flash('Your Account has now been activated', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('Expired or Invalid Token', 'warning')
    return redirect(url_for('main.home'))


@users.route('/register', methods=['GET', 'POST'])  # THE METHOD ALLOWS USERS TO TAKE AND SEND DATA FROM SERVER
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    lastname=form.lastname.data, firstname=form.firstname.data)
        db.session.add(user)
        db.session.commit()
        email_token(user)
        flash(f"A confirmation link has been sent to your email", 'success')  # displays a message after user registration
        return redirect(url_for('.login'))
    return render_template('register.html', title='Register Now', form=form)


@users.route('/resend_confirmation')
def resend():
    email_token(current_user)
    flash('A confirmation link has been resent to your Inbox', 'success')
    return redirect(url_for('main.home'))


@users.route('/logout')
def logout():
    logout_user()
    flash('Log out Successful', 'success')
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = Updateform()
    if form.validate_on_submit():  # update the account
        if form.image.data:  # add a picture
            print(form.image.data)
            picture = cloudinary_file_upload(form.image.data)
            current_user.image = picture
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated successfully', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':  # fill the form with the current username and email
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = current_user.image
    return render_template('account.html', title='Account', image=image, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_pass():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetForm()
    if form.validate_on_submit():
        email_check = User.query.filter_by(email=form.email.data).first()
        if email_check:
            reset_token(email_check)
            flash('A request link has been sent to your mail', 'success')
            return redirect(url_for('.login'))
        else:
            flash('Email does not exist!, Register to create a new account', 'warning')
            return redirect(url_for('.reset_pass'))
    return render_template('reset_email.html', form=form)


@users.route('/reset_pass/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_user(token)
    if user is None:
        flash('Expired or Invalid Token!', 'info')
        return redirect(url_for('reset_pass'))
    form = ResetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(username=user.username).first()
        hashed_pass = generate_password_hash(form.password.data)
        user.password = hashed_pass
        db.session.commit()
        flash('Your password has been updated! You are now able to login', 'info')
        return redirect(url_for('login'))
    return render_template('resetpassword.html', form=form)
