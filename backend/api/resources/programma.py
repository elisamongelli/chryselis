from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from api.models.programma import LookupProgrammiModel
from api.models import db
from api.schemas.programma import LookupProgrammiSchema



many_programmi_schema = LookupProgrammiSchema(many=True)
one_programma_schema = LookupProgrammiSchema()



class LookupProgrammiResource(Resource):


    def get(self, id=None):

        # if ID does not exists, get all schedules
        if id is None:
            try:

                page = request.args.get('page', default=1, type=int)
                limit = request.args.get('limit', default=25, type=int)

                if page < 1:
                    return {"message": "La pagina deve essere un valore positivo"}, 400
                if limit < 1 or limit > 100:
                    return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
                
                query = LookupProgrammiModel.query.order_by(LookupProgrammiModel.VALORE_SEQUENZA_TEMPORALE_PROGRAMMA)

                pagination = query.paginate(page=page, per_page=limit, error_out=False)
                programmi = pagination.items
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "programmi": many_programmi_schema.dump(programmi),
                    "count": len(programmi),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero dei programmi"}, 500
        
        # else if ID is not null, get the one schedule corresponding to the ID
        try:
            programma = LookupProgrammiModel.query.get(id)
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero del programma"}, 500

        # if the schedule has been retrieve successfully from the DB
        if programma:
            return one_programma_schema.dump(programma), 200

        # else return 404 error, schedule not found
        return {"message": "Programma non trovato"}, 404
    


    def post(self):

        # get JSON for REST API request body
        data = request.get_json()

        # create a new schedule with request body's data
        nuovo_programma = LookupProgrammiModel(
            VALORE_SEQUENZA_TEMPORALE_PROGRAMMA=data['VALORE_SEQUENZA_TEMPORALE_PROGRAMMA'],
            NOME_PROGRAMMA=data['NOME_PROGRAMMA'],
            ORARIO_INIZIO_PROGRAMMA=data['ORARIO_INIZIO_PROGRAMMA'],
            ORARIO_FINE_PROGRAMMA=data['ORARIO_FINE_PROGRAMMA']
        )

        try:
            db.session.add(nuovo_programma)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione del programma"}, 500

        return one_programma_schema.dump(nuovo_programma), 201



    def patch(self, id):

        # get the one schedule from the DB with the corresponding ID
        programma = LookupProgrammiModel.query.get(id)

        # if the ID is not found in the DB, return 404 error, schedule not found
        if not programma:
            return {"message": "Programma non trovato"}, 404
        
        # get JSON for REST API request body
        # silent=True does not throw any exception if request body is empty (or not in a JSON format)
        data = request.get_json(silent=True) or {}

        try:
            # load method returnes a dictionary with all valid fields
            # if a field has a wrong data type or does not exist on DB table, it throws a ValidationError
            # partial=True allows to get a JSON request with only a subset of fields
            valid_data = one_programma_schema.load(data, partial=True)
        except ValidationError:
            return {"message": "I valori inseriti per la modifica del programma non sono validi"}, 400
        
        # sets the allowed fields and updates only them on DB
        allowed_fields = ['VALORE_SEQUENZA_TEMPORALE_PROGRAMMA', 'NOME_PROGRAMMA', 'ORARIO_INIZIO_PROGRAMMA', 'ORARIO_FINE_PROGRAMMA']
        for key, value in valid_data.items():
            if key in allowed_fields:
                setattr(programma, key, value)
        
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante l'aggiornamento del programma"}, 500

        return one_programma_schema.dump(programma), 200
    


    def delete(self, id):

        # get the one schedule from the DB with the corresponding ID
        programma = LookupProgrammiModel.query.get(id)

        # if the ID is not found in the DB, return 404 error, schedule not found
        if not programma:
            return {"message": "Programma non trovato"}, 404

        # else delete the schedule from the DB
        try:
            db.session.delete(programma)
            db.session.commit()
            return {"message": "Programma eliminato"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione del programma"}, 500