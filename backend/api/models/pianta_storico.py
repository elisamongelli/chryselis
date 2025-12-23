from api.models import db



class ActPianteStoricoModel(db.Model):

    # specify the DB table name
    __tablename__ = 'his_anagrafica_piante_dettaglio_sensori'

    # lists all DB table columns
    ID_PIANTA = db.Column(db.String(100), db.ForeignKey('act_anagrafica_piante_testata.ID_PIANTA'), primary_key=True)
    ID_STATO_PIANTA = db.Column(db.String(500), db.ForeignKey('lkp_stati_piante.ID_STATO'))
    ID_PROGRAMMA_ESEGUITO = db.Column(db.String(100), db.ForeignKey('lkp_programmi.ID_PROGRAMMA'))
    UMIDITA_CORRENTE = db.Column(db.Integer)
    ACQUA_ULTIMA_INNAFFIATURA = db.Column(db.Integer)
    ALTRO_DATO_SENSORI_1 = db.Column(db.Numeric(5,2))
    ALTRO_DATO_SENSORI_2 = db.Column(db.Numeric(5,2))
    ALTRO_DATO_SENSORI_3 = db.Column(db.Numeric(5,2))
    ALTRO_DATO_SENSORI_4 = db.Column(db.Numeric(5,2))
    DATA_MODIFICA = db.Column(db.DateTime)


    # class constructor
    def __init__(self, ID_PIANTA, ID_STATO_PIANTA, ID_PROGRAMMA_ESEGUITO, UMIDITA_CORRENTE, ACQUA_ULTIMA_INNAFFIATURA, ALTRO_DATO_SENSORI_1, ALTRO_DATO_SENSORI_2, ALTRO_DATO_SENSORI_3, ALTRO_DATO_SENSORI_4, DATA_MODIFICA):
        # ID will be taken from the testata table
        self.ID_PIANTA = ID_PIANTA
        self.ID_STATO_PIANTA = ID_STATO_PIANTA
        self.ID_PROGRAMMA_ESEGUITO = ID_PROGRAMMA_ESEGUITO
        self.UMIDITA_CORRENTE = UMIDITA_CORRENTE
        self.ACQUA_ULTIMA_INNAFFIATURA = ACQUA_ULTIMA_INNAFFIATURA
        self.ALTRO_DATO_SENSORI_1 = ALTRO_DATO_SENSORI_1
        self.ALTRO_DATO_SENSORI_2 = ALTRO_DATO_SENSORI_2
        self.ALTRO_DATO_SENSORI_3 = ALTRO_DATO_SENSORI_3
        self.ALTRO_DATO_SENSORI_4 = ALTRO_DATO_SENSORI_4
        self.DATA_MODIFICA = DATA_MODIFICA
    

    # represent the object when printed
    def __repr__(self):
        return f'<id {self.ID_PIANTA}>'