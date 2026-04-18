from api.models import db
import uuid



class LookupProgrammiModel(db.Model):

    # specify the DB table name
    __tablename__ = 'lkp_programmi'

    # list all DB table columns
    ID_PROGRAMMA = db.Column(db.String(100), primary_key=True)
    VALORE_SEQUENZA_TEMPORALE_PROGRAMMA = db.Column(db.Integer)
    NOME_PROGRAMMA = db.Column(db.String(500))
    ORARIO_INIZIO_PROGRAMMA = db.Column(db.Time)
    ORARIO_FINE_PROGRAMMA = db.Column(db.Time)


    # class constructor
    def __init__(self, VALORE_SEQUENZA_TEMPORALE_PROGRAMMA, NOME_PROGRAMMA, ORARIO_INIZIO_PROGRAMMA, ORARIO_FINE_PROGRAMMA, ID_PROGRAMMA=None):
        # if no ID is provided, it generates a new UUID from Python to avoid INSERT errors without a default
        self.ID_PROGRAMMA = ID_PROGRAMMA or str(uuid.uuid4())
        self.VALORE_SEQUENZA_TEMPORALE_PROGRAMMA = VALORE_SEQUENZA_TEMPORALE_PROGRAMMA
        self.NOME_PROGRAMMA = NOME_PROGRAMMA
        self.ORARIO_INIZIO_PROGRAMMA = ORARIO_INIZIO_PROGRAMMA
        self.ORARIO_FINE_PROGRAMMA = ORARIO_FINE_PROGRAMMA
    

    # represent the object when printed
    def __repr__(self):
        return f'<id {self.ID_PROGRAMMA}>'