from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from api.models import db
from api.models.stato import LookupStatiModel
from api.schemas.stato import LookupStatiSchema



many_statuses_schema = LookupStatiSchema(many=True)
one_status_schema = LookupStatiSchema()



class LookupStatiResource(Resource):


    def get(self, statusID=None):


        # if ID does not exists, get all statuses
        if statusID is None:
            try:

                page = request.args.get('page', default=1, type=int)
                limit = request.args.get('limit', default=25, type=int)

                if page < 1:
                    return {"message": "La pagina deve essere un valore positivo"}, 400
                if limit < 1 or limit > 100:
                    return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400


                statuses = LookupStatiModel.query.order_by(LookupStatiModel.ID_STATO)


                pagination = statuses.paginate(page=page, per_page=limit, error_out=False)
                statusesArray = pagination.items
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "stati": many_statuses_schema.dump(statusesArray),
                    "count": len(statusesArray),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero degli stati"}, 500
        

        # else if ID is not null, get the one status corresponding to the ID
        try:
            status = LookupStatiModel.query.get(statusID)
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero dello stato"}, 500


        # if the status has been successfully retrieved from the DB
        if status:
            return one_status_schema.dump(status), 200

        # else return 404 error, status not found
        return {"message": "Stato non trovato"}, 404
    


    def post(self):

        # get JSON for REST API request body
        requestPayload = request.get_json()

        # create a new status with request payload's data
        newStatus = LookupStatiModel(
            ID_STATO=requestPayload['ID_STATO'],
            NOME_STATO=requestPayload['NOME_STATO'],
            DESCRIZIONE_STATO=requestPayload['DESCRIZIONE_STATO']
        )


        try:
            db.session.add(newStatus)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione dello stato"}, 500

        return one_status_schema.dump(newStatus), 201



    def patch(self, statusID):

        # get the one status from the DB with the corresponding ID
        status = LookupStatiModel.query.get(statusID)


        # if the ID is not found in the DB, return 404 error, status not found
        if not status:
            return {"message": "Stato non trovato"}, 404


        # get JSON for REST API request body
        #   silent=True does not throw any exception if request payload is empty (or not in a JSON format)
        jsonRequestPayload = request.get_json(silent=True) or {}

        try:
            # load method returnes a dictionary with all the valid fields
            #   if a field has a wrong data type or does not exist on DB table, it throws a ValidationError
            #   partial=True allows to accept a JSON request payload with only a subset of fields
            validFields = one_status_schema.load(jsonRequestPayload, partial=True)
        except ValidationError:
            return {"message": "I valori inseriti per la modifica dello stato non sono validi"}, 400
        

        # set the allowed fields and updates only them on DB
        allowedFields = ['ID_STATO', 'NOME_STATO', 'DESCRIZIONE_STATO']
        for key, value in validFields.items():
            if key in allowedFields:
                setattr(status, key, value)
        

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante l'aggiornamento dello stato"}, 500

        return one_status_schema.dump(status), 200
    


    def delete(self, statusID):

        # get the one status from the DB with the corresponding ID
        status = LookupStatiModel.query.get(statusID)


        # if the ID is not found in the DB, return 404 error, status not found
        if not status:
            return {"message": "Stato non trovato"}, 404


        # else delete the status from the DB
        try:
            db.session.delete(status)
            db.session.commit()
            return {"message": "Stato eliminato"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione dello stato"}, 500