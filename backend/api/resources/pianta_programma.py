from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from api.models import db
from api.models.pianta_programma import LookupPianteProgrammiModel
from api.schemas.pianta_programma import LookupPianteProgrammiSchema



many_plants_schedules_schema = LookupPianteProgrammiSchema(many=True)
one_plant_schedule_schema = LookupPianteProgrammiSchema()



class LookupPianteProgrammiResource(Resource):


    def get(self, plantID=None, scheduleID=None):


        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=25, type=int)

        if page < 1:
            return {"message": "La pagina deve essere un valore positivo"}, 400
        if limit < 1 or limit > 100:
            return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
        

        # if plant ID and schedule ID do not exist, get all plant-schedule association
        if plantID is None and scheduleID is None:

            try:

                plantSchedule = LookupPianteProgrammiModel.query\
                            .order_by(LookupPianteProgrammiModel.ID_PIANTA)
                
                pagination = plantSchedule.paginate(page=page, per_page=limit, error_out=False)
                plantsSchedules = pagination.items
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "pianteProgrammi": many_plants_schedules_schema.dump(plantsSchedules),
                    "count": len(plantsSchedules),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero dell'associazione tra le piante e i programmi"}, 500
        
        
        # else if plant ID is not null and schedule ID is null, get all plant-schedule association for the plant ID
        if plantID is not None and scheduleID is None:
        
            try:
                
                plantSchedule = LookupPianteProgrammiModel.query\
                                    .filter(LookupPianteProgrammiModel.ID_PIANTA == plantID)\
                                    .order_by(LookupPianteProgrammiModel.ID_PIANTA)
                
                pagination = plantSchedule.paginate(page=page, per_page=limit, error_out=False)
                plantsSchedules = pagination.items # LookupPianteProgrammiModel.query.filter(LookupPianteProgrammiModel.ID_PIANTA == idPianta).all()
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "pianteProgrammi": many_plants_schedules_schema.dump(plantsSchedules),
                    "count": len(plantsSchedules),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero dell'associazione tra le piante e i programmi"}, 500
        

        # else if plant ID is null and schedule ID is not null, get all plant-schedule association for the schedule ID
        if plantID is None and scheduleID is not None:
        
            try:

                plantSchedule = LookupPianteProgrammiModel.query\
                                    .filter(LookupPianteProgrammiModel.ID_PROGRAMMA == scheduleID)
                
                pagination = plantSchedule.paginate(page=page, per_page=limit, error_out=False)
                plantsSchedules = pagination.items # LookupPianteProgrammiModel.query.filter(LookupPianteProgrammiModel.ID_PROGRAMMA == idProgramma).all()
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "pianteProgrammi": many_plants_schedules_schema.dump(plantsSchedules),
                    "count": len(plantsSchedules),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero dell'associazione tra le piante e i programmi"}, 500
        

        # else if plant ID is not null and schedule ID is not null, get the one plant-schedule association corresponding to the IDs
        try:

            plantSchedule = LookupPianteProgrammiModel.query\
                                .filter(LookupPianteProgrammiModel.ID_PIANTA == plantID, LookupPianteProgrammiModel.ID_PROGRAMMA == scheduleID)\
                                .first()
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero dell'associazione tra le piante e i programmi"}, 500


        # if the plant-schedule association has been retrieve successfully from the DB
        if plantSchedule:
            return one_plant_schedule_schema.dump(plantSchedule), 200

        # else return 404 error, plant-schedule association not found
        return {"message": "Associazione tra le piante e i programmi non trovato"}, 404
    


    def post(self):

        # get JSON for REST API request body
        requestPayload = request.get_json()

        # create a new plant-schedule association with request payload's data
        newPlantSchedule = LookupPianteProgrammiModel(
            ID_PIANTA=requestPayload['ID_PIANTA'],
            ID_PROGRAMMA=requestPayload['ID_PROGRAMMA']
        )

        try:
            db.session.add(newPlantSchedule)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione dell'associazione tra le piante e i programmi"}, 500

        return one_plant_schedule_schema.dump(newPlantSchedule), 201



    def patch(self, plantID=None, scheduleID=None):

        return {"message": "Non è possibile modificare l'associazione tra le piante e i programmi. Se l'associazione è sbagliata, eliminarla"}, 500
    


    def delete(self, plantID, scheduleID):

        # get the one plant-schedule association from the DB with the corresponding IDs
        plantSchedule = LookupPianteProgrammiModel.query\
                            .filter(LookupPianteProgrammiModel.ID_PIANTA == plantID, LookupPianteProgrammiModel.ID_PROGRAMMA == scheduleID)\
                            .first()

        # if the ID is not found in the DB, return 404 error, plant-schedule association not found
        if not plantSchedule:
            return {"message": "Associazione tra le piante e i programmi non trovata"}, 404

        # else delete the plant-schedule association from the DB
        try:
            db.session.delete(plantSchedule)
            db.session.commit()
            return {"message": "Associazione tra le piante e i programmi eliminata"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione dell'associazione tra le piante e i programmi"}, 500