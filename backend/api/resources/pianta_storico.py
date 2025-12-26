import datetime
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from api.models import db
from api.models.pianta_storico import ActPianteStoricoModel
from api.models.pianta import ActPianteTestataModel, ActPianteDettaglioSensoriModel
from api.models.stato import LookupStatiModel
from api.models.programma import LookupProgrammiModel
from api.schemas.pianta_storico import ActPianteStoricoSchema




many_piante_storico_schema = ActPianteStoricoSchema(many=True)
one_piante_storico_schema = ActPianteStoricoSchema()



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
                            ActPianteStoricoModel.DATA_MODIFICA]


all_history_plant_fields_without_descriptive = [ActPianteTestataModel.ID_PIANTA,
                                                ActPianteTestataModel.ID_STATO_PIANTA,
                                                ActPianteTestataModel.ID_ULTIMO_PROGRAMMA_ESEGUITO.label('ID_PROGRAMMA_ESEGUITO'),
                                                ActPianteDettaglioSensoriModel.UMIDITA_CORRENTE,
                                                ActPianteDettaglioSensoriModel.ACQUA_ULTIMA_INNAFFIATURA,
                                                ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_1,
                                                ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_2,
                                                ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_3,
                                                ActPianteDettaglioSensoriModel.ALTRO_DATO_SENSORI_4,
                                                ActPianteTestataModel.DATA_ULTIMA_MODIFICA.label('DATA_MODIFICA')]





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



        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=25, type=int)
        orderBy = request.args.get('orderBy', default='DATA_MODIFICA:desc', type=str)

        if page < 1:
            return {"message": "La pagina deve essere un valore positivo"}, 400
        if limit < 1 or limit > 100:
            return {"message": "Il limite deve essere compreso o uguale tra 1 e 100"}, 400
        orderBy = orderBy.split(':')


        # if ID does not exists, get all history plants
        if id is None:

            try:
                
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
            query = ActPianteStoricoModel.query\
                        .join(ActPianteTestataModel, ActPianteTestataModel.ID_PIANTA == ActPianteStoricoModel.ID_PIANTA)\
                        .join(LookupStatiModel, LookupStatiModel.ID_STATO == ActPianteStoricoModel.ID_STATO_PIANTA)\
                        .join(LookupProgrammiModel, LookupProgrammiModel.ID_PROGRAMMA == ActPianteStoricoModel.ID_PROGRAMMA_ESEGUITO)\
                        .with_entities(*all_history_plant_fields)\
                        .filter(ActPianteStoricoModel.ID_PIANTA == id)\
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
            return {"message": "Errore durante il recupero dello storico della pianta"}, 500
    


    def post(self, id):

        if id is None:
            return {"message": "Il valore corrispondente all'ID della pianta non è specificato"}, 400

        plant_data = ActPianteTestataModel.query\
                        .join(ActPianteDettaglioSensoriModel, ActPianteDettaglioSensoriModel.ID_PIANTA == ActPianteTestataModel.ID_PIANTA)\
                        .with_entities(*all_history_plant_fields_without_descriptive)\
                        .filter(ActPianteTestataModel.ID_PIANTA == id)\
                        .first()
        

        try:
            if plant_data is not None:
                new_history_plant = ActPianteStoricoModel(
                    ID_PIANTA=plant_data.ID_PIANTA,
                    ID_STATO_PIANTA=plant_data.ID_STATO_PIANTA,
                    ID_PROGRAMMA_ESEGUITO=plant_data.ID_PROGRAMMA_ESEGUITO,
                    UMIDITA_CORRENTE=plant_data.UMIDITA_CORRENTE,
                    ACQUA_ULTIMA_INNAFFIATURA=plant_data.ACQUA_ULTIMA_INNAFFIATURA,
                    ALTRO_DATO_SENSORI_1=plant_data.ALTRO_DATO_SENSORI_1,
                    ALTRO_DATO_SENSORI_2=plant_data.ALTRO_DATO_SENSORI_2,
                    ALTRO_DATO_SENSORI_3=plant_data.ALTRO_DATO_SENSORI_3,
                    ALTRO_DATO_SENSORI_4=plant_data.ALTRO_DATO_SENSORI_4,
                    DATA_MODIFICA=plant_data.DATA_MODIFICA
                )
                db.session.add(new_history_plant)
                db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la creazione dello storico della pianta"}, 500

        return one_piante_storico_schema.dump(plant_data), 201



    def delete(self, id=None):

        # if plant ID is specified --> delete all records for that plant
        # if startDate is specified --> delete all records from the startDate
        # if endDate is specified --> delete all records until the endDate

        startDate = request.args.get('startDate', default=None, type=str)
        endDate = request.args.get('endDate', default=None, type=str)

        # checks if start date is after the end date
        if startDate is not None and endDate is not None:
            if (datetime.datetime.strptime(startDate, '%Y-%m-%d') > datetime.datetime.strptime(endDate, '%Y-%m-%d')):
                return {"message": "La data di inizio deve essere precedente alla data di fine"}, 500



        plants = None

        # get all plants without any ID filter
        if id is None:


            if startDate is not None and endDate is not None:

                try:
                    # get all plants between start date and end date
                    plants = ActPianteStoricoModel.query\
                                .filter(ActPianteStoricoModel.DATA_MODIFICA >= datetime.datetime.strptime(startDate, '%Y-%m-%d'))\
                                .filter(ActPianteStoricoModel.DATA_MODIFICA < datetime.datetime.strptime(endDate, '%Y-%m-%d') + datetime.timedelta(days=1))\
                                .order_by(ActPianteStoricoModel.DATA_MODIFICA.desc())\
                                .all()
                except:
                    return {"message": "Errore durante il recupero dello storico delle piante da eliminare"}, 500
            

            elif startDate is not None and endDate is None:

                try:
                    # get all plants after start date
                    plants = ActPianteStoricoModel.query\
                                .filter(ActPianteStoricoModel.DATA_MODIFICA >= datetime.datetime.strptime(startDate, '%Y-%m-%d'))\
                                .order_by(ActPianteStoricoModel.DATA_MODIFICA.desc())\
                                .all()
                except:
                    return {"message": "Errore durante il recupero dello storico delle piante da eliminare"}, 500
            

            elif startDate is None and endDate is not None:
                try:
                    # get all plants before end date
                    plants = ActPianteStoricoModel.query\
                                .filter(ActPianteStoricoModel.DATA_MODIFICA < datetime.datetime.strptime(endDate, '%Y-%m-%d') + datetime.timedelta(days=1))\
                                .order_by(ActPianteStoricoModel.DATA_MODIFICA.desc())\
                                .all()
                except:
                    return {"message": "Errore durante il recupero dello storico delle piante da eliminare"}, 500
            

            else:
                try:
                    # get all plants without any date filter
                    plants = ActPianteStoricoModel.query\
                                .order_by(ActPianteStoricoModel.DATA_MODIFICA.desc())\
                                .all()
                except:
                    return {"message": "Errore durante il recupero dello storico delle piante da eliminare"}, 500
        


        # get records for a specific plant
        else:


            if startDate is not None and endDate is not None:

                try:
                    # get records for plant between start date and end date
                    plants = ActPianteStoricoModel.query\
                                .filter(ActPianteStoricoModel.ID_PIANTA == id)\
                                .filter(ActPianteStoricoModel.DATA_MODIFICA >= datetime.datetime.strptime(startDate, '%Y-%m-%d'))\
                                .filter(ActPianteStoricoModel.DATA_MODIFICA < datetime.datetime.strptime(endDate, '%Y-%m-%d') + datetime.timedelta(days=1))\
                                .order_by(ActPianteStoricoModel.DATA_MODIFICA.desc())\
                                .all()
                except:
                    return {"message": "Errore durante il recupero dello storico della pianta da eliminare"}, 500
            

            elif startDate is not None and endDate is None:

                try:
                    # get records for plant after start date
                    plants = ActPianteStoricoModel.query\
                                .filter(ActPianteStoricoModel.ID_PIANTA == id)\
                                .filter(ActPianteStoricoModel.DATA_MODIFICA >= datetime.datetime.strptime(startDate, '%Y-%m-%d'))\
                                .order_by(ActPianteStoricoModel.DATA_MODIFICA.desc())\
                                .all()
                except:
                    return {"message": "Errore durante il recupero dello storico della pianta da eliminare"}, 500
            

            elif startDate is None and endDate is not None:
                try:
                    # get records for plant before end date
                    plants = ActPianteStoricoModel.query\
                                .filter(ActPianteStoricoModel.ID_PIANTA == id)\
                                .filter(ActPianteStoricoModel.DATA_MODIFICA < datetime.datetime.strptime(endDate, '%Y-%m-%d') + datetime.timedelta(days=1))\
                                .order_by(ActPianteStoricoModel.DATA_MODIFICA.desc())\
                                .all()
                except:
                    return {"message": "Errore durante il recupero dello storico della pianta da eliminare"}, 500
            

            else:
                try:
                    # get records for plant without any date filter
                    plants = ActPianteStoricoModel.query\
                                .filter(ActPianteStoricoModel.ID_PIANTA == id)\
                                .order_by(ActPianteStoricoModel.DATA_MODIFICA.desc())\
                                .all()
                except:
                    return {"message": "Errore durante il recupero dello storico della pianta da eliminare"}, 500



        try:
            for plant in plants:
                db.session.delete(plant)
            db.session.commit()
            return {"message": "Storico delle piante eliminate"}, 204
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Errore durante la cancellazione dello storico delle piante"}, 500