from flask import Flask
from config import DevelopmentConfig


def create_app():
    # instantiate app and dev config
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # import blueprints and then register them
    from app.blueprints.user.routes import user_bp
    from app.blueprints.admin.routes import admin_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app


    
    