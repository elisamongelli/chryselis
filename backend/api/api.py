from flask import Blueprint
from flask_restful import Api
from api.resources.stanza import LookupStanzeResource



# define the API blueprint
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


# list the API resources and their corresponding routes
api.add_resource(LookupStanzeResource, '/stanze', '/stanze/<string:id>')