from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from api.models import db
from api.models.stanza import LookupStanzeModel
from api.schemas.stanza import LookupStanzeSchema



many_rooms_schema = LookupStanzeSchema(many=True)
one_room_schema = LookupStanzeSchema()



class LookupStanzeResource(Resource):


    def get(self, roomID=None):


        # if ID does not exists, get all rooms
        if roomID is None:
            try:

                page = request.args.get('page', default=1, type=int)
                limit = request.args.get('limit', default=25, type=int)

                if page < 1:
                    return {"message": "La pagina deve essere un valore positivo"}, 400
                if limit < 1 or limit > 100:
                    return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
                

                rooms = LookupStanzeModel.query.order_by(LookupStanzeModel.NOME_STANZA)


                pagination = rooms.paginate(page=page, per_page=limit, error_out=False)
                roomsArray = pagination.items
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "stanze": many_rooms_schema.dump(roomsArray),
                    "count": len(roomsArray),
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
            room = LookupStanzeModel.query.get(roomID)
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero della stanza"}, 500


        # if the room has been retrieve successfully from the DB
        if room:
            return one_room_schema.dump(room), 200

        # else return 404 error, room not found
        return {"message": "Stanza non trovata"}, 404
    


    def post(self):

        # get JSON for REST API request body
        requestPayload = request.get_json()

        # create a new room with request payload's data
        newRoom = LookupStanzeModel(
            NOME_STANZA=requestPayload['NOME_STANZA'],
            DIMENSIONE_GRIGLIA_X=requestPayload['DIMENSIONE_GRIGLIA_X'],
            DIMENSIONE_GRIGLIA_Y=requestPayload['DIMENSIONE_GRIGLIA_Y']
        )


        try:
            db.session.add(newRoom)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione della stanza"}, 500

        return one_room_schema.dump(newRoom), 201



    def patch(self, roomID):

        # get the one room from the DB with the corresponding ID
        room = LookupStanzeModel.query.get(roomID)


        # if the ID is not found in the DB, return 404 error, room not found
        if not room:
            return {"message": "Stanza non trovata"}, 404


        # get JSON for REST API request body
        #   silent=True does not throw any exception if request payload is empty (or not in a JSON format)
        jsonRequestPayload = request.get_json(silent=True) or {}

        try:
            # load method returnes a dictionary with all the valid fields
            #   if a field has a wrong data type or does not exist on DB table, it throws a ValidationError
            #   partial=True allows to accept a JSON request payload with only a subset of fields
            validFields = one_room_schema.load(jsonRequestPayload, partial=True)
        except ValidationError:
            return {"message": "I valori inseriti per la modifica della stanza non sono validi"}, 400
        

        # set the allowed fields and updates only them on DB
        allowedFields = ['NOME_STANZA', 'DIMENSIONE_GRIGLIA_X', 'DIMENSIONE_GRIGLIA_Y']
        for key, value in validFields.items():
            if key in allowedFields:
                setattr(room, key, value)
        

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante l'aggiornamento della stanza"}, 500

        return one_room_schema.dump(room), 200
    


    def delete(self, roomID):

        # get the one room from the DB with the corresponding ID
        room = LookupStanzeModel.query.get(roomID)


        # if the ID is not found in the DB, return 404 error, room not found
        if not room:
            return {"message": "Stanza non trovata"}, 404


        # else delete the room from the DB
        try:
            db.session.delete(room)
            db.session.commit()
            return {"message": "Stanza eliminata"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione della stanza"}, 500