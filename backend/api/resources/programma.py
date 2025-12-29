import json
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from api.models import db
from api.models.programma import LookupProgrammiModel
from api.schemas.programma import LookupProgrammiSchema



many_schedules_schema = LookupProgrammiSchema(many=True)
one_schedule_schema = LookupProgrammiSchema()



class LookupProgrammiResource(Resource):


    def get(self, scheduleID=None):


        # if ID does not exists, get all schedules
        if scheduleID is None:
            
            try:

                page = request.args.get('page', default=1, type=int)
                limit = request.args.get('limit', default=25, type=int)

                if page < 1:
                    return {"message": "La pagina deve essere un valore positivo"}, 400
                if limit < 1 or limit > 100:
                    return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
                

                # get all schedules from the DB
                schedules = LookupProgrammiModel.query.\
                                order_by(LookupProgrammiModel.VALORE_SEQUENZA_TEMPORALE_PROGRAMMA)


                pagination = schedules.paginate(page=page, per_page=limit, error_out=False)
                schedulesArray = pagination.items
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "programmi": many_schedules_schema.dump(schedulesArray),
                    "count": len(schedulesArray),
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
            schedule = LookupProgrammiModel.query.get(scheduleID)
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero del programma"}, 500

        # if the schedule has been successfully retrieved from the DB
        if schedule:
            return one_schedule_schema.dump(schedule), 200

        # else return 404 error, schedule not found
        return {"message": "Programma non trovato"}, 404
    


    def post(self):

        # get JSON for REST API request body
        requestPayload = request.get_json()

        # create a new schedule with request payload's data
        newSchedule = LookupProgrammiModel(
            VALORE_SEQUENZA_TEMPORALE_PROGRAMMA=requestPayload['VALORE_SEQUENZA_TEMPORALE_PROGRAMMA'],
            NOME_PROGRAMMA=requestPayload['NOME_PROGRAMMA'],
            ORARIO_INIZIO_PROGRAMMA=requestPayload['ORARIO_INIZIO_PROGRAMMA'],
            ORARIO_FINE_PROGRAMMA=requestPayload['ORARIO_FINE_PROGRAMMA']
        )


        try:
            db.session.add(newSchedule)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione del programma"}, 500

        return one_schedule_schema.dump(newSchedule), 201



    def patch(self, scheduleID):

        # get the one schedule from the DB with the corresponding ID
        schedule = LookupProgrammiModel.query.get(scheduleID)


        # if the ID is not found in the DB, return 404 error, schedule not found
        if not schedule:
            return {"message": "Programma non trovato"}, 404


        # get JSON for REST API request body
        #   silent=True does not throw any exception if request payload is empty (or not in a JSON format)
        jsonRequestPayload = request.get_json(silent=True) or {}

        try:
            # load method returnes a dictionary with all the valid fields
            #   if a field has a wrong data type or does not exist on DB table, it throws a ValidationError
            #   partial=True allows to accept a JSON request payload with only a subset of fields
            validFields = one_schedule_schema.load(jsonRequestPayload, partial=True)
        except ValidationError:
            return {"message": "I valori inseriti per la modifica del programma non sono validi"}, 400
        

        # set the allowed fields and update only them on DB
        allowedFields = ['VALORE_SEQUENZA_TEMPORALE_PROGRAMMA', 'NOME_PROGRAMMA', 'ORARIO_INIZIO_PROGRAMMA', 'ORARIO_FINE_PROGRAMMA']
        for key, value in validFields.items():
            if key in allowedFields:
                setattr(schedule, key, value)
        

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante l'aggiornamento del programma"}, 500

        return one_schedule_schema.dump(schedule), 200
    


    def delete(self, scheduleID):

        # get the one schedule from the DB with the corresponding ID
        schedule = LookupProgrammiModel.query.get(scheduleID)

        # if the ID is not found in the DB, return 404 error, schedule not found
        if not schedule:
            return {"message": "Programma non trovato"}, 404


        # else delete the schedule from the DB
        try:
            db.session.delete(schedule)
            db.session.commit()
            return {"message": "Programma eliminato"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione del programma"}, 500