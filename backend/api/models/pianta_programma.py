from api.models import db
from sqlalchemy import PrimaryKeyConstraint



class LookupPianteProgrammiModel(db.Model):

    # specify the DB table name
    __tablename__ = 'lkp_piante_programmi'
    __table_args__ = (
        PrimaryKeyConstraint('ID_PIANTA', 'ID_PROGRAMMA'),
    )

    # list all DB table columns
    ID_PIANTA = db.Column(db.String(100), db.ForeignKey('act_anagrafica_piante_testata.ID_PIANTA'))
    ID_PROGRAMMA = db.Column(db.String(100), db.ForeignKey('lkp_programmi.ID_PROGRAMMA'))


    # class constructor
    def __init__(self, ID_PIANTA, ID_PROGRAMMA):
        self.ID_PIANTA = ID_PIANTA
        self.ID_PROGRAMMA = ID_PROGRAMMA
    

    # represent the object when printed
    def __repr__(self):
        return f'<id pianta {self.ID_PIANTA}, id programma {self.ID_PROGRAMMA}>'