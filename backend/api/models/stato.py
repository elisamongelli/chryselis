from api.models import db
from sqlalchemy import CheckConstraint



class LookupStatiModel(db.Model):

    # specify the DB table name
    __tablename__ = 'lkp_stati_piante'
    """ __table_args__ = (
        CheckConstraint("ID_STATO IN ('TROPPO_SECCO','SECCO','UMIDO','BAGNATO','TROPPO_BAGNATO')"),
    ) """

    # lists all DB table columns
    ID_STATO = db.Column(db.String(500), primary_key=True)
    NOME_STATO = db.Column(db.String(500))
    DESCRIZIONE_STATO = db.Column(db.Text)


    # class constructor
    def __init__(self, ID_STATO, NOME_STATO, DESCRIZIONE_STATO):
        # ID is required, because corresponds to the status code
        self.ID_STATO = ID_STATO
        self.NOME_STATO = NOME_STATO
        self.DESCRIZIONE_STATO = DESCRIZIONE_STATO
    

    # represent the object when printed
    def __repr__(self):
        return f'<id {self.ID_STATO}>'