from flask import Blueprint
from flask_restful import Api
from api.resources.stanza import LookupStanzeResource
from api.resources.stato import LookupStatiResource
from api.resources.programma import LookupProgrammiResource



# define the API blueprint
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


# list the API resources and their corresponding routes
api.add_resource(LookupStanzeResource, '/stanze', '/stanze/<string:id>')
api.add_resource(LookupStatiResource, '/stati', '/stati/<string:id>')
api.add_resource(LookupProgrammiResource, '/programmi', '/programmi/<string:id>')