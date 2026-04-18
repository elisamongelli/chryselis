from marshmallow import Schema, fields, validate



class LookupStatiSchema(Schema):
    # define schema for statuses lookup
    ID_STATO = fields.Str()
    NOME_STATO = fields.Str()
    DESCRIZIONE_STATO = fields.Str(validate=validate.Length(max=65535))