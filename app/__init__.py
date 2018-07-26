from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)

    from .api_1_0 import api as api_1_0
    app.register_blueprint(api_1_0,url_prefix="/api/v1.0")

    return app
