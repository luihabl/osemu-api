import os
from flask import Flask, jsonify
from psycopg2 import OperationalError as Psycopg2Error


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev-key'
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route('/hello')
    def hello_again():
        return jsonify({'a': 'b'})

    return app

