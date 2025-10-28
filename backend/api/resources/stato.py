from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from api.models.stato import LookupStatiModel
from api.models import db
from api.schemas.stato import LookupStatiSchema



many_stati_schema = LookupStatiSchema(many=True)
one_stati_schema = LookupStatiSchema()



class LookupStatiResource(Resource):


    def get(self, id=None):

        offset = request.args.get('offset', default=0, type=int)
        limit = request.args.get('limit', default=20, type=int)

        if offset < 0:
            return {"message": "L'offset deve essere positivo"}, 400
        if limit < 1 or limit > 100:
            return {"message": "Il limite deve essere compreso tra 1 e 100"}, 400

        print("Offset:", offset, "\nLimit:", limit)

        query = LookupStatiModel.query.order_by(LookupStatiModel.ID_STATO)

        # if ID does not exists, get all statuses
        if id is None:
            try:
                pagination = query.paginate(page=offset, per_page=limit, error_out=False)
                items = pagination.items
                total = pagination.total
                pages = pagination.pages
                # stati = LookupStatiModel.query.all()
                return {
                    "stati": many_stati_schema.dump(items),
                    "offset": offset,
                    "limit": limit,
                    "total": total,
                    "pages": pages,
                    "count": len(items)
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero degli stati"}, 500
        
        # else if ID is not null, get the one status corresponding to the ID
        try:
            stato = LookupStatiModel.query.get(id)
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero dello stato"}, 500

        # if the status has been retrieve successfully from the DB
        if stato:
            return one_stati_schema.dump(stato), 200

        # else return 404 error, status not found
        return {"message": "Stato non trovato"}, 404
    


    def post(self):

        # get JSON for REST API request body
        data = request.get_json()

        # create a new status with request body's data
        nuovo_stato = LookupStatiModel(
            ID_STATO=data['ID_STATO'],
            NOME_STATO=data['NOME_STATO'],
            DESCRIZIONE_STATO=data['DESCRIZIONE_STATO']
        )

        try:
            db.session.add(nuovo_stato)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione dello stato"}, 500

        return one_stati_schema.dump(nuovo_stato), 201



    def patch(self, id):

        # get the one status from the DB with the corresponding ID
        stato = LookupStatiModel.query.get(id)

        # if the ID is not found in the DB, return 404 error, status not found
        if not stato:
            return {"message": "Stato non trovato"}, 404
        
        # get JSON for REST API request body
        # silent=True does not throw any exception if request body is empty (or not in a JSON format)
        data = request.get_json(silent=True) or {}

        try:
            # load method returnes a dictionary with all valid fields
            # if a field has a wrong data type or does not exist on DB table, it throws a ValidationError
            # partial=True allows to get a JSON request with only a subset of fields
            valid_data = one_stati_schema.load(data, partial=True)
        except ValidationError:
            return {"message": "I valori inseriti per la modifica dello stato non sono validi"}, 400
        
        # sets the allowed fields and updates only them on DB
        allowed_fields = ['ID_STATO', 'NOME_STATO', 'DESCRIZIONE_STATO']
        for key, value in valid_data.items():
            if key in allowed_fields:
                setattr(stato, key, value)
        
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante l'aggiornamento dello stato"}, 500

        return one_stati_schema.dump(stato), 200
    


    def delete(self, id):

        # get the one status from the DB with the corresponding ID
        stato = LookupStatiModel.query.get(id)

        # if the ID is not found in the DB, return 404 error, status not found
        if not stato:
            return {"message": "Stato non trovato"}, 404

        # else delete the status from the DB
        try:
            db.session.delete(stato)
            db.session.commit()
            return {"message": "Stato eliminato"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione dello stato"}, 500