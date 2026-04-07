import json, datetime, io, zipfile
from flask import request, Response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, aliased, contains_eager
from marshmallow import ValidationError
from PIL import Image
from api.models import db
from api.models.pianta import ActPianteTestataModel, ActPianteDettaglioModel, ActPianteDettaglioSensoriModel
from api.models.stato import LookupStatiModel
from api.models.programma import LookupProgrammiModel
from api.models.stanza import LookupStanzeModel
from api.schemas.pianta import ActPianteSchema, ActFotoPianteSchema




many_plants_schema = ActPianteSchema(many=True)
one_plant_schema = ActPianteSchema()

one_foto_piante_schema = ActFotoPianteSchema()



photo_fields = [ActPianteTestataModel.ID_PIANTA,
                ActPianteDettaglioModel.FOTO_PIANTA]





class ActPianteResource(Resource):


    def get(self, plantID=None):

        
        # the map helps the fields attribute during REST API invoke to not write the entity for each nested field (detail and sensors detail)
        CONST_FIELDS_ATTRIBUTE_FIELDS_MAP = {
            'NOME_PIANTA': 'dettaglio',
            'DESCRIZIONE_PIANTA': 'dettaglio',
            'ID_STANZA': 'dettaglio',
            'NOME_STANZA': 'dettaglio',
            'POSIZIONE_STANZA_X': 'dettaglio',
            'POSIZIONE_STANZA_Y': 'dettaglio',
            'UMIDITA_CORRENTE': 'dettaglioSensori',
            'ACQUA_ULTIMA_INNAFFIATURA': 'dettaglioSensori',
            'ALTRO_DATO_SENSORI_1': 'dettaglioSensori',
            'ALTRO_DATO_SENSORI_2': 'dettaglioSensori',
            'ALTRO_DATO_SENSORI_3': 'dettaglioSensori',
            'ALTRO_DATO_SENSORI_4': 'dettaglioSensori',
        }


                        
        # define aliases for related tables in order to make joins
        Details = aliased(ActPianteDettaglioModel)
        SensorsDetails = aliased(ActPianteDettaglioSensoriModel)
        Room = aliased(LookupStanzeModel)
        Status = aliased(LookupStatiModel)
        Schedule = aliased(LookupProgrammiModel)


        CONST_ALL_ALIASED_FIELDS = {
            'ID_PIANTA' : ActPianteTestataModel.ID_PIANTA,
            'ID_STATO_PIANTA' : ActPianteTestataModel.ID_STATO_PIANTA,
            'NOME_STATO' : Status.NOME_STATO,
            'DESCRIZIONE_STATO' : Status.DESCRIZIONE_STATO,
            'ID_ULTIMO_PROGRAMMA_ESEGUITO' : ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO,
            'NOME_PROGRAMMA' : Schedule.NOME_PROGRAMMA,
            'ORARIO_INIZIO_PROGRAMMA' : Schedule.ORARIO_INIZIO_PROGRAMMA,
            'ORARIO_FINE_PROGRAMMA' : Schedule.ORARIO_FINE_PROGRAMMA,
            'DATA_INSERIMENTO' : ActPianteTestataModel.DATA_INSERIMENTO,
            'DATA_ULTIMA_MODIFICA' : ActPianteTestataModel.DATA_ULTIMA_MODIFICA,
            'NOME_PIANTA' : Details.NOME_PIANTA,
            'DESCRIZIONE_PIANTA' : Details.DESCRIZIONE_PIANTA,
            'ID_STANZA' : Details.ID_STANZA,
            'NOME_STANZA' : Room.NOME_STANZA,
            'POSIZIONE_STANZA_X' : Details.POSIZIONE_STANZA_X,
            'POSIZIONE_STANZA_Y' : Details.POSIZIONE_STANZA_Y,
            'UMIDITA_CORRENTE' : SensorsDetails.UMIDITA_CORRENTE,
            'ACQUA_ULTIMA_INNAFFIATURA' : SensorsDetails.ACQUA_ULTIMA_INNAFFIATURA,
            'ALTRO_DATO_SENSORI_1' : SensorsDetails.ALTRO_DATO_SENSORI_1,
            'ALTRO_DATO_SENSORI_2' : SensorsDetails.ALTRO_DATO_SENSORI_2,
            'ALTRO_DATO_SENSORI_3' : SensorsDetails.ALTRO_DATO_SENSORI_3,
            'ALTRO_DATO_SENSORI_4' : SensorsDetails.ALTRO_DATO_SENSORI_4
        }


        
        # fields to be returned can be chosen both if ID is None or populated
        fields = request.args.get('fields', default=None, type=str)
        queryFields = []

        if fields is not None:
            # get the fields list from the REST API invoke and associate them with the ones in the map
            requestedFields = {field.strip() for field in fields.split(',') if field.strip()}
            schemaFields = ActPianteSchema().fields

            for schema_field in schemaFields:
                if schema_field in requestedFields:
                    queryFields.append(schema_field)

                nested_fields = [f for f in requestedFields if CONST_FIELDS_ATTRIBUTE_FIELDS_MAP.get(f) == schema_field]
                if nested_fields:
                    queryFields.extend(f"{schema_field}.{f}" for f in nested_fields)



        # if ID does not exist, get all plants
        if plantID is None:
            try:

                page = request.args.get('page', default=1, type=int)
                limit = request.args.get('limit', default=25, type=int)
                orderBy = request.args.get('orderBy', default='DATA_ULTIMA_MODIFICA:desc', type=str).split(':')


                if page < 1:
                    return {"message": "La pagina deve essere un valore positivo"}, 400
                if limit < 1 or limit > 100:
                    return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
                if not CONST_ALL_ALIASED_FIELDS.get(orderBy[0]):
                    return {"message": "L'attributo di ordinamento contiene un campo non valido"}, 400

                
                
                plants = ActPianteTestataModel.query\
                            .join(Details, ActPianteTestataModel.dettaglio, isouter=True)\
                            .join(Room, Details.stanza, isouter=True)\
                            .join(SensorsDetails, ActPianteTestataModel.dettaglioSensori, isouter=True)\
                            .join(Status, ActPianteTestataModel.status, isouter=True)\
                            .join(Schedule, ActPianteTestataModel.schedule, isouter=True)\
                            .options(
                                contains_eager(ActPianteTestataModel.dettaglio, alias=Details),
                                contains_eager(ActPianteTestataModel.dettaglio, ActPianteDettaglioModel.stanza, alias=Room),
                                contains_eager(ActPianteTestataModel.dettaglioSensori, alias=SensorsDetails),
                                contains_eager(ActPianteTestataModel.status, alias=Status),
                                contains_eager(ActPianteTestataModel.schedule, alias=Schedule)
                            )\
                            .order_by(CONST_ALL_ALIASED_FIELDS.get(orderBy[0]).desc() if orderBy[1].lower() == 'desc' else CONST_ALL_ALIASED_FIELDS.get(orderBy[0]).asc())
                

                pagination = plants.paginate(page=page, per_page=limit, error_out=False)
                # get only fields specified in the queryFields list from the schema or all fields
                schema = ActPianteSchema(many=True, only=queryFields if queryFields else None)
                plantsArray = pagination.items
                totalItems = pagination.total
                totalPages = pagination.pages
                hasMore = pagination.has_next
                return {
                    "piante": schema.dump(plantsArray),
                    "count": len(plantsArray),
                    "hasMore": hasMore,
                    "page": page,
                    "limit": limit,
                    "totalPages": totalPages,
                    "totalItems": totalItems
                }, 200
            except SQLAlchemyError as e:
                return {"message": "Errore durante il recupero delle piante"}, 500



        # else if ID is not null, get the one plant corresponding to the ID
        try:
            # query construction:
            #   filter shows the only plant with the ID specified in the path
            plant = ActPianteTestataModel.query\
                        .options(joinedload(ActPianteTestataModel.dettaglio).joinedload(ActPianteDettaglioModel.stanza))\
                        .options(joinedload(ActPianteTestataModel.dettaglioSensori))\
                        .options(joinedload(ActPianteTestataModel.status))\
                        .options(joinedload(ActPianteTestataModel.schedule))\
                        .filter(ActPianteTestataModel.ID_PIANTA == plantID)\
                        .first()
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero della pianta"}, 500

        # if the plant has been successfully retrieved from the DB
        if plant:
            schema = ActPianteSchema(only=queryFields if queryFields else None)
            return schema.dump(plant), 200

        # else return 404 error, plant not found
        return {"message": "Pianta non trovata"}, 404
    


    # plant creation is implemented with multipart form-data
    def post(self):

        # get JSON request payload with all fields except for the photo
        try:
            requestPayload = request.form.get('payload')
            jsonRequestPayload = json.loads(requestPayload)
        except Exception:
            return {"message": "Errore durante il recupero dei dati da salvare"}, 400
        

        # check if room ID is specified if at least one position is populated
        if ((jsonRequestPayload.get('POSIZIONE_STANZA_X') is not None or jsonRequestPayload.get('POSIZIONE_STANZA_Y') is not None)
                and jsonRequestPayload.get('ID_STANZA') is None):
            return {"message": "E' necessario specificare una stanza per impostare la posizione della pianta."}, 400
        

        # check if both positions are set if at least one is specified
        if ((jsonRequestPayload.get('POSIZIONE_STANZA_X') is not None and jsonRequestPayload.get('POSIZIONE_STANZA_Y') is None)
                or (jsonRequestPayload.get('POSIZIONE_STANZA_X') is None and jsonRequestPayload.get('POSIZIONE_STANZA_Y') is not None)):
            return {"message": "E' necessario specificare entrambe le coordinate nella stanza."}, 400


        
        # get room info to check if specified coordinates are within room's dimensions
        if jsonRequestPayload.get('ID_STANZA') is not None:
            
            room = LookupStanzeModel.query.get(jsonRequestPayload.get('ID_STANZA'))

            if not room:
                return {"message": "La stanza specificata non esiste."}, 400
            
            if (jsonRequestPayload.get('POSIZIONE_STANZA_X') is not None and jsonRequestPayload.get('POSIZIONE_STANZA_Y') is not None):
                # plant coordinates are specified
                if jsonRequestPayload.get('POSIZIONE_STANZA_X') < 0 or jsonRequestPayload.get('POSIZIONE_STANZA_X') > room.DIMENSIONE_GRIGLIA_X:
                    return {"message": "La coordinata X indicata non è valida per la stanza specificata."}, 400
                elif jsonRequestPayload.get('POSIZIONE_STANZA_Y') < 0 or jsonRequestPayload.get('POSIZIONE_STANZA_Y') > room.DIMENSIONE_GRIGLIA_Y:
                    return {"message": "La coordinata Y indicata non è valida per la stanza specificata."}, 400
        


        # get plants to check if specified coordinates are free
        if jsonRequestPayload.get('ID_STANZA') is not None\
            and jsonRequestPayload.get('POSIZIONE_STANZA_X') is not None\
            and jsonRequestPayload.get('POSIZIONE_STANZA_Y') is not None:

            try:
                # define aliases for related tables in order to make joins
                Details = aliased(ActPianteDettaglioModel)
                SensorsDetails = aliased(ActPianteDettaglioSensoriModel)
                Room = aliased(LookupStanzeModel)
                Status = aliased(LookupStatiModel)
                Schedule = aliased(LookupProgrammiModel)

                plantsWithSpecifiedPosition = ActPianteTestataModel.query\
                                                .join(Details, ActPianteTestataModel.dettaglio, isouter=True)\
                                                .join(Room, Details.stanza, isouter=True)\
                                                .join(SensorsDetails, ActPianteTestataModel.dettaglioSensori, isouter=True)\
                                                .join(Status, ActPianteTestataModel.status, isouter=True)\
                                                .join(Schedule, ActPianteTestataModel.schedule, isouter=True)\
                                                .options(
                                                    contains_eager(ActPianteTestataModel.dettaglio, alias=Details),
                                                    contains_eager(ActPianteTestataModel.dettaglio, ActPianteDettaglioModel.stanza, alias=Room),
                                                    contains_eager(ActPianteTestataModel.dettaglioSensori, alias=SensorsDetails),
                                                    contains_eager(ActPianteTestataModel.status, alias=Status),
                                                    contains_eager(ActPianteTestataModel.schedule, alias=Schedule)
                                                )\
                                                .filter(Details.ID_STANZA == jsonRequestPayload.get('ID_STANZA'),
                                                        Details.POSIZIONE_STANZA_X == jsonRequestPayload.get('POSIZIONE_STANZA_X'),
                                                        Details.POSIZIONE_STANZA_Y == jsonRequestPayload.get('POSIZIONE_STANZA_Y'))\
                                                .first()
            except SQLAlchemyError:
                return {"message": "Errore durante i controlli preliminari"}, 500

            # if the plant with specified positions has been successfully retrieved from the DB
            if plantsWithSpecifiedPosition is not None:
                return {"message": "La posizione indicata per la pianta è già occupata."}, 400



        # get the photo's bytes from the file attachment in the multipart form-data request
        photoBytes = None
        photoFile = request.files.get('image')
        if photoFile:
            try:
                photoBytes = photoFile.read()
            except Exception:
                return {"message": "Errore durante il recupero della foto da salvare"}, 400


        # create a new plant with JSON request payload's data
        newPlant = ActPianteTestataModel(
            ID_STATO_PIANTA=jsonRequestPayload.get('ID_STATO_PIANTA'),
            ID_ULTIMO_PROGRAMMA_ESEGUITO=jsonRequestPayload.get('ID_ULTIMO_PROGRAMMA_ESEGUITO'),
        )
        
        # create a new model for plant details, because it does not exist in the database yet
        newPlant.dettaglio = ActPianteDettaglioModel(
            NOME_PIANTA=jsonRequestPayload.get('NOME_PIANTA'),
            DESCRIZIONE_PIANTA=jsonRequestPayload.get('DESCRIZIONE_PIANTA'),
            FOTO_PIANTA=photoBytes,
            ID_STANZA=jsonRequestPayload.get('ID_STANZA'),
            POSIZIONE_STANZA_X=jsonRequestPayload.get('POSIZIONE_STANZA_X'),
            POSIZIONE_STANZA_Y=jsonRequestPayload.get('POSIZIONE_STANZA_Y')
        )


        try:
            db.session.add(newPlant)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione della pianta"}, 500
        
        # get the created plant
        entirePlant = ActPianteTestataModel.query\
                        .options(joinedload(ActPianteTestataModel.dettaglio).joinedload(ActPianteDettaglioModel.stanza))\
                        .options(joinedload(ActPianteTestataModel.status))\
                        .options(joinedload(ActPianteTestataModel.schedule))\
                        .filter(ActPianteTestataModel.ID_PIANTA == newPlant.ID_PIANTA)\
                        .first()

        return one_plant_schema.dump(entirePlant), 201



    # plant update is implemented with multipart form-data
    def patch(self, plantID):


        headerFields = {
            'ID_STATO_PIANTA',
            'ID_ULTIMO_PROGRAMMA_ESEGUITO'
        }

        detailsFields = {
            'NOME_PIANTA',
            'DESCRIZIONE_PIANTA',
            'ID_STANZA',
            'POSIZIONE_STANZA_X',
            'POSIZIONE_STANZA_Y'
        }

        sensorsDetailsFields = {
            'UMIDITA_CORRENTE',
            'ACQUA_ULTIMA_INNAFFIATURA',
            'ALTRO_DATO_SENSORI_1',
            'ALTRO_DATO_SENSORI_2',
            'ALTRO_DATO_SENSORI_3',
            'ALTRO_DATO_SENSORI_4'
        }

        
        # get the one plant from the DB with the corresponding ID
        plant = ActPianteTestataModel.query.get(plantID)

        # if the ID is not found in the DB, return 404 error, plant not found
        if not plant:
            return {"message": "Pianta non trovata"}, 404
        

        # get JSON payload with all fields to be updated except for the photo
        jsonRequestPayload=None
        try:
            requestPayload = request.form.get('payload')
            if requestPayload is not None:
                jsonRequestPayload = json.loads(requestPayload)
        except Exception:
            return {"message": "Errore durante il recupero dei dati da salvare"}, 400
        

        # check if room ID is specified if at least one position is populated
        if ((jsonRequestPayload.get('POSIZIONE_STANZA_X') is not None or jsonRequestPayload.get('POSIZIONE_STANZA_Y') is not None)
                and jsonRequestPayload.get('ID_STANZA') is None):
            return {"message": "E' necessario specificare una stanza per impostare la posizione della pianta."}, 400
        

        # check if both positions are set if at least one is specified
        if ((jsonRequestPayload.get('POSIZIONE_STANZA_X') is not None and jsonRequestPayload.get('POSIZIONE_STANZA_Y') is None)
                or (jsonRequestPayload.get('POSIZIONE_STANZA_X') is None and jsonRequestPayload.get('POSIZIONE_STANZA_Y') is not None)):
            return {"message": "E' necessario specificare entrambe le coordinate nella stanza."}, 400


        
        # get room info to check if specified coordinates are within room's dimensions
        if jsonRequestPayload.get('ID_STANZA') is not None:
            
            room = LookupStanzeModel.query.get(jsonRequestPayload.get('ID_STANZA'))

            if not room:
                return {"message": "La stanza specificata non esiste."}, 400
            
            if (jsonRequestPayload.get('POSIZIONE_STANZA_X') is not None and jsonRequestPayload.get('POSIZIONE_STANZA_Y') is not None):
                # plant coordinates are specified
                if jsonRequestPayload.get('POSIZIONE_STANZA_X') < 0 or jsonRequestPayload.get('POSIZIONE_STANZA_X') > room.DIMENSIONE_GRIGLIA_X:
                    return {"message": "La coordinata X indicata non è valida per la stanza specificata."}, 400
                elif jsonRequestPayload.get('POSIZIONE_STANZA_Y') < 0 or jsonRequestPayload.get('POSIZIONE_STANZA_Y') > room.DIMENSIONE_GRIGLIA_Y:
                    return {"message": "La coordinata Y indicata non è valida per la stanza specificata."}, 400
        


        # get plants to check if specified coordinates are free
        if jsonRequestPayload.get('ID_STANZA') is not None\
            and jsonRequestPayload.get('POSIZIONE_STANZA_X') is not None\
            and jsonRequestPayload.get('POSIZIONE_STANZA_Y') is not None:

            try:
                # define aliases for related tables in order to make joins
                Details = aliased(ActPianteDettaglioModel)
                SensorsDetails = aliased(ActPianteDettaglioSensoriModel)
                Room = aliased(LookupStanzeModel)
                Status = aliased(LookupStatiModel)
                Schedule = aliased(LookupProgrammiModel)

                plantsWithSpecifiedPosition = ActPianteTestataModel.query\
                                                .join(Details, ActPianteTestataModel.dettaglio, isouter=True)\
                                                .join(Room, Details.stanza, isouter=True)\
                                                .join(SensorsDetails, ActPianteTestataModel.dettaglioSensori, isouter=True)\
                                                .join(Status, ActPianteTestataModel.status, isouter=True)\
                                                .join(Schedule, ActPianteTestataModel.schedule, isouter=True)\
                                                .options(
                                                    contains_eager(ActPianteTestataModel.dettaglio, alias=Details),
                                                    contains_eager(ActPianteTestataModel.dettaglio, ActPianteDettaglioModel.stanza, alias=Room),
                                                    contains_eager(ActPianteTestataModel.dettaglioSensori, alias=SensorsDetails),
                                                    contains_eager(ActPianteTestataModel.status, alias=Status),
                                                    contains_eager(ActPianteTestataModel.schedule, alias=Schedule)
                                                )\
                                                .filter(Details.ID_STANZA == jsonRequestPayload.get('ID_STANZA'),
                                                        Details.POSIZIONE_STANZA_X == jsonRequestPayload.get('POSIZIONE_STANZA_X'),
                                                        Details.POSIZIONE_STANZA_Y == jsonRequestPayload.get('POSIZIONE_STANZA_Y'))\
                                                .first()
            except SQLAlchemyError:
                return {"message": "Errore durante i controlli preliminari"}, 500

            # if the plant with specified positions has been successfully retrieved from the DB
            if plantsWithSpecifiedPosition is not None:
                return {"message": "La posizione indicata per la pianta è già occupata."}, 400
            


        # get the photo's bytes from the file attachment in the multipart form-data request
        photoBytes = None
        photoFile = request.files.get('image')
        if photoFile:
            try:
                photoBytes = photoFile.read()
            except Exception:
                return {"message": "Errore durante il recupero della foto da salvare"}, 400

        

        validFields=None
        try:

            headerJsonPayload = {}
            detailsJsonPayload = {}
            sensorsDetailsJsonPayload = {}
            
            for key, value in jsonRequestPayload.items():
                if key in headerFields:
                    headerJsonPayload[key] = value
                elif key in detailsFields:
                    detailsJsonPayload[key] = value
                elif key in sensorsDetailsFields:
                    sensorsDetailsJsonPayload[key] = value
            

            # marshmallow format payload, separating header, details and sensors details
            marshmallowPayload = dict(headerJsonPayload)
            if detailsJsonPayload:
                marshmallowPayload['dettaglio'] = detailsJsonPayload
            if sensorsDetailsJsonPayload:
                marshmallowPayload['dettaglioSensori'] = sensorsDetailsJsonPayload
            

            # load method returnes a dictionary with all the valid fields
            #   if a field has a wrong data type or does not exist on DB table, it throws a ValidationError
            #   partial=True allows to accept a JSON request payload with only a subset of fields
            if marshmallowPayload is not None:
                validFields = one_plant_schema.load(marshmallowPayload, partial=True)
        except ValidationError as err:
            return {"message": "I valori inseriti per la modifica della pianta non sono validi"}, 400
        
        
        
        # scroll the validFields dictionary
        #   key contains the header table's field or the table itself, like "dettaglio" and "dettaglioSensori"
        #   value contains the corresponding value or the json payload with all the fields of the current table
        if validFields:
            for key, value in validFields.items():
                # if current table is the header table, key will be the specific field
                #   details and sensorsDetails are dictionaries, while the header only contains strings
                #   isinstance returnes True if the value is a dictionary, False otherwise
                if not isinstance(value, dict):
                    setattr(plant, key, value)
                else:
                    # get the relationship between header plant and its details
                    plantRelationship = getattr(plant, key)
                    # when the key is "dettaglioSensori" the relationship might not exist
                    #   because it's not created during the plant creation
                    if key == 'dettaglioSensori' and plantRelationship is None:
                        try:
                            # initialize the relationship between header plant and sensors details
                            # --all fields need to be specified, but if any key isn't updated through the payload, it will be set to None
                            plantRelationship = ActPianteDettaglioSensoriModel(
                                UMIDITA_CORRENTE=validFields['dettaglioSensori']['UMIDITA_CORRENTE'] if 'UMIDITA_CORRENTE' in validFields['dettaglioSensori'].keys() else None,
                                ACQUA_ULTIMA_INNAFFIATURA=validFields['dettaglioSensori']['ACQUA_ULTIMA_INNAFFIATURA'] if 'ACQUA_ULTIMA_INNAFFIATURA' in validFields['dettaglioSensori'].keys() else None,
                                ALTRO_DATO_SENSORI_1=validFields['dettaglioSensori']['ALTRO_DATO_SENSORI_1'] if 'ALTRO_DATO_SENSORI_1' in validFields['dettaglioSensori'].keys() else None,
                                ALTRO_DATO_SENSORI_2=validFields['dettaglioSensori']['ALTRO_DATO_SENSORI_2'] if 'ALTRO_DATO_SENSORI_2' in validFields['dettaglioSensori'].keys() else None,
                                ALTRO_DATO_SENSORI_3=validFields['dettaglioSensori']['ALTRO_DATO_SENSORI_3'] if 'ALTRO_DATO_SENSORI_3' in validFields['dettaglioSensori'].keys() else None,
                                ALTRO_DATO_SENSORI_4=validFields['dettaglioSensori']['ALTRO_DATO_SENSORI_4'] if 'ALTRO_DATO_SENSORI_4' in validFields['dettaglioSensori'].keys() else None
                            )
                            plant.dettaglioSensori = plantRelationship
                            db.session.add(plantRelationship)
                        except SQLAlchemyError:
                            db.session.rollback()
                            return {"message": "Errore durante l'aggiornamento dei dati dei sensori"}, 500
                    # scroll the json request payload for the current table
                    for t_key, t_value in value.items():
                        setattr(plantRelationship, t_key, t_value)
        

        try:
            if photoBytes is not None:
                plant.dettaglio.FOTO_PIANTA = photoBytes
            plant.DATA_ULTIMA_MODIFICA = datetime.datetime.now()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante l'aggiornamento della pianta"}, 500
        
        # get the updated plant
        entirePlant = ActPianteTestataModel.query\
                            .options(joinedload(ActPianteTestataModel.dettaglio).joinedload(ActPianteDettaglioModel.stanza))\
                            .options(joinedload(ActPianteTestataModel.dettaglioSensori))\
                            .options(joinedload(ActPianteTestataModel.status))\
                            .options(joinedload(ActPianteTestataModel.schedule))\
                            .filter(ActPianteTestataModel.ID_PIANTA == plantID)\
                            .first()

        return one_plant_schema.dump(entirePlant), 200
    


    def delete(self, plantID):

        # get the one plant from the DB with the corresponding ID
        plant = ActPianteTestataModel.query.get(plantID)

        # if the ID is not found in the DB, return 404 error, plant not found
        if not plant:
            return {"message": "Pianta non trovata"}, 404

        # else delete the plant from the DB
        try:
            db.session.delete(plant)
            db.session.commit()
            return {"message": "Pianta eliminata"}, 204
        except SQLAlchemyError as err:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione della pianta"}, 500





class ActFotoPianteResource(Resource):



    def get(self, plantID=None):

        
        # if ID does not exists, get all plants' photo
        if plantID is None:

            idListString = request.args.get('filter', default="", type=str)
            
            # make a list from IDs concatenation
            idList = [s.strip() for s in idListString.split(',') if s.strip()]
            if not idList:
                return {"message": "E' necessario specificare gli ID delle piante"}, 400
            

            try:
                # get ID and photo from the plants whose IDs have been specified
                plants = ActPianteTestataModel.query\
                    .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                    .with_entities(*photo_fields)\
                    .filter(ActPianteTestataModel.ID_PIANTA.in_(idList))\
                    .all()
            except SQLAlchemyError:
                return {"message": "Errore durante il recupero delle foto delle piante"}, 500
            

            # create a map with plant's ID as key and the photo as value
            plantsMap = {pianta.ID_PIANTA: pianta.FOTO_PIANTA for pianta in plants}

            # create a memory buffer to contain the zip file
            buffer = io.BytesIO()
            # the with clause opens and automatically closes the resource
            #   it opens up the file on write mode and with deflated compression
            with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zipFile:
                for singleID in idList:
                    photo = plantsMap.get(singleID)
                    if photo:
                        # open up the single image to get its format
                        extension = Image.open(io.BytesIO(photo)).format.lower()
                        zipFile.writestr(f"{singleID}.{extension}", photo)
                    else:
                        zipFile.writestr(f"{singleID}_missing.txt", f"Foto non trovata per ID {singleID}")
            
            # get the cursor to the beginning of the buffer to read it
            buffer.seek(0)
            # get the bytes of the zip file
            zipBytes = buffer.getvalue()
            # download the file with photos.zip name
            headers = {"Content-Disposition": 'attachment; filename="photos.zip"'}


            return Response(zipBytes, mimetype="application/zip", headers=headers)
            


        # else if ID is not null, get the one plant corresponding to the ID
        try:

            # query construction:
            #   with_entities filters the query showing only the fields specified in the fields array
            #   filter shows the only plant with the ID specified in the path
            plant = ActPianteTestataModel.query\
                        .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                        .with_entities(*photo_fields)\
                        .filter(ActPianteTestataModel.ID_PIANTA == plantID)\
                        .first()
            
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero della pianta"}, 500
        

        # if the plant has been successfully retrieved from the DB, returnes its photo
        if plant:
            photoPlant = plant.FOTO_PIANTA

            if photoPlant:
                extension = Image.open(io.BytesIO(photoPlant)).format.lower()
                headers = {"Content-Disposition": 'attachment; filename="' + plant.ID_PIANTA + '.' + extension + '"'}
                
                return Response(photoPlant, mimetype='image/' + extension, headers=headers)
            
            else:
                return {"message": "La pianta non ha una foto"}, 200

        # else return 404 error, plant not found
        return {"message": "Pianta non trovata"}, 404
    


    def delete(self, plantID):

        plant = ActPianteTestataModel.query.get(plantID)
        plantDetail = ActPianteDettaglioModel.query.get(plantID)

        if not plant:
            return {"message": "Pianta non trovata"}, 404

        # else delete the plant's photo from the DB
        try:
            plant.DATA_ULTIMA_MODIFICA = datetime.datetime.now()
            plantDetail.FOTO_PIANTA = None
            db.session.commit()
            return {"message": "Foto eliminata"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante l'eliminazione della foto della pianta"}, 500