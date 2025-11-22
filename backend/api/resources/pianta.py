import json
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from api.models.pianta import ActPianteTestataModel, ActPianteDettaglioModel, ActPianteDettaglioSensoriModel
from api.models.stato import LookupStatiModel
from api.models.programma import LookupProgrammiModel
from api.models.stanza import LookupStanzeModel
from api.models import db
from api.schemas.pianta import ActPianteSchema



many_piante_schema = ActPianteSchema(many=True)
one_piante_schema = ActPianteSchema()



class ActPianteResource(Resource):


    def get(self, id=None):

        # the map helps the fields attribute during REST API invoke to not write the model for each field
        fields_map = {
            'ID_PIANTA' : ActPianteTestataModel.ID_PIANTA,
            'ID_STATO_PIANTA' : ActPianteTestataModel.ID_STATO_PIANTA,
            'NOME_STATO' : LookupStatiModel.NOME_STATO,
            'DESCRIZIONE_STATO' : LookupStatiModel.DESCRIZIONE_STATO,
            'ID_ULTIMO_PROGRAMMA_ESEGUITO' : ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO,
            'DATA_INSERIMENTO' : ActPianteTestataModel.DATA_INSERIMENTO,
            'DATA_ULTIMA_MODIFICA' : ActPianteTestataModel.DATA_ULTIMA_MODIFICA,
            'NOME_PIANTA' : ActPianteDettaglioModel.NOME_PIANTA,
            'DESCRIZIONE_PIANTA' : ActPianteDettaglioModel.DESCRIZIONE_PIANTA,
            # 'FOTO_PIANTA' : ActPianteDettaglioModel.FOTO_PIANTA,
            'ID_STANZA' : ActPianteDettaglioModel.ID_STANZA,
            'POSIZIONE_STANZA_X' : ActPianteDettaglioModel.POSIZIONE_STANZA_X,
            'POSIZIONE_STANZA_Y' : ActPianteDettaglioModel.POSIZIONE_STANZA_Y,
            'UMIDITA_CORRENTE' : ActPianteDettaglioSensoriModel.UMIDITA_CORRENTE,
            'ACQUA_ULTIMA_INNAFFIATURA' : ActPianteDettaglioSensoriModel.ACQUA_ULTIMA_INNAFFIATURA,
            'ALTRO_DATO_SENSORI_1' : ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_1,
            'ALTRO_DATO_SENSORI_2' : ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_2,
            'ALTRO_DATO_SENSORI_3' : ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_3,
            'ALTRO_DATO_SENSORI_4' : ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_4
        }
        
        # fields to return can be chosen both if ID is None or populated
        fields = request.args.get('fields', default=None, type=str)

        if fields is None:
            fields = [ActPianteTestataModel.ID_PIANTA,
                        ActPianteTestataModel.ID_STATO_PIANTA,
                        LookupStatiModel.NOME_STATO,
                        LookupStatiModel.DESCRIZIONE_STATO,
                        ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO,
                        ActPianteTestataModel.DATA_INSERIMENTO,
                        ActPianteTestataModel.DATA_ULTIMA_MODIFICA,
                        ActPianteDettaglioModel.NOME_PIANTA,
                        ActPianteDettaglioModel.DESCRIZIONE_PIANTA,
                        #ActPianteDettaglioModel.FOTO_PIANTA,
                        ActPianteDettaglioModel.ID_STANZA,
                        ActPianteDettaglioModel.POSIZIONE_STANZA_X,
                        ActPianteDettaglioModel.POSIZIONE_STANZA_Y,
                        ActPianteDettaglioSensoriModel.UMIDITA_CORRENTE,
                        ActPianteDettaglioSensoriModel.ACQUA_ULTIMA_INNAFFIATURA,
                        ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_1,
                        ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_2,
                        ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_3,
                        ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_4]
        else:
            # gets the fields list in the REST API invoke and associates them with the ones in the map
            fields = [field.strip() for field in fields.split(',') if field.strip()]
            fields = [fields_map[name] for name in fields if name in fields_map]


        # if ID does not exists, get all plants
        if id is None:
            try:

                page = request.args.get('page', default=1, type=int)
                limit = request.args.get('limit', default=25, type=int)
                orderBy = request.args.get('orderBy', default='DATA_ULTIMA_MODIFICA:desc', type=str)

                if page < 1:
                    return {"message": "La pagina deve essere un valore positivo"}, 400
                if limit < 1 or limit > 100:
                    return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
                orderBy = orderBy.split(':')
                

                # query construction:
                #   with_entities filters the query showing only the fields specified in the fields array
                query = ActPianteTestataModel.query\
                            .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .outerjoin(ActPianteDettaglioSensoriModel, ActPianteDettaglioSensoriModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .join(LookupStatiModel, LookupStatiModel.ID_STATO == ActPianteTestataModel.ID_STATO_PIANTA)\
                            .with_entities(*fields)\
                            .order_by(fields_map.get(orderBy[0]).desc() if orderBy[1].lower() == 'desc' else fields_map.get(orderBy[0]).asc())

                pagination = query.paginate(page=page, per_page=limit, error_out=False)
                piante = pagination.items
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "piante": many_piante_schema.dump(piante),
                    "count": len(piante),
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
            # query construction:
            #   with_entities filters the query showing only the fields specified in the fields array
            #   filter shows the only plant with the ID specified in the path
            pianta = ActPianteTestataModel.query\
                        .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                        .outerjoin(ActPianteDettaglioSensoriModel, ActPianteDettaglioSensoriModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                        .with_entities(*fields)\
                        .filter(ActPianteTestataModel.ID_PIANTA == id)\
                        .first()
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


        # gets the photos bytes from the file attachment in the multipart form-data request
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
        
        # gets the created plant
        pianta_completa = ActPianteTestataModel.query\
                            .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .filter(ActPianteTestataModel.ID_PIANTA == nuova_pianta.ID_PIANTA)\
                            .first()

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