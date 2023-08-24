from flask import Flask
from setting import DevelopmentConfig
from exts import db, migrate
from apps.user import *
from apps.room import *


def createApp():
    app = Flask(
        __name__, template_folder='../templates/', static_folder='../static/'
    )
    app.config.from_object(DevelopmentConfig)

    app.register_blueprint(user_bp)
    app.register_blueprint(room_bp)

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    return app
