from . import main
from flask import render_template, request
from package.database import Post



@main.route('/')
def home():
    return render_template('about.html')

@main.route('/home')
def posts():
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page, per_page=10)
    current_post = post.items
    return render_template('home.html', post=current_post, posts=post)

@main.route('/about')
def about():
    return render_template('about.html', title='ABOUT')














