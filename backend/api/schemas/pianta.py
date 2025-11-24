from marshmallow import Schema, fields, validate, pre_dump
import base64



class ActPianteSchema(Schema):
    # define schema for piante table
    ID_PIANTA = fields.Str()
    NOME_PIANTA = fields.Str(attribute='dettaglio.NOME_PIANTA')
    DESCRIZIONE_PIANTA = fields.Str(attribute='dettaglio.DESCRIZIONE_PIANTA', validate=validate.Length(max=65535))
    ID_STATO_PIANTA = fields.Str()
    NOME_STATO = fields.Str(attribute='stato.NOME_STATO')
    DESCRIZIONE_STATO = fields.Str(attribute='stato.DESCRIZIONE_STATO')
    FOTO_PIANTA = fields.Str()
    ID_STANZA = fields.Str(attribute='dettaglio.ID_STANZA')
    NOME_STANZA = fields.Str(attribute='stanza.NOME_STANZA')
    POSIZIONE_STANZA_X = fields.Int(attribute='dettaglio.POSIZIONE_STANZA_X')
    POSIZIONE_STANZA_Y = fields.Int(attribute='dettaglio.POSIZIONE_STANZA_Y')
    ID_ULTIMO_PROGRAMMA_ESEGUITO = fields.Str()
    NOME_PROGRAMMA = fields.Str(attribute='programma.NOME_PROGRAMMA')
    ORARIO_INIZIO_PROGRAMMA = fields.Time(attribute='programma.ORARIO_INIZIO_PROGRAMMA')
    ORARIO_FINE_PROGRAMMA = fields.Time(attribute='programma.ORARIO_FINE_PROGRAMMA')
    UMIDITA_CORRENTE = fields.Int()
    ACQUA_ULTIMA_INNAFFIATURA = fields.Int()
    ALTRO_DATO_SENSORI_1 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_2 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_3 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_4 = fields.Decimal(as_string=True, places=2)
    DATA_INSERIMENTO = fields.DateTime()
    DATA_ULTIMA_MODIFICA = fields.DateTime()


    # gets each row from KeyedTuple and trasforms it into a dictionary
    #   pass_many argument means that the function can receive both objects and lists
    @pre_dump(pass_many=True)
    def _normalize_mapping(self, data, many):

        # called for each row
        def from_row_to_dict(row):
            # checks if the current row is a KeyedTuple or a dictionary
            #   if the object is already a ORM, the row is returned as it is
            mapping = row._mapping if hasattr(row, '_mapping') else (row if isinstance(row, dict) else None)

            if mapping is None:
                return row
            
            out = {}
            # for each field of the schema
            for fieldName, field in self.fields.items():
                # finds the corresponding attribute in the schema
                attribute = field.attribute or fieldName
                # it it contains a dot, it splits the name in the entity and its field
                entity, field = attribute.split('.', 1) if '.' in attribute else (None, attribute)
                # if entity exists, the key will be the field, otherwise the attribute itself
                key = field if entity else attribute
                # if the key is contained inside the mapping (fields to be returned)
                #   the value will be the one corresponding to the key
                #   otherwise the field will not be shown in the response payload
                if key in mapping:
                    value = mapping[key]
                    if entity:
                        out.setdefault(entity, {})[field] = value
                    else:
                        out[attribute] = value
            
            return out
        
        return [from_row_to_dict(row) for row in data] if many else from_row_to_dict(data)