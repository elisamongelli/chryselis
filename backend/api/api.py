from flask import Blueprint
from flask_restful import Api
from api.resources.stanza import LookupStanzeResource
from api.resources.stato import LookupStatiResource
from api.resources.programma import LookupProgrammiResource
from api.resources.pianta_programma import LookupPianteProgrammiResource
from api.resources.pianta import ActPianteResource, ActFotoPianteResource
from api.resources.pianta_storico import ActPianteStoricoResource



# define the API blueprint
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


# list the API resources and their corresponding routes - lookup
api.add_resource(LookupStanzeResource, '/lookup/stanze', '/lookup/stanze/<string:id>')
api.add_resource(LookupStatiResource, '/lookup/stati', '/lookup/stati/<string:id>')
api.add_resource(LookupProgrammiResource, '/lookup/programmi', '/lookup/programmi/<string:id>')
api.add_resource(LookupPianteProgrammiResource, '/lookup/pianteProgrammi', '/lookup/pianteProgrammi/piante/<string:plantID>/programmi/<string:scheduleID>', '/lookup/pianteProgrammi/piante/<string:plantID>', '/lookup/pianteProgrammi/programmi/<string:scheduleID>')

# list the API resources and their corresponding routes - anagrafica
api.add_resource(ActPianteResource, '/anagrafica/piante', '/anagrafica/piante/<string:id>')
api.add_resource(ActFotoPianteResource, '/anagrafica/fotoPiante', '/anagrafica/fotoPiante/<string:id>')
api.add_resource(ActPianteStoricoResource, '/anagrafica/storicoPiante', '/anagrafica/storicoPiante/<string:plantID>')