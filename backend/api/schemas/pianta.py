from marshmallow import Schema, fields, validate
import base64



class ActPianteSchema(Schema):
    # define schema for piante table
    ID_PIANTA = fields.Str()
    ID_STATO_PIANTA = fields.Str()
    NOME_PIANTA = fields.Str()
    DESCRIZIONE_PIANTA = fields.Str(validate=validate.Length(max=65535))
    FOTO_PIANTA = fields.Str()
    ID_STANZA = fields.Str()
    POSIZIONE_STANZA_X = fields.Int()
    POSIZIONE_STANZA_Y = fields.Int()
    UMIDITA_CORRENTE = fields.Int()
    ACQUA_ULTIMA_INNAFFIATURA = fields.Int()
    ALTRO_DATO_SENSORI_1 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_2 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_3 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_4 = fields.Decimal(as_string=True, places=2)
    ID_ULTIMO_PROGRAMMA_ESEGUITO = fields.Str()
    DATA_INSERIMENTO = fields.DateTime()
    DATA_ULTIMA_MODIFICA = fields.DateTime()