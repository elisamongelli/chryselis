import json, datetime, io, zipfile
from flask import request, Response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
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



all_plant_fields_without_sensors = [ActPianteTestataModel.ID_PIANTA,
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
                ActPianteDettaglioModel.FOTO_PIANTA]





class ActPianteResource(Resource):


    def get(self, plantID=None):


        # the map helps the fields attribute during REST API invoke to not write the model for each field
        fields_map = {
            'ID_PIANTA' : ActPianteTestataModel.ID_PIANTA,
            'ID_STATO_PIANTA' : ActPianteTestataModel.ID_STATO_PIANTA,
            'NOME_STATO' : LookupStatiModel.NOME_STATO,
            'DESCRIZIONE_STATO' : LookupStatiModel.DESCRIZIONE_STATO,
            'ID_ULTIMO_PROGRAMMA_ESEGUITO' : ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO,
            'NOME_PROGRAMMA' : LookupProgrammiModel.NOME_PROGRAMMA,
            'ORARIO_INIZIO_PROGRAMMA' : LookupProgrammiModel.ORARIO_INIZIO_PROGRAMMA,
            'ORARIO_FINE_PROGRAMMA' : LookupProgrammiModel.ORARIO_FINE_PROGRAMMA,
            'DATA_INSERIMENTO' : ActPianteTestataModel.DATA_INSERIMENTO,
            'DATA_ULTIMA_MODIFICA' : ActPianteTestataModel.DATA_ULTIMA_MODIFICA,
            'NOME_PIANTA' : ActPianteDettaglioModel.NOME_PIANTA,
            'DESCRIZIONE_PIANTA' : ActPianteDettaglioModel.DESCRIZIONE_PIANTA,
            'ID_STANZA' : ActPianteDettaglioModel.ID_STANZA,
            'NOME_STANZA' : LookupStanzeModel.NOME_STANZA,
            'POSIZIONE_STANZA_X' : ActPianteDettaglioModel.POSIZIONE_STANZA_X,
            'POSIZIONE_STANZA_Y' : ActPianteDettaglioModel.POSIZIONE_STANZA_Y,
            'UMIDITA_CORRENTE' : ActPianteDettaglioSensoriModel.UMIDITA_CORRENTE,
            'ACQUA_ULTIMA_INNAFFIATURA' : ActPianteDettaglioSensoriModel.ACQUA_ULTIMA_INNAFFIATURA,
            'ALTRO_DATO_SENSORI_1' : ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_1,
            'ALTRO_DATO_SENSORI_2' : ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_2,
            'ALTRO_DATO_SENSORI_3' : ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_3,
            'ALTRO_DATO_SENSORI_4' : ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_4
        }


        route_map = {
            # 'ID_PIANTA': None,
            # 'ID_STATO_PIANTA': None,
            # 'NOME_STATO': None,
            # 'DESCRIZIONE_STATO': None,
            # 'ID_ULTIMO_PROGRAMMA_ESEGUITO': None,
            # 'NOME_PROGRAMMA': None,
            # 'ORARIO_INIZIO_PROGRAMMA': None,
            # 'ORARIO_FINE_PROGRAMMA': None,
            # 'DATA_INSERIMENTO': None,
            # 'DATA_ULTIMA_MODIFICA': None,
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


        
        # fields to be returned can be chosen both if ID is None or populated
        fields = request.args.get('fields', default=None, type=str)
        filteredSchema = None
        only = []
        seen = set()
        # only = set()

        if fields is None:
            """ fields = all_plant_fields """
        else:
            # get the fields list from the REST API invoke and associate them with the ones in the map
            """ fields = [field.strip() for field in fields.split(',') if field.strip()]
            fields = [fields_map[name].label(name) for name in fields if name in fields_map] """
            """ filteredSchema = ActPianteSchema(many=True, only=fields) """
            """ fields = [field.strip() for field in fields.split(',') if field.strip()]
            # fields.add(field if fields_map.get(field) is None else [fields_map.get(field), f"{fields_map.get(field)}.{field}"] for field in fields)
            # only.update(field if (route := fields_map.get(field)) is None else [route, f"{route}.{field}"] for field in fields)
            only = {item for field in fields for item in ((field,) if route_map.get(field) is None else (route_map[field], f"{route_map[field]}.{field}"))} """
            """ for field in fields:
                route = route_map.get(field)

                if route is None:
                    only.add(field)
                else:
                    only.add(route)
                    only.add(f"{route}.{field}") """
            """ fields = [field.strip() for field in fields.split(',') if field.strip()]
            only = list(dict.fromkeys(item for field in fields for item in (
                        (field,) if route_map.get(field) is None else (route_map[field], f"{route_map[field]}.{field}"))
                    )) """
            """ fields = [field.strip() for field in fields.split(',') if field.strip()]
            nestedNeeded = set(route_map[field] for field in fields if route_map.get(field))
            only = [
                'ID_PIANTA',
                'ID_STATO_PIANTA',
                'NOME_STATO',
                'DESCRIZIONE_STATO',
                'ID_ULTIMO_PROGRAMMA_ESEGUITO',
                'NOME_PROGRAMMA',
                'ORARIO_INIZIO_PROGRAMMA',
                'ORARIO_FINE_PROGRAMMA',
                'DATA_INSERIMENTO',
                'DATA_ULTIMA_MODIFICA',
                *nestedNeeded
            ] """
            """ fields = [field.strip() for field in fields.split(',') if field.strip()]
            for field in fields:
                route = route_map.get(field)
                # nested field (from detail table or sensors detail table)
                if route is None:
                    if field not in seen:
                        only.append(field)
                        seen.add(field)

                # root field (header table field or lookup table field)
                else:
                    if route not in seen:
                        only.append(route)
                        seen.add(route)

                    only.append(f"{route}.{field}") """
            fields = [field.strip() for field in fields.split(',') if field.strip()]
            schemaFields = ActPianteSchema().fields
            for schemaField in schemaFields:
                # root field (header table field or lookup table field)
                if schemaField in fields:
                    only.append(schemaField)
                # nested field (from detail table or sensors detail table)
                for field in fields:
                    route = route_map.get(field)
                    if route == schemaField:
                        if schemaField not in only:
                            only.append(schemaField)
                        only.append(f"{schemaField}.{field}")




        # if ID does not exist, get all plants
        if plantID is None:
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
                """ plants = ActPianteTestataModel.query\
                            .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .outerjoin(ActPianteDettaglioSensoriModel, ActPianteDettaglioSensoriModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .join(LookupStatiModel, LookupStatiModel.ID_STATO == ActPianteTestataModel.ID_STATO_PIANTA)\
                            .join(LookupProgrammiModel, LookupProgrammiModel.ID_PROGRAMMA == ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO)\
                            .join(LookupStanzeModel, LookupStanzeModel.ID_STANZA == ActPianteDettaglioModel.ID_STANZA)\
                            .with_entities(*fields)\
                            .order_by(fields_map.get(orderBy[0]).desc() if orderBy[1].lower() == 'desc' else fields_map.get(orderBy[0]).asc()) """
                

                """ plants = ActPianteTestataModel.query\
                            .options(joinedload(ActPianteTestataModel.dettaglio).joinedload(ActPianteDettaglioModel.room),
                                        joinedload(ActPianteTestataModel.dettaglioSensori),
                                        joinedload(ActPianteTestataModel.status),
                                        joinedload(ActPianteTestataModel.schedule)
                            )\
                            .order_by(fields_map.get(orderBy[0]).desc() if orderBy[1].lower() == 'desc' else fields_map.get(orderBy[0]).asc()) """
                

                plants = ActPianteTestataModel.query\
                            .options(joinedload(ActPianteTestataModel.dettaglio).joinedload(ActPianteDettaglioModel.stanza))\
                            .options(joinedload(ActPianteTestataModel.dettaglioSensori))\
                            .options(joinedload(ActPianteTestataModel.status))\
                            .options(joinedload(ActPianteTestataModel.schedule))\
                            .order_by(fields_map.get(orderBy[0]).desc() if orderBy[1].lower() == 'desc' else fields_map.get(orderBy[0]).asc())
                
                
                pagination = plants.paginate(page=page, per_page=limit, error_out=False)
                schema = ActPianteSchema(
                    many=True,
                    only=only #fields.split(',') if fields else None
                )
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
                return {"message": "Errore durante il recupero delle piante - " + str(e)}, 500
        
        # else if ID is not null, get the one plant corresponding to the ID
        try:
            # query construction:
            #   with_entities filters the query showing only the fields specified in the fields array
            #   filter shows the only plant with the ID specified in the path
            plant = ActPianteTestataModel.query\
                        .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                        .outerjoin(ActPianteDettaglioSensoriModel, ActPianteDettaglioSensoriModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                        .join(LookupStatiModel, LookupStatiModel.ID_STATO == ActPianteTestataModel.ID_STATO_PIANTA)\
                        .join(LookupProgrammiModel, LookupProgrammiModel.ID_PROGRAMMA == ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO)\
                        .join(LookupStanzeModel, LookupStanzeModel.ID_STANZA == ActPianteDettaglioModel.ID_STANZA)\
                        .with_entities(*fields)\
                        .filter(ActPianteTestataModel.ID_PIANTA == plantID)\
                        .first()
        except SQLAlchemyError:
            return {"message": "Errore durante il recupero della pianta"}, 500

        # if the plant has been retrieve successfully from the DB
        if plant:
            return one_plant_schema.dump(plant), 200

        # else return 404 error, plant not found
        return {"message": "Pianta non trovata"}, 404
    


    """ # plant creation is implemented with multipart form-data
    def post(self):

        # get JSON request payload with all fields except for the photo
        try:
            requestPayload = request.form.get('payload')
            jsonRequestPayload = json.loads(requestPayload)
        except Exception:
            return {"message": "Errore durante il recupero dei dati da salvare"}, 400


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
        newPlant.detail = ActPianteDettaglioModel(
            ID_PIANTA=newPlant.ID_PIANTA,
            NOME_PIANTA=jsonRequestPayload.get('NOME_PIANTA'),
            DESCRIZIONE_PIANTA=jsonRequestPayload.get('DESCRIZIONE_PIANTA'),
            FOTO_PIANTA=photoBytes,
            ID_STANZA=jsonRequestPayload.get('ID_STANZA'),
            POSIZIONE_STANZA_X=jsonRequestPayload.get('POSIZIONE_STANZA_X'),
            POSIZIONE_STANZA_Y=jsonRequestPayload.get('POSIZIONE_STANZA_Y')
        )


        try:
            db.session.add(newPlant)
            db.session.add(newPlant.detail)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione della pianta"}, 500
        
        # get the created plant
        entirePlant = ActPianteTestataModel.query\
                        .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                        .join(LookupStatiModel, LookupStatiModel.ID_STATO == ActPianteTestataModel.ID_STATO_PIANTA)\
                        .join(LookupProgrammiModel, LookupProgrammiModel.ID_PROGRAMMA == ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO)\
                        .join(LookupStanzeModel, LookupStanzeModel.ID_STANZA == ActPianteDettaglioModel.ID_STANZA)\
                        .with_entities(*all_plant_fields_without_sensors)\
                        .filter(ActPianteTestataModel.ID_PIANTA == newPlant.ID_PIANTA)\
                        .first()

        return one_plant_schema.dump(entirePlant), 201



    def patch(self, plantID):
        
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
            # load method returnes a dictionary with all the valid fields
            #   if a field has a wrong data type or does not exist on DB table, it throws a ValidationError
            #   partial=True allows to accept a JSON request payload with only a subset of fields
            if jsonRequestPayload is not None:
                validFields = one_plant_schema.load(jsonRequestPayload, partial=True)
        except ValidationError:
            return {"message": "I valori inseriti per la modifica della pianta non sono validi"}, 400
        
        
        # set the allowed fields and update only them on DB
        allowedFields = ['NOME_PIANTA',
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
        # scroll the validFields dictionary
        #   key contains the header table's field or the table itself, like "dettaglio" and "dettaglio_sensori"
        #   value contains the corresponding value or the json payload with all the fields of the current table
        if validFields is not None:
            for key, value in validFields.items():
                # if current table is the header table, key will be the specific field
                if key in allowedFields:
                    setattr(plant, key, value)
                else:
                    # get the relationship between header plant and its details
                    plantRelationship = getattr(plant, key)
                    # when the key is "dettaglio_sensori" the relationship might not exist
                    #   because it's not created during the plant creation
                    if key == 'dettaglio_sensori' and plantRelationship is None:
                        try:
                            # initialize the relationship between header plant and sensors details
                            plantRelationship = ActPianteDettaglioSensoriModel(
                                ID_PIANTA=plantID,
                                UMIDITA_CORRENTE=None,
                                ACQUA_ULTIMA_INNAFFIATURA=None,
                                ALTRO_DATO_SENSORI_1=None,
                                ALTRO_DATO_SENSORI_2=None,
                                ALTRO_DATO_SENSORI_3=None,
                                ALTRO_DATO_SENSORI_4=None
                            )
                            plant.dettaglio_sensori = plantRelationship
                            db.session.add(plantRelationship)
                        except SQLAlchemyError:
                            db.session.rollback()
                            return {"message": "Errore durante l'aggiornamento dei dati dei sensori"}, 500
                    # scroll the json request payload for the current table
                    for t_key, t_value in value.items():
                        # if the current field is allowed, it updates its value
                        if t_key in allowedFields:
                            setattr(plantRelationship, t_key, t_value)
        

        try:
            if photoBytes is not None:
                plant.dettaglio.FOTO_PIANTA = photoBytes
            plant.DATA_ULTIMA_MODIFICA = datetime.datetime.now()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante l'aggiornamento della pianta"}, 500
        
        # gets the updated plant
        entirePlant = ActPianteTestataModel.query\
                            .join(ActPianteDettaglioModel, ActPianteDettaglioModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .outerjoin(ActPianteDettaglioSensoriModel, ActPianteDettaglioSensoriModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                            .join(LookupStatiModel, LookupStatiModel.ID_STATO == ActPianteTestataModel.ID_STATO_PIANTA)\
                            .join(LookupProgrammiModel, LookupProgrammiModel.ID_PROGRAMMA == ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO)\
                            .join(LookupStanzeModel, LookupStanzeModel.ID_STANZA == ActPianteDettaglioModel.ID_STANZA)\
                            .with_entities(*all_plant_fields)\
                            .filter(ActPianteTestataModel.ID_PIANTA == plantID)\
                            .first()

        return one_plant_schema.dump(entirePlant), 200
    


    def delete(self, plantID):

        # get the one plant from the DB with the corresponding ID
        plant = ActPianteTestataModel.query.get(plantID)
        plantDetail = ActPianteDettaglioModel.query.get(plantID)
        plantDetailSensors = ActPianteDettaglioSensoriModel.query.get(plantID)

        # if the ID is not found in the DB, return 404 error, plant not found
        if not plant:
            return {"message": "Pianta non trovata"}, 404

        # else delete the plant from the DB
        try:
            if plantDetailSensors is not None:
                db.session.delete(plantDetailSensors)
            db.session.delete(plantDetail)
            db.session.delete(plant)
            db.session.commit()
            return {"message": "Pianta eliminata"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione della pianta"}, 500 """





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