import os
from flask import Flask, jsonify
from .extensions import db, ma
from .api.models import *

def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev-key'
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # Connect to PostgreSQL database
    db_user = os.environ.get('POSTGRES_USER')
    db_pass = os.environ.get('POSTGRES_PASSWORD')
    db_name = os.environ.get('POSTGRES_DB')
    db_host = os.environ.get('POSTGRES_HOST')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .api import api_bp
    app.register_blueprint(api_bp)

    ma.init_app(app)

    return app

