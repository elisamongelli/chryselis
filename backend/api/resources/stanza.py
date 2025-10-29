from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from api.models.stanza import LookupStanzeModel
from api.models import db
from api.schemas.stanza import LookupStanzeSchema



many_stanze_schema = LookupStanzeSchema(many=True)
one_stanza_schema = LookupStanzeSchema()



class LookupStanzeResource(Resource):


    def get(self, id=None):

        # if ID does not exists, get all rooms
        if id is None:
            try:

                page = request.args.get('page', default=1, type=int)
                limit = request.args.get('limit', default=25, type=int)

                if page < 1:
                    return {"message": "La pagina deve essere un valore positivo"}, 400
                if limit < 1 or limit > 100:
                    return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
                
                query = LookupStanzeModel.query.order_by(LookupStanzeModel.NOME_STANZA)

                pagination = query.paginate(page=page, per_page=limit, error_out=False)
                stanze = pagination.items
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "stanze": many_stanze_schema.dump(stanze),
                    "count": len(stanze),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero delle stanze"}, 500
        
        # else if ID is not null, get the one room corresponding to the ID
        try:
            stanza = LookupStanzeModel.query.get(id)
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero della stanza"}, 500

        # if the room has been retrieve successfully from the DB
        if stanza:
            return one_stanza_schema.dump(stanza), 200

        # else return 404 error, room not found
        return {"message": "Stanza non trovata"}, 404
    


    def post(self):

        # get JSON for REST API request body
        data = request.get_json()

        # create a new room with request body's data
        nuova_stanza = LookupStanzeModel(
            NOME_STANZA=data['NOME_STANZA'],
            DIMENSIONE_GRIGLIA_X=data['DIMENSIONE_GRIGLIA_X'],
            DIMENSIONE_GRIGLIA_Y=data['DIMENSIONE_GRIGLIA_Y']
        )

        try:
            db.session.add(nuova_stanza)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione della stanza"}, 500

        return one_stanza_schema.dump(nuova_stanza), 201



    def patch(self, id):

        # get the one room from the DB with the corresponding ID
        stanza = LookupStanzeModel.query.get(id)

        # if the ID is not found in the DB, return 404 error, room not found
        if not stanza:
            return {"message": "Stanza non trovata"}, 404
        
        # get JSON for REST API request body
        # silent=True does not throw any exception if request body is empty (or not in a JSON format)
        data = request.get_json(silent=True) or {}

        try:
            # load method returnes a dictionary with all valid fields
            # if a field has a wrong data type or does not exist on DB table, it throws a ValidationError
            # partial=True allows to get a JSON request with only a subset of fields
            valid_data = one_stanza_schema.load(data, partial=True)
        except ValidationError:
            return {"message": "I valori inseriti per la modifica della stanza non sono validi"}, 400
        
        # sets the allowed fields and updates only them on DB
        allowed_fields = ['NOME_STANZA', 'DIMENSIONE_GRIGLIA_X', 'DIMENSIONE_GRIGLIA_Y']
        for key, value in valid_data.items():
            if key in allowed_fields:
                setattr(stanza, key, value)
        
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante l'aggiornamento della stanza"}, 500

        return one_stanza_schema.dump(stanza), 200
    


    def delete(self, id):

        # get the one room from the DB with the corresponding ID
        stanza = LookupStanzeModel.query.get(id)

        # if the ID is not found in the DB, return 404 error, room not found
        if not stanza:
            return {"message": "Stanza non trovata"}, 404

        # else delete the room from the DB
        try:
            db.session.delete(stanza)
            db.session.commit()
            return {"message": "Stanza eliminata"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione della stanza"}, 500