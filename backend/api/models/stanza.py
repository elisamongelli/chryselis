from api.models import db
import uuid



class LookupStanzeModel(db.Model):

    __tablename__ = 'lkp_stanze'

    ID_STANZA = db.Column(db.String(100), primary_key=True)
    NOME_STANZA = db.Column(db.String(500))
    DIMENSIONE_GRIGLIA_X = db.Column(db.Integer)
    DIMENSIONE_GRIGLIA_Y = db.Column(db.Integer)


    def __init__(self, NOME_STANZA, DIMENSIONE_GRIGLIA_X, DIMENSIONE_GRIGLIA_Y, ID_STANZA=None):
        # if no ID is provided, it generates a new UUID from Python to avoid INSERT errors without a default
        self.ID_STANZA = ID_STANZA or str(uuid.uuid4())
        self.NOME_STANZA = NOME_STANZA
        self.DIMENSIONE_GRIGLIA_X = DIMENSIONE_GRIGLIA_X
        self.DIMENSIONE_GRIGLIA_Y = DIMENSIONE_GRIGLIA_Y
    

    def __repr__(self):
        return f'<id {self.ID_STANZA}>'