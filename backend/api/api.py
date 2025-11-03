from flask import Blueprint
from flask_restful import Api
from api.resources.stanza import LookupStanzeResource
from api.resources.stato import LookupStatiResource
from api.resources.programma import LookupProgrammiResource
from api.resources.pianta_programma import LookupPianteProgrammiResource
from api.resources.pianta import ActPianteResource



# define the API blueprint
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


# list the API resources and their corresponding routes - lookup
api.add_resource(LookupStanzeResource, '/lookup/stanze', '/lookup/stanze/<string:id>')
api.add_resource(LookupStatiResource, '/lookup/stati', '/lookup/stati/<string:id>')
api.add_resource(LookupProgrammiResource, '/lookup/programmi', '/lookup/programmi/<string:id>')
api.add_resource(LookupPianteProgrammiResource, '/lookup/pianteProgrammi', '/lookup/pianteProgrammi/piante/<string:idPianta>/programmi/<string:idProgramma>', '/lookup/pianteProgrammi/piante/<string:idPianta>', '/lookup/pianteProgrammi/programmi/<string:idProgramma>')

# list the API resources and their corresponding routes - anagrafica
api.add_resource(ActPianteResource, '/anagrafica/piante', '/anagrafica/piante/<string:id>')