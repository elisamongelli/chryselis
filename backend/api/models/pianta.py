from api.models import db
import uuid
import datetime



class ActPianteTestataModel(db.Model):

    # specify the DB table name
    __tablename__ = 'act_anagrafica_piante_testata'

    # lists all DB table columns
    ID_PIANTA = db.Column(db.String(100), primary_key=True)
    ID_STATO_PIANTA = db.Column(db.String(500), db.ForeignKey('lkp_stati_piante.ID_STATO'))
    ID_ULTIMO_PROGRAMMA_ESEGUITO = db.Column(db.String(100), db.ForeignKey('lkp_programmi.ID_PROGRAMMA'))
    DATA_INSERIMENTO = db.Column(db.DateTime)
    DATA_ULTIMA_MODIFICA = db.Column(db.DateTime)


    dettaglio = db.relationship(
        'ActPianteDettaglioModel',
        backref = 'testata',
        uselist = False
    )


    # class constructor
    def __init__(self, ID_STATO_PIANTA, ID_ULTIMO_PROGRAMMA_ESEGUITO, ID_PIANTA=None, DATA_INSERIMENTO=None, DATA_ULTIMA_MODIFICA=None):
        # if no ID is provided, it generates a new UUID from Python to avoid INSERT errors without a default
        self.ID_PIANTA = ID_PIANTA or str(uuid.uuid4())
        self.ID_STATO_PIANTA = ID_STATO_PIANTA
        self.ID_ULTIMO_PROGRAMMA_ESEGUITO = ID_ULTIMO_PROGRAMMA_ESEGUITO
        self.DATA_INSERIMENTO = DATA_INSERIMENTO or datetime.datetime.now()
        self.DATA_ULTIMA_MODIFICA = DATA_ULTIMA_MODIFICA or datetime.datetime.now()
    

    # represent the object when printed
    def __repr__(self):
        return f'<id {self.ID_PIANTA}>'
    


class ActPianteDettaglioModel(db.Model):

    # specify the DB table name
    __tablename__ = 'act_anagrafica_piante_dettaglio'

    # lists all DB table columns
    ID_PIANTA = db.Column(db.String(100), db.ForeignKey('act_anagrafica_piante_testata.ID_PIANTA'), primary_key=True)
    NOME_PIANTA = db.Column(db.String(500))
    DESCRIZIONE_PIANTA = db.Column(db.Text)
    FOTO_PIANTA = db.Column(db.LargeBinary)
    ID_STANZA = db.Column(db.String(100), db.ForeignKey('lkp_stanze.ID_STANZA'))
    POSIZIONE_STANZA_X = db.Column(db.Integer)
    POSIZIONE_STANZA_Y = db.Column(db.Integer)


    # class constructor
    def __init__(self, ID_PIANTA, NOME_PIANTA, DESCRIZIONE_PIANTA, FOTO_PIANTA, ID_STANZA, POSIZIONE_STANZA_X, POSIZIONE_STANZA_Y):
        # ID will be taken from the testata table
        self.ID_PIANTA = ID_PIANTA
        self.NOME_PIANTA = NOME_PIANTA
        self.DESCRIZIONE_PIANTA = DESCRIZIONE_PIANTA
        self.FOTO_PIANTA = FOTO_PIANTA
        self.ID_STANZA = ID_STANZA
        self.POSIZIONE_STANZA_X = POSIZIONE_STANZA_X
        self.POSIZIONE_STANZA_Y = POSIZIONE_STANZA_Y
    

    # represent the object when printed
    def __repr__(self):
        return f'<id {self.ID_PIANTA}>'
    


class ActPianteDettaglioSensoriModel(db.Model):

    # specify the DB table name
    __tablename__ = 'act_anagrafica_piante_dettaglio_sensori'

    # lists all DB table columns
    ID_PIANTA = db.Column(db.String(100), db.ForeignKey('act_anagrafica_piante_testata.ID_PIANTA'), primary_key=True)
    UMIDITA_CORRENTE = db.Column(db.Integer)
    ACQUA_ULTIMA_INNAFFIATURA = db.Column(db.Integer)
    ALTRO_DATO_SENSORI_1 = db.Column(db.Numeric(5,2))
    ALTRO_DATO_SENSORI_2 = db.Column(db.Numeric(5,2))
    ALTRO_DATO_SENSORI_3 = db.Column(db.Numeric(5,2))
    ALTRO_DATO_SENSORI_4 = db.Column(db.Numeric(5,2))


    # class constructor
    def __init__(self, ID_PIANTA, UMIDITA_CORRENTE, ACQUA_ULTIMA_INNAFFIATURA, ALTRO_DATO_SENSORI_1, ALTRO_DATO_SENSORI_2, ALTRO_DATO_SENSORI_3, ALTRO_DATO_SENSORI_4):
        # ID will be taken from the testata table
        self.ID_PIANTA = ID_PIANTA
        self.UMIDITA_CORRENTE = UMIDITA_CORRENTE
        self.ACQUA_ULTIMA_INNAFFIATURA = ACQUA_ULTIMA_INNAFFIATURA
        self.ALTRO_DATO_SENSORI_1 = ALTRO_DATO_SENSORI_1
        self.ALTRO_DATO_SENSORI_2 = ALTRO_DATO_SENSORI_2
        self.ALTRO_DATO_SENSORI_3 = ALTRO_DATO_SENSORI_3
        self.ALTRO_DATO_SENSORI_4 = ALTRO_DATO_SENSORI_4
    

    # represent the object when printed
    def __repr__(self):
        return f'<id {self.ID_PIANTA}>'