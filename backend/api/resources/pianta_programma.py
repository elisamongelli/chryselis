from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from api.models.pianta_programma import LookupPianteProgrammiModel
from api.models import db
from api.schemas.pianta_programma import LookupPianteProgrammiSchema



many_piante_programmi_schema = LookupPianteProgrammiSchema(many=True)
one_piante_programma_schema = LookupPianteProgrammiSchema()



class LookupPianteProgrammiResource(Resource):


    def get(self, idPianta=None, idProgramma=None):

        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=25, type=int)

        if page < 1:
            return {"message": "La pagina deve essere un valore positivo"}, 400
        if limit < 1 or limit > 100:
            return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
        
        query = LookupPianteProgrammiModel.query.order_by(LookupPianteProgrammiModel.ID_PIANTA)

        # if plant ID and schedule ID do not exist, get all plants-schedules association
        if idPianta is None and idProgramma is None:
            try:
                pagination = query.paginate(page=page, per_page=limit, error_out=False)
                pianteProgrammi = pagination.items
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "pianteProgrammi": many_piante_programmi_schema.dump(pianteProgrammi),
                    "count": len(pianteProgrammi),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero dell'associazione tra le piante e i programmi"}, 500
        
        # else if plant ID is not null and schedule ID is null, get all plants-schedules association for the plant ID
        if idPianta is not None and idProgramma is None:
            try:
                pagination = query.paginate(page=page, per_page=limit, error_out=False)
                pianteProgrammi = LookupPianteProgrammiModel.query.filter(LookupPianteProgrammiModel.ID_PIANTA == idPianta).all()
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "pianteProgrammi": many_piante_programmi_schema.dump(pianteProgrammi),
                    "count": len(pianteProgrammi),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero dell'associazione tra le piante e i programmi"}, 500
        
        # else if plant ID is null and schedule ID is not null, get all plants-schedules association for the schedule ID
        if idPianta is None and idProgramma is not None:
            try:
                pagination = query.paginate(page=page, per_page=limit, error_out=False)
                pianteProgrammi = LookupPianteProgrammiModel.query.filter(LookupPianteProgrammiModel.ID_PROGRAMMA == idProgramma).all()
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "pianteProgrammi": many_piante_programmi_schema.dump(pianteProgrammi),
                    "count": len(pianteProgrammi),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero dell'associazione tra le piante e i programmi"}, 500
        
        # else if plant ID is not null and schedule ID is not null, get the one plants-schedules association corresponding to the IDs
        try:
            print("id pianta = " + idPianta + "; id programma = " + idProgramma)
            piantaProgramma = LookupPianteProgrammiModel.query.filter(LookupPianteProgrammiModel.ID_PIANTA == idPianta, LookupPianteProgrammiModel.ID_PROGRAMMA == idProgramma).first()
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero dell'associazione tra le piante e i programmi"}, 500

        # if the plants-schedules association has been retrieve successfully from the DB
        if piantaProgramma:
            return one_piante_programma_schema.dump(piantaProgramma), 200

        # else return 404 error, plants-schedules association not found
        return {"message": "Associazione tra le piante e i programmi non trovato"}, 404
    


    def post(self):

        # get JSON for REST API request body
        data = request.get_json()

        # create a new plants-schedules association with request body's data
        nuovo_pianta_programma = LookupPianteProgrammiModel(
            ID_PIANTA=data['ID_PIANTA'],
            ID_PROGRAMMA=data['ID_PROGRAMMA']
        )

        try:
            db.session.add(nuovo_pianta_programma)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione dell'associazione tra le piante e i programmi"}, 500

        return one_piante_programma_schema.dump(nuovo_pianta_programma), 201



    def patch(self, idPianta=None, idProgramma=None):

        return {"message": "Non è possibile modificare l'associazione tra le piante e i programmi. Se l'associazione è sbagliata, eliminarla."}, 500
    


    def delete(self, idPianta, idProgramma):

        # get the one plants-schedules association from the DB with the corresponding ID
        piantaProgramma = LookupPianteProgrammiModel.query.filter(LookupPianteProgrammiModel.ID_PIANTA == idPianta, LookupPianteProgrammiModel.ID_PROGRAMMA == idProgramma).first()

        # if the ID is not found in the DB, return 404 error, plants-schedules association not found
        if not piantaProgramma:
            return {"message": "Associazione tra le piante e i programmi non trovata"}, 404

        # else delete the plants-schedules association from the DB
        try:
            db.session.delete(piantaProgramma)
            db.session.commit()
            return {"message": "Associazione tra le piante e i programmi eliminata"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione dell'associazione tra le piante e i programmi"}, 500