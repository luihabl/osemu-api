import os
from flask import Flask, jsonify
from .extensions import db, migrate
from .api.models import *
from .config import DevelopmentConfig

def create_app(config=DevelopmentConfig, init_db=True):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .api import api_bp
    app.register_blueprint(api_bp)

    return app

