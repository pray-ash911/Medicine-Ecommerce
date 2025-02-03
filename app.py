from flask import Flask

from config import Config
from app import db
from app.routes.auth_routes import auth_blueprint
from app.routes.user_routes import user_blueprints
from app.routes.medicine_routes import medicine_blueprint



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.config['UPLOAD_FOLDER'] = 'static/images/medicines'


    # Register blueprints with the app
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprints, url_prefix='/user')
    app.register_blueprint(medicine_blueprint, url_prefix='/medicine')


    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)