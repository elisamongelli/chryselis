from marshmallow import Schema, fields



class LookupStanzeSchema(Schema):
    # define schema for stanze lookup
    ID_STANZA = fields.Str()
    NOME_STANZA = fields.Str()
    DIMENSIONE_GRIGLIA_X = fields.Int()
    DIMENSIONE_GRIGLIA_Y = fields.Int()