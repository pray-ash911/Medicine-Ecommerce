from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize SQLAlchemy instance (but do not pass app here)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize db with app
    db.init_app(app)

    # Import and register blueprints
    from .routes.auth_routes import auth_blueprint
    from .routes.user_routes import user_blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprints, url_prefix='/user')

    # Create database tables within the app context
    with app.app_context():
        db.create_all()

    return app
