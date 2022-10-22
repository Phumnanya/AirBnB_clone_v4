#!/usr/bin/python3
"""This module runs a flask server"""
import os
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def reload_db(exception):
    storage.close()


@app.errorhandler(404)
def error_404_handler(exception):
    return jsonify({'error': 'Not found'})


app.register_blueprint(app_views, url_prefix='/api/v1')


if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST')
    PORT = os.getenv('HBNB_API_PORT')
    app.run(host=HOST if HOST is not None else '0.0.0.0',
            port=int(PORT) if PORT is not None else 5000,
            threaded=True, debug=True)
