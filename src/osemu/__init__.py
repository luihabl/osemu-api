import os
from flask import Flask, jsonify
from .extensions import db, migrate, login_manager, admin, scheduler
from .api.models import *
from .config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
from .scheduled.jobs import *

def create_app(config=Config, init_db=True):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.url_map.strict_slashes = False

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)
    
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    scheduler.init_app(app)

    from osemu.admin.views import register_admin_views
    register_admin_views()

    from .api import api_bp
    app.register_blueprint(api_bp)

    from osemu.api.views.docs import swaggerui_bp
    app.register_blueprint(swaggerui_bp)

    from osemu.docs.specs import register_views_on_spec
    with app.app_context():
        register_views_on_spec()
    
    if app.config.get('START_SCHEDULED_JOBS'):
        
        if scheduler.running:
            return
        
        print('Starting jobs')
        scheduler.start()
    
    return app

