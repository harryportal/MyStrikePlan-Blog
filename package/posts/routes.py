from . import posts

from flask import render_template, flash, redirect, url_for, request
from .forms import PostForm, UpdatePost, SearchForm
from package.database import User, Post
from package import db, create_app
from flask_login import current_user, login_required
from sqlalchemy import or_

app = create_app()


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        newpost = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(newpost)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.posts'))
    return render_template('post.html', title='New Post', form=form)


@posts.route('/post/<int:post_id>')
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = UpdatePost()
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.author.id:
        return render_template('500.html')
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('.view_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_post.html', form=form, title='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('.my_post'))


@posts.route('/mypost')
@login_required
def my_post():
    page = request.args.get('page', 1, type=int)
    post = Post.query.filter_by(user_id=current_user.id) \
        .order_by(Post.date_posted.desc()).paginate(page, per_page=5)
    return render_template('mypost.html', post=post)


@posts.route('/user_post/<user>')
@login_required
def user_post(user):
    page = request.args.get('page', 1, type=int)
    author = User.query.filter_by(username=user).first_or_404()
    author_post = Post.query.filter_by(user_id=author.id) \
        .order_by(Post.date_posted.desc()).paginate(page, per_page=5)
    return render_template('userpost.html', post=author_post, user=author)


@posts.route('/search', methods=['GET','POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        searched_post = form.searched.data
        post_query = (Post.query.filter(or_(Post.content.like('%' + searched_post + '%'),
                               Post.title.like('%' + searched_post + '%'))))
        post = post_query.all()
        page = request.args.get('page', 1, type=int)
        posts_perpage = post_query.paginate(page, per_page=10)
        return render_template('search.html', form=form, searched=searched_post, post=post, posts=
        posts_perpage)
    else:
        flash('Please input a string!', 'warning')
        return redirect(url_for('main.home'))
