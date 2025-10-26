from flask import Flask
from api.models import db
from api.api import api_blueprint



def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    db.init_app(app)
    app.register_blueprint(api_blueprint, url_prefix='/chryselis')
    return app