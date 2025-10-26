from flask_restful import Resource
from flask import request
from api.models.stanza import LookupStanzeModel
from api.models import db
from api.schemas.stanza import LookupStanzeSchema



many_stanze_schema = LookupStanzeSchema(many=True)
one_stanza_schema = LookupStanzeSchema()



class LookupStanzeResource(Resource):


    def get(self, id=None):

        if id is None:
            stanze = LookupStanzeModel.query.all()
            return many_stanze_schema.dump(stanze), 200
        
        stanza = LookupStanzeModel.query.get(id)

        if stanza:
            return one_stanza_schema.dump(stanza), 200

        return {"message": "Stanza non trovata"}, 404
    

    def post(self):

        data = request.get_json()
        nuova_stanza = LookupStanzeModel(
            NOME_STANZA=data['NOME_STANZA'],
            DIMENSIONE_GRIGLIA_X=data['DIMENSIONE_GRIGLIA_X'],
            DIMENSIONE_GRIGLIA_Y=data['DIMENSIONE_GRIGLIA_Y']
        )

        db.session.add(nuova_stanza)
        db.session.commit()
        
        return one_stanza_schema.dump(nuova_stanza), 201
    

    def delete(self, id):

        stanza = LookupStanzeModel.query.get(id)

        if stanza:
            db.session.delete(stanza)
            db.session.commit()
            return {"message": "Stanza eliminata"}, 204

        return {"message": "Stanza non trovata"}, 404