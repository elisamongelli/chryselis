from marshmallow import Schema, fields, validate
import base64



class ActPianteSchema(Schema):
    # define schema for piante table
    ID_PIANTA = fields.Str()
    ID_STATO_PIANTA = fields.Str()
    NOME_STATO = fields.Str(attribute='stato.NOME_STATO')
    DESCRIZIONE_STATO = fields.Str(attribute='stato.DESCRIZIONE_STATO')
    NOME_PIANTA = fields.Str(attribute='dettaglio.NOME_PIANTA')
    DESCRIZIONE_PIANTA = fields.Str(attribute='dettaglio.DESCRIZIONE_PIANTA', validate=validate.Length(max=65535))
    FOTO_PIANTA = fields.Str()
    ID_STANZA = fields.Str(attribute='dettaglio.ID_STANZA')
    POSIZIONE_STANZA_X = fields.Int(attribute='dettaglio.POSIZIONE_STANZA_X')
    POSIZIONE_STANZA_Y = fields.Int(attribute='dettaglio.POSIZIONE_STANZA_Y')
    UMIDITA_CORRENTE = fields.Int()
    ACQUA_ULTIMA_INNAFFIATURA = fields.Int()
    ALTRO_DATO_SENSORI_1 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_2 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_3 = fields.Decimal(as_string=True, places=2)
    ALTRO_DATO_SENSORI_4 = fields.Decimal(as_string=True, places=2)
    ID_ULTIMO_PROGRAMMA_ESEGUITO = fields.Str()
    DATA_INSERIMENTO = fields.DateTime()
    DATA_ULTIMA_MODIFICA = fields.DateTime()