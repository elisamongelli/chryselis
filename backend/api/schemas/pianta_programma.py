from marshmallow import Schema, fields



class LookupPianteProgrammiSchema(Schema):
    # define schema for piante programmi lookup
    ID_PIANTA = fields.Str()
    ID_PROGRAMMA = fields.Str()