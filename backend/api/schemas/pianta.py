from marshmallow import Schema, fields, validate



class ActPianteDettaglioSchema(Schema):
    # define schema for plants details table

    NOME_PIANTA = fields.Str() # attribute='dettaglio.NOME_PIANTA'
    DESCRIZIONE_PIANTA = fields.Str(validate=validate.Length(max=65535)) # attribute='dettaglio.DESCRIZIONE_PIANTA', 
    ID_STANZA = fields.Str() # attribute='dettaglio.ID_STANZA'
    NOME_STANZA = fields.Str(attribute='room.NOME_STANZA')
    POSIZIONE_STANZA_X = fields.Int() # attribute='dettaglio.POSIZIONE_STANZA_X'
    POSIZIONE_STANZA_Y = fields.Int() # attribute='dettaglio.POSIZIONE_STANZA_Y'



class ActPianteDettaglioSensoriSchema(Schema):
    # define schema for plants sensors details table

    UMIDITA_CORRENTE = fields.Int() # attribute='dettaglio_sensori.UMIDITA_CORRENTE'
    ACQUA_ULTIMA_INNAFFIATURA = fields.Int() # attribute='dettaglio_sensori.ACQUA_ULTIMA_INNAFFIATURA'
    ALTRO_DATO_SENSORI_1 = fields.Decimal(as_string=True, places=2) # attribute='dettaglio_sensori.ALTRO_DATO_SENSORI_1', 
    ALTRO_DATO_SENSORI_2 = fields.Decimal(as_string=True, places=2) # attribute='dettaglio_sensori.ALTRO_DATO_SENSORI_2', 
    ALTRO_DATO_SENSORI_3 = fields.Decimal(as_string=True, places=2) # attribute='dettaglio_sensori.ALTRO_DATO_SENSORI_3', 
    ALTRO_DATO_SENSORI_4 = fields.Decimal(as_string=True, places=2) # attribute='dettaglio_sensori.ALTRO_DATO_SENSORI_4', 



class ActPianteSchema(Schema):
    # define schema for plants header table

    ID_PIANTA = fields.Str()
    
    ID_STATO_PIANTA = fields.Str()
    NOME_STATO = fields.Str(attribute='status.NOME_STATO')
    DESCRIZIONE_STATO = fields.Str(attribute='status.DESCRIZIONE_STATO')

    ID_ULTIMO_PROGRAMMA_ESEGUITO = fields.Str()
    NOME_PROGRAMMA = fields.Str(attribute='schedule.NOME_PROGRAMMA')
    ORARIO_INIZIO_PROGRAMMA = fields.Time(attribute='schedule.ORARIO_INIZIO_PROGRAMMA')
    ORARIO_FINE_PROGRAMMA = fields.Time(attribute='schedule.ORARIO_FINE_PROGRAMMA')

    dettaglio = fields.Nested(ActPianteDettaglioSchema)
    dettaglioSensori = fields.Nested(
        ActPianteDettaglioSensoriSchema,
        attribute='dettaglioSensori',
        allow_none=True
    )

    DATA_ULTIMA_MODIFICA = fields.DateTime()
    DATA_INSERIMENTO = fields.DateTime()



class ActFotoPianteSchema(Schema):
    FOTO_PIANTA = fields.Str()




""" from marshmallow import Schema, fields, validate, pre_dump



class ActPianteSchema(Schema):
    # define schema for plants table
    ID_PIANTA = fields.Str()
    NOME_PIANTA = fields.Str(attribute='dettaglio.NOME_PIANTA')
    DESCRIZIONE_PIANTA = fields.Str(attribute='dettaglio.DESCRIZIONE_PIANTA', validate=validate.Length(max=65535))
    ID_STATO_PIANTA = fields.Str()
    NOME_STATO = fields.Str(attribute='stato.NOME_STATO')
    DESCRIZIONE_STATO = fields.Str(attribute='stato.DESCRIZIONE_STATO')
    ID_STANZA = fields.Str(attribute='dettaglio.ID_STANZA')
    NOME_STANZA = fields.Str(attribute='stanza.NOME_STANZA')
    POSIZIONE_STANZA_X = fields.Int(attribute='dettaglio.POSIZIONE_STANZA_X')
    POSIZIONE_STANZA_Y = fields.Int(attribute='dettaglio.POSIZIONE_STANZA_Y')
    ID_ULTIMO_PROGRAMMA_ESEGUITO = fields.Str()
    NOME_PROGRAMMA = fields.Str(attribute='programma.NOME_PROGRAMMA')
    ORARIO_INIZIO_PROGRAMMA = fields.Time(attribute='programma.ORARIO_INIZIO_PROGRAMMA')
    ORARIO_FINE_PROGRAMMA = fields.Time(attribute='programma.ORARIO_FINE_PROGRAMMA')
    UMIDITA_CORRENTE = fields.Int(attribute='dettaglio_sensori.UMIDITA_CORRENTE')
    ACQUA_ULTIMA_INNAFFIATURA = fields.Int(attribute='dettaglio_sensori.ACQUA_ULTIMA_INNAFFIATURA')
    ALTRO_DATO_SENSORI_1 = fields.Decimal(attribute='dettaglio_sensori.ALTRO_DATO_SENSORI_1', as_string=True, places=2)
    ALTRO_DATO_SENSORI_2 = fields.Decimal(attribute='dettaglio_sensori.ALTRO_DATO_SENSORI_2', as_string=True, places=2)
    ALTRO_DATO_SENSORI_3 = fields.Decimal(attribute='dettaglio_sensori.ALTRO_DATO_SENSORI_3', as_string=True, places=2)
    ALTRO_DATO_SENSORI_4 = fields.Decimal(attribute='dettaglio_sensori.ALTRO_DATO_SENSORI_4', as_string=True, places=2)
    DATA_ULTIMA_MODIFICA = fields.DateTime()
    DATA_INSERIMENTO = fields.DateTime()


    # get each row from KeyedTuple and transforms it into a dictionary
    #   pass_many means that the function can receive both objects and lists
    @pre_dump(pass_many=True)
    def _normalize_mapping(self, data, many):

        # called for each row
        def from_row_to_dict(row):
            # check if the current row is a KeyedTuple or a dictionary
            #   if the object is already a ORM, the row is returned as it is
            rowObject = row._mapping if hasattr(row, '_mapping') else (row if isinstance(row, dict) else None)

            if rowObject is None:
                return row
            
            outObject = {}
            # for each field of the schema
            for fieldName, field in self.fields.items():
                # find the corresponding attribute in the schema
                schemaAttribute = field.attribute or fieldName
                # it might contain a dot
                #   if so, it splits the name in the entity and its field
                #   otherwise, the entity is None and the field is the attribute itself
                entity, field = schemaAttribute.split('.', 1) if '.' in schemaAttribute else (None, schemaAttribute)
                # if entity exists, the key will be the field, otherwise the attribute
                key = field if entity else schemaAttribute
                # if the key is contained inside the mapping (fields to be returned)
                #   the value will be the one corresponding to the key
                #   otherwise the field will not be shown in the response payload
                if key in rowObject:
                    value = rowObject[key]
                    if entity:
                        outObject.setdefault(entity, {})[field] = value
                    else:
                        outObject[schemaAttribute] = value
            
            return outObject
        
        return [from_row_to_dict(row) for row in data] if many else from_row_to_dict(data)



class ActFotoPianteSchema(Schema):
    FOTO_PIANTA = fields.Str() """