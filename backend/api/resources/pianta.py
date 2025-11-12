import json
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from api.models.pianta import ActPianteTestataModel, ActPianteDettaglioModel, ActPianteDettaglioSensoriModel
from api.models import db
from api.schemas.pianta import ActPianteSchema



many_piante_schema = ActPianteSchema(many=True)
one_piante_schema = ActPianteSchema()



class ActPianteResource(Resource):


    def get(self, id=None):

        # if ID does not exists, get all plants
        if id is None:
            try:

                page = request.args.get('page', default=1, type=int)
                limit = request.args.get('limit', default=25, type=int)
                fields = request.args.get('fields', default=None, type=str)
                # orderBy = request.args.get('orderBy', default='ActPianteTestataModel.DATA_ULTIMA_MODIFICA:desc', type=str)

                if page < 1:
                    return {"message": "La pagina deve essere un valore positivo"}, 400
                if limit < 1 or limit > 100:
                    return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
                if fields is None:
                    fields = [ActPianteTestataModel.ID_PIANTA,
                              ActPianteTestataModel.ID_STATO_PIANTA,
                              ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO,
                              ActPianteTestataModel.DATA_INSERIMENTO,
                              ActPianteTestataModel.DATA_ULTIMA_MODIFICA,
                              ActPianteDettaglioModel.NOME_PIANTA,
                              ActPianteDettaglioModel.DESCRIZIONE_PIANTA,
                              ActPianteDettaglioModel.FOTO_PIANTA,
                              ActPianteDettaglioModel.ID_STANZA,
                              ActPianteDettaglioModel.POSIZIONE_STANZA_X,
                              ActPianteDettaglioModel.POSIZIONE_STANZA_Y,
                              ActPianteDettaglioSensoriModel.UMIDITA_CORRENTE,
                              ActPianteDettaglioSensoriModel.ACQUA_ULTIMA_INNAFFIATURA,
                              ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_1,
                              ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_2,
                              ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_3,
                              ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_4]

                #if orderBy is not None:
                query = ActPianteTestataModel.query.order_by(ActPianteTestataModel.DATA_ULTIMA_MODIFICA.desc())

                piante = ActPianteTestataModel.query\
                            .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .outerjoin(ActPianteDettaglioSensoriModel, ActPianteDettaglioSensoriModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .order_by(ActPianteTestataModel.DATA_ULTIMA_MODIFICA.desc())
                pagination = piante.paginate(page=page, per_page=limit, error_out=False)
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "piante": many_piante_schema.dump(piante),
                    "count": len(pagination.items),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero delle piante"}, 500
        
        # else if ID is not null, get the one plant corresponding to the ID
        try:
            pianta = ActPianteTestataModel.query\
                        .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                        .join(ActPianteDettaglioSensoriModel, ActPianteDettaglioSensoriModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                        .filter(ActPianteTestataModel.ID_PIANTA == id).first()
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero della pianta"}, 500

        # if the plant has been retrieve successfully from the DB
        if pianta:
            return one_piante_schema.dump(pianta), 200

        # else return 404 error, plant not found
        return {"message": "Pianta non trovata"}, 404
    


    # plant creation is implemented with multipart form-data
    def post(self):

        # gets JSON payload with all fields except the photo
        try:
            data = request.form.get('payload')
            payload = json.loads(data)
        except Exception as e:
            return {"message": "Errore durante il recupero dei dati da salvare"}, 400


        bytes_foto = None
        file_foto = request.files.get('image')
        if file_foto:
            try:
                bytes_foto = file_foto.read()
            except Exception as e:
                return {"message": "Errore durante il recupero della foto da salvare"}, 400


        # create a new plant with request body's data
        nuova_pianta = ActPianteTestataModel(
            ID_STATO_PIANTA=payload.get('ID_STATO_PIANTA'),
            ID_ULTIMO_PROGRAMMA_ESEGUITO=payload.get('ID_ULTIMO_PROGRAMMA_ESEGUITO'),
        )
        
        nuova_pianta.dettaglio = ActPianteDettaglioModel(
            ID_PIANTA=nuova_pianta.ID_PIANTA,
            NOME_PIANTA=payload.get('NOME_PIANTA'),
            DESCRIZIONE_PIANTA=payload.get('DESCRIZIONE_PIANTA'),
            FOTO_PIANTA=bytes_foto,
            ID_STANZA=payload.get('ID_STANZA'),
            POSIZIONE_STANZA_X=payload.get('POSIZIONE_STANZA_X'),
            POSIZIONE_STANZA_Y=payload.get('POSIZIONE_STANZA_Y')
        )


        try:
            db.session.add(nuova_pianta)
            db.session.add(nuova_pianta.dettaglio)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Errore durante la creazione della pianta: " + str(e)}, 500
        
        pianta_completa = ActPianteTestataModel.query\
                            .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .filter(ActPianteTestataModel.ID_PIANTA == nuova_pianta.ID_PIANTA).first()

        return one_piante_schema.dump(pianta_completa), 201



    def patch(self, id):

        # get the one schedule from the DB with the corresponding ID
        programma = ActPianteTestataModel.query.get(id)

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
            valid_data = one_piante_schema.load(data, partial=True)
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

        return one_piante_schema.dump(programma), 200
    


    def delete(self, id):

        # get the one schedule from the DB with the corresponding ID
        programma = ActPianteTestataModel.query.get(id)

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