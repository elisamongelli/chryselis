from marshmallow import Schema, fields, pre_dump



class ActPianteStoricoSchema(Schema):
    # define schema from plants history table
    ID_PIANTA = fields.Str()
    ID_STATO_PIANTA = fields.Str()
    NOME_STATO = fields.Str(attribute='stato.NOME_STATO')
    DESCRIZIONE_STATO = fields.Str(attribute='stato.DESCRIZIONE_STATO')
    ID_PROGRAMMA_ESEGUITO = fields.Str()
    NOME_PROGRAMMA = fields.Str(attribute='programma.NOME_PROGRAMMA')
    ORARIO_INIZIO_PROGRAMMA = fields.Time(attribute='programma.ORARIO_INIZIO_PROGRAMMA')
    ORARIO_FINE_PROGRAMMA = fields.Time(attribute='programma.ORARIO_FINE_PROGRAMMA')
    UMIDITA_CORRENTE = fields.Int()
    ACQUA_ULTIMA_INNAFFIATURA = fields.Int()
    ALTRO_DATO_SENSORI_1 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_2 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_3 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_4 = fields.Decimal(as_string=True, places=2)
    DATA_MODIFICA = fields.DateTime()



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