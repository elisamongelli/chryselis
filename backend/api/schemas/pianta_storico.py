from marshmallow import Schema, fields



class ActPianteStoricoSchema(Schema):
    print("Sono nella classe dello schema")
    # define schema from history plants table
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
    ALTRO_DATO_SENSORI_1 = fields.Decimal()
    ALTRO_DATO_SENSORI_2 = fields.Decimal()
    ALTRO_DATO_SENSORI_3 = fields.Decimal()
    ALTRO_DATO_SENSORI_4 = fields.Decimal()
    DATA_MODIFICA = fields.DateTime()