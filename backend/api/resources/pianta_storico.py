import json, datetime
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from api.models import db
from api.models.pianta_storico import ActPianteStoricoModel
from api.models.pianta import ActPianteTestataModel #, ActPianteDettaglioModel, ActPianteDettaglioSensoriModel
from api.models.stato import LookupStatiModel
from api.models.programma import LookupProgrammiModel
from api.schemas.pianta_storico import ActPianteStoricoSchema




many_piante_storico_schema = ActPianteStoricoSchema(many=True)
one_piante_storico_schema = ActPianteStoricoSchema()



""" all_plant_fields_without_sensors = [ActPianteTestataModel.ID_PIANTA,
                                    ActPianteTestataModel.ID_STATO_PIANTA,
                                    LookupStatiModel.NOME_STATO.label('NOME_STATO'),
                                    LookupStatiModel.DESCRIZIONE_STATO.label('DESCRIZIONE_STATO'),
                                    ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO,
                                    LookupProgrammiModel.NOME_PROGRAMMA.label('NOME_PROGRAMMA'),
                                    LookupProgrammiModel.ORARIO_INIZIO_PROGRAMMA.label('ORARIO_INIZIO_PROGRAMMA'),
                                    LookupProgrammiModel.ORARIO_FINE_PROGRAMMA.label('ORARIO_FINE_PROGRAMMA'),
                                    ActPianteTestataModel.DATA_INSERIMENTO,
                                    ActPianteTestataModel.DATA_ULTIMA_MODIFICA,
                                    ActPianteDettaglioModel.NOME_PIANTA,
                                    ActPianteDettaglioModel.DESCRIZIONE_PIANTA,
                                    ActPianteDettaglioModel.ID_STANZA,
                                    LookupStanzeModel.NOME_STANZA.label('NOME_STANZA'),
                                    ActPianteDettaglioModel.POSIZIONE_STANZA_X,
                                    ActPianteDettaglioModel.POSIZIONE_STANZA_Y]


all_plant_fields = [ActPianteTestataModel.ID_PIANTA,
                    ActPianteTestataModel.ID_STATO_PIANTA,
                    LookupStatiModel.NOME_STATO.label('NOME_STATO'),
                    LookupStatiModel.DESCRIZIONE_STATO.label('DESCRIZIONE_STATO'),
                    ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO,
                    LookupProgrammiModel.NOME_PROGRAMMA.label('NOME_PROGRAMMA'),
                    LookupProgrammiModel.ORARIO_INIZIO_PROGRAMMA.label('ORARIO_INIZIO_PROGRAMMA'),
                    LookupProgrammiModel.ORARIO_FINE_PROGRAMMA.label('ORARIO_FINE_PROGRAMMA'),
                    ActPianteTestataModel.DATA_INSERIMENTO,
                    ActPianteTestataModel.DATA_ULTIMA_MODIFICA,
                    ActPianteDettaglioModel.NOME_PIANTA,
                    ActPianteDettaglioModel.DESCRIZIONE_PIANTA,
                    ActPianteDettaglioModel.ID_STANZA,
                    LookupStanzeModel.NOME_STANZA.label('NOME_STANZA'),
                    ActPianteDettaglioModel.POSIZIONE_STANZA_X,
                    ActPianteDettaglioModel.POSIZIONE_STANZA_Y,
                    ActPianteDettaglioSensoriModel.UMIDITA_CORRENTE,
                    ActPianteDettaglioSensoriModel.ACQUA_ULTIMA_INNAFFIATURA,
                    ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_1,
                    ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_2,
                    ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_3,
                    ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_4]


photo_fields = [ActPianteTestataModel.ID_PIANTA,
                ActPianteDettaglioModel.FOTO_PIANTA] """


all_history_plant_fields = [ActPianteStoricoModel.ID_PIANTA,
                            ActPianteStoricoModel.ID_STATO_PIANTA,
                            LookupStatiModel.NOME_STATO.label('NOME_STATO'),
                            LookupStatiModel.DESCRIZIONE_STATO.label('DESCRIZIONE_STATO'),
                            ActPianteStoricoModel.ID_PROGRAMMA_ESEGUITO,
                            LookupProgrammiModel.NOME_PROGRAMMA.label('NOME_PROGRAMMA'),
                            LookupProgrammiModel.ORARIO_INIZIO_PROGRAMMA.label('ORARIO_INIZIO_PROGRAMMA'),
                            LookupProgrammiModel.ORARIO_FINE_PROGRAMMA.label('ORARIO_FINE_PROGRAMMA'),
                            ActPianteStoricoModel.UMIDITA_CORRENTE,
                            ActPianteStoricoModel.ACQUA_ULTIMA_INNAFFIATURA,
                            ActPianteStoricoModel.ALTRO_DATO_SENSORI_1,
                            ActPianteStoricoModel.ALTRO_DATO_SENSORI_2,
                            ActPianteStoricoModel.ALTRO_DATO_SENSORI_3,
                            ActPianteStoricoModel.ALTRO_DATO_SENSORI_4,
                            ActPianteStoricoModel.DATA_MODIFICA,]





class ActPianteStoricoResource(Resource):


    def get(self, id=None):


        # the map helps the fields attribute during REST API invoke to not write the model for each field
        fields_map = {
            'ID_PIANTA' : ActPianteStoricoModel.ID_PIANTA,
            'ID_STATO_PIANTA' : ActPianteStoricoModel.ID_STATO_PIANTA,
            'NOME_STATO' : LookupStatiModel.NOME_STATO,
            'DESCRIZIONE_STATO' : LookupStatiModel.DESCRIZIONE_STATO,
            'ID_PROGRAMMA_ESEGUITO' : ActPianteStoricoModel.ID_PROGRAMMA_ESEGUITO,
            'NOME_PROGRAMMA' : LookupProgrammiModel.NOME_PROGRAMMA,
            'ORARIO_INIZIO_PROGRAMMA' : LookupProgrammiModel.ORARIO_INIZIO_PROGRAMMA,
            'ORARIO_FINE_PROGRAMMA' : LookupProgrammiModel.ORARIO_FINE_PROGRAMMA,
            'UMIDITA_CORRENTE' : ActPianteStoricoModel.UMIDITA_CORRENTE,
            'ACQUA_ULTIMA_INNAFFIATURA' : ActPianteStoricoModel.ACQUA_ULTIMA_INNAFFIATURA,
            'ALTRO_DATO_SENSORI_1' : ActPianteStoricoModel.ALTRO_DATO_SENSORI_1,
            'ALTRO_DATO_SENSORI_2' : ActPianteStoricoModel.ALTRO_DATO_SENSORI_2,
            'ALTRO_DATO_SENSORI_3' : ActPianteStoricoModel.ALTRO_DATO_SENSORI_3,
            'ALTRO_DATO_SENSORI_4' : ActPianteStoricoModel.ALTRO_DATO_SENSORI_4,
            'DATA_MODIFICA' : ActPianteStoricoModel.DATA_MODIFICA
        }
        
        
        """ # fields to return can be chosen both if ID is None or populated
        fields = request.args.get('fields', default=None, type=str)

        if fields is None:
            fields = all_plant_fields
        else:
            # gets the fields list in the REST API invoke and associates them with the ones in the map
            fields = [field.strip() for field in fields.split(',') if field.strip()]
            fields = [fields_map[name].label(name) for name in fields if name in fields_map] """


        # if ID does not exists, get all history plants
        if id is None:

            try:

                page = request.args.get('page', default=1, type=int)
                limit = request.args.get('limit', default=25, type=int)
                orderBy = request.args.get('orderBy', default='DATA_MODIFICA:desc', type=str)

                if page < 1:
                    return {"message": "La pagina deve essere un valore positivo"}, 400
                if limit < 1 or limit > 100:
                    return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
                orderBy = orderBy.split(':')
                

                # query construction:
                #   with_entities filters the query showing only the fields specified in the fields array
                query = ActPianteStoricoModel.query\
                            .join(ActPianteTestataModel, ActPianteTestataModel.ID_PIANTA == ActPianteStoricoModel.ID_PIANTA)\
                            .join(LookupStatiModel, LookupStatiModel.ID_STATO == ActPianteStoricoModel.ID_STATO_PIANTA)\
                            .join(LookupProgrammiModel, LookupProgrammiModel.ID_PROGRAMMA == ActPianteStoricoModel.ID_PROGRAMMA_ESEGUITO)\
                            .with_entities(*all_history_plant_fields)\
                            .order_by(fields_map.get(orderBy[0]).desc() if orderBy[1].lower() == 'desc' else fields_map.get(orderBy[0]).asc())


                
                pagination = query.paginate(page=page, per_page=limit, error_out=False)
                piante = pagination.items
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "piante": many_piante_storico_schema.dump(piante),
                    "count": len(piante),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero dello storico delle piante"}, 500
        
        # else if ID is not null, get the one plant corresponding to the ID
        try:
            # query construction:
            #   with_entities filters the query showing only the fields specified in the fields array
            #   filter shows the only plant with the ID specified in the path
            pianta = ActPianteStoricoModel.query\
                        .join(ActPianteTestataModel, ActPianteTestataModel.ID_PIANTA == ActPianteStoricoModel.ID_PIANTA)\
                        .join(LookupStatiModel, LookupStatiModel.ID_STATO == ActPianteStoricoModel.ID_STATO_PIANTA)\
                        .join(LookupProgrammiModel, LookupProgrammiModel.ID_PROGRAMMA == ActPianteStoricoModel.ID_PROGRAMMA_ESEGUITO)\
                        .with_entities(*all_history_plant_fields)\
                        .filter(ActPianteStoricoModel.ID_PIANTA == id)\
                        .first()
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero dello storico della pianta"}, 500

        # if the plant has been retrieve successfully from the DB
        if pianta:
            return one_piante_storico_schema.dump(pianta), 200

        # else return 404 error, plant not found
        return {"message": "Pianta non trovata"}, 404
    


    # plant creation is implemented with multipart form-data
    def post(self):

        # gets JSON payload with all fields except for the photo
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
        
        # need to create new model for plant details, because it does not exist in the database yet
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
            return {"message": "Errore durante la creazione della pianta"}, 500
        
        # gets the created plant
        pianta_completa = ActPianteTestataModel.query\
                            .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .join(LookupStatiModel, LookupStatiModel.ID_STATO == ActPianteTestataModel.ID_STATO_PIANTA)\
                            .join(LookupProgrammiModel, LookupProgrammiModel.ID_PROGRAMMA == ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO)\
                            .join(LookupStanzeModel, LookupStanzeModel.ID_STANZA == ActPianteDettaglioModel.ID_STANZA)\
                            .with_entities(*all_plant_fields_without_sensors)\
                            .filter(ActPianteTestataModel.ID_PIANTA == nuova_pianta.ID_PIANTA)\
                            .first()

        return one_piante_schema.dump(pianta_completa), 201



    def patch(self, id):
        
        # get the one plant from the DB with the corresponding ID
        pianta = ActPianteTestataModel.query.get(id)

        # if the ID is not found in the DB, return 404 error, plant not found
        if not pianta:
            return {"message": "Pianta non trovata"}, 404
        

        # gets JSON payload with all fields to be updated except for the photo
        payload=None
        try:
            data = request.form.get('payload')
            if data is not None:
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

        

        valid_data=None
        try:
            # load method returnes a dictionary with all valid fields
            #   if a field has a wrong data type or does not exist on DB table, it throws a ValidationError
            #   partial=True allows to get a JSON request with only a subset of fields
            if payload is not None:
                valid_data = one_piante_schema.load(payload, partial=True)
        except ValidationError:
            return {"message": "I valori inseriti per la modifica della pianta non sono validi"}, 400
        
        
        # sets the allowed fields and updates only them on DB
        allowed_fields = ['NOME_PIANTA',
                          'DESCRIZIONE_PIANTA',
                          'ID_STATO_PIANTA',
                          'ID_STANZA',
                          'POSIZIONE_STANZA_X',
                          'POSIZIONE_STANZA_Y',
                          'ID_ULTIMO_PROGRAMMA_ESEGUITO',
                          'UMIDITA_CORRENTE',
                          'ACQUA_ULTIMA_INNAFFIATURA',
                          'ALTRO_DATO_SENSORI_1',
                          'ALTRO_DATO_SENSORI_2',
                          'ALTRO_DATO_SENSORI_3',
                          'ALTRO_DATO_SENSORI_4']
        # it scrolls the valid_data dictionary
        #   key contains the header table's field or the table itself, like "dettaglio" and "dettaglio_sensori"
        #   value contains the corresponding value or the json payload with all the fields of the current table
        if valid_data is not None:
            for key, value in valid_data.items():
                # if current table is the header table, key is the specific field
                if key in allowed_fields:
                    setattr(pianta, key, value)
                else:
                    # gets the relationship between header plant and its details
                    pianta_relationship = getattr(pianta, key)
                    # when the key is "dettaglio_sensori" the relationship might not exist
                    #   because it's not created during the plant creation
                    if key == 'dettaglio_sensori' and pianta_relationship is None:
                        try:
                            # initializes the relationship between header plant and sensors details
                            pianta_relationship = ActPianteDettaglioSensoriModel(
                                ID_PIANTA=id,
                                UMIDITA_CORRENTE=None,
                                ACQUA_ULTIMA_INNAFFIATURA=None,
                                ALTRO_DATO_SENSORI_1=None,
                                ALTRO_DATO_SENSORI_2=None,
                                ALTRO_DATO_SENSORI_3=None,
                                ALTRO_DATO_SENSORI_4=None
                            )
                            pianta.dettaglio_sensori = pianta_relationship
                            db.session.add(pianta_relationship)
                        except SQLAlchemyError as e:
                            db.session.rollback()
                            return {"message": "Errore durante l'aggiornamento dei dati dei sensori"}, 500
                    # it scrolls the json payload for the current table
                    for t_key, t_value in value.items():
                        # if the current field is allowed, it updates its value
                        if t_key in allowed_fields:
                            setattr(pianta_relationship, t_key, t_value)
        

        try:
            if bytes_foto is not None:
                pianta.dettaglio.FOTO_PIANTA = bytes_foto
            pianta.DATA_ULTIMA_MODIFICA = datetime.datetime.now()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante l'aggiornamento della pianta"}, 500
        
        # gets the updated plant
        pianta_completa = ActPianteTestataModel.query\
                            .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .outerjoin(ActPianteDettaglioSensoriModel, ActPianteDettaglioSensoriModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .join(LookupStatiModel, LookupStatiModel.ID_STATO == ActPianteTestataModel.ID_STATO_PIANTA)\
                            .join(LookupProgrammiModel, LookupProgrammiModel.ID_PROGRAMMA == ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO)\
                            .join(LookupStanzeModel, LookupStanzeModel.ID_STANZA == ActPianteDettaglioModel.ID_STANZA)\
                            .with_entities(*all_plant_fields)\
                            .filter(ActPianteTestataModel.ID_PIANTA == id)\
                            .first()

        return one_piante_schema.dump(pianta_completa), 200
    


    def delete(self, id):

        # get the one plant from the DB with the corresponding ID
        plant = ActPianteTestataModel.query.get(id)
        plant_detail = ActPianteDettaglioModel.query.get(id)
        plant_detail_sensors = ActPianteDettaglioSensoriModel.query.get(id)

        # if the ID is not found in the DB, return 404 error, plant not found
        if not plant:
            return {"message": "Pianta non trovata"}, 404

        # else delete the plant from the DB
        try:
            if plant_detail_sensors is not None:
                db.session.delete(plant_detail_sensors)
            db.session.delete(plant_detail)
            db.session.delete(plant)
            db.session.commit()
            return {"message": "Pianta eliminata"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione della pianta"}, 500