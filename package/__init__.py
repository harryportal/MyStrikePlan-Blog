
from package.database import User,Post
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from .posts.forms import SearchForm



db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Please Login to continue'
login_manager.login_message_category = 'info'
from flask_mail import Mail

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    with app.app_context():
        db.create_all()
    

    from .main.routes import main
    from .users.routes import users
    from .posts.routes import posts
    from .errors.routes import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    @app.context_processor
    def base():
        form = SearchForm()
        return dict(form=form)


    return app
