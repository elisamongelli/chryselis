from marshmallow import Schema, fields



class LookupProgrammiSchema(Schema):
    # define schema for schedules lookup
    ID_PROGRAMMA = fields.Str()
    VALORE_SEQUENZA_TEMPORALE_PROGRAMMA = fields.Int()
    NOME_PROGRAMMA = fields.Str()
    ORARIO_INIZIO_PROGRAMMA = fields.Time()
    ORARIO_FINE_PROGRAMMA = fields.Time()