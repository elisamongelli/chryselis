from flask import Flask
from api.models import db
from api.api import api_blueprint



# methods for creating and configuring the Flask app
def create_app(config_filename):
    app = Flask(__name__, static_folder='../../assets/html', static_url_path='')
    app.config.from_object(config_filename)
    db.init_app(app)
    # /chryselis is the base path for all API endpoints
    app.register_blueprint(api_blueprint, url_prefix='/chryselis')
    return app