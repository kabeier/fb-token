from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'authentication.login'
login.login_message = 'You do not have to access to this page.'
login.login_message_category = 'danger'
moment = Moment()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.blog import bp as blog_bp
    app.register_blueprint(blog_bp)

    from .blueprints.authentication import bp as auth_bp
    app.register_blueprint(auth_bp)


    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    with app.app_context():
        from .import context_processors

        from .blueprints.shop import bp as shop_bp
        app.register_blueprint(shop_bp)


    return app