from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_utente(utente_id):
    return Utente.query.get(int(utente_id))

# Association Object M2M table with *attributes*
# https://stackoverflow.com/questions/38654624/flask-sqlalchemy-many-to-many-relationship-new-attribute
class Comune_Prodotto(db.Model):
    comune_id = db.Column('comune_id', db.Integer, db.ForeignKey('comune.id'), primary_key=True)
    prodotto_id = db.Column('prodotto_id', db.Integer, db.ForeignKey('prodotto.id'), primary_key=True)
    quantita = db.Column('quantita', db.Integer, nullable=False)
    comune = db.relationship("Comune", back_populates="prodotti")
    prodotto = db.relationship("Prodotto", back_populates="comuni")

# comune_prodotto = db.Table('Comune_Prodotto',
#     db.Column('comune_id', db.Integer, db.ForeignKey('comune.id')),
#     db.Column('prodotto_id', db.Integer, db.ForeignKey('prodotto.id')),
#     db.Column('quantita', db.Integer, nullable=False),
# )

class Donazione(db.Model):
    utente_id = db.Column('utente_id', db.Integer, db.ForeignKey('utente.id'), primary_key=True)
    prodotto_id = db.Column('prodotto_id', db.Integer, db.ForeignKey('prodotto.id'), primary_key=True)
    quantita = db.Column('quantita', db.Integer, nullable=False)
    data_ora = db.Column('data_ora', db.DateTime, default=datetime.utcnow, primary_key=True)
    donatore = db.relationship("Utente", back_populates="prodotti_donati")
    prodotto_donato = db.relationship("Prodotto", back_populates="donatori")

class Ritiro(db.Model):
    utente_id = db.Column('utente_id', db.Integer, db.ForeignKey('utente.id'), primary_key=True)
    prodotto_id = db.Column('prodotto_id', db.Integer, db.ForeignKey('prodotto.id'), primary_key=True)
    quantita = db.Column('quantita', db.Integer, nullable=False)
    data_ora = db.Column('data_ora', db.DateTime, default=datetime.utcnow, primary_key=True)
    bisognoso = db.relationship("Utente", back_populates="prodotti_ritirati")
    prodotto_ritirato = db.relationship("Prodotto", back_populates="bisognosi")

# donazione = db.Table('Donazione',
#     db.Column('utente_id', db.Integer, db.ForeignKey('utente.id')),
#     db.Column('prodotto_id', db.Integer, db.ForeignKey('prodotto.id')),
#     # db.Column('comune_id', db.Integer, db.ForeignKey('comune.id')),
#     db.Column('data_ora_donazione', db.DateTime, default=datetime.utcnow),
#     db.Column('quantita', db.Integer, nullable=False),
# )

# ritiro = db.Table('Ritiro',
#     db.Column('utente_id', db.Integer, db.ForeignKey('utente.id')),
#     db.Column('prodotto_id', db.Integer, db.ForeignKey('prodotto.id')),
#     # db.Column('comune_id', db.Integer, db.ForeignKey('comune.id')),
#     db.Column('data_ora_ritiro', db.DateTime, default=datetime.utcnow),
#     db.Column('quantita', db.Integer, nullable=False),
# )

class Comune(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    cap = db.Column(db.Integer, nullable=False)
    utenti = db.relationship('Utente', backref='comune', lazy=True)
    prodotti = db.relationship("Comune_Prodotto", back_populates='comune', lazy='dynamic')
    # donazioni = db.relationship('Prodotto', secondary=donazione, back_populates='donazioni', lazy=True)
    # ritiri = db.relationship('Prodotto', secondary=ritiro, back_populates='ritiri', lazy=True)

    def __repr__(self):
        return f"Comune('{self.id}', '{self.nome}', '{self.cap}')"


class Prodotto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    quantita = db.Column(db.Integer, nullable=False)
    tipologia = db.Column(db.String(40), nullable=False)
    comuni = db.relationship("Comune_Prodotto", back_populates='prodotto', lazy='dynamic')
    donatori = db.relationship('Donazione', back_populates='prodotto_donato', lazy='dynamic')
    bisognosi = db.relationship('Ritiro', back_populates='prodotto_ritirato', lazy='dynamic')

    def __repr__(self):
        return f"Prodotto('{self.id}', '{self.nome}', '{self.quantita}', '{self.tipologia}')"


class Utente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True,nullable=False)
    nome = db.Column(db.String(40), nullable=False)
    cognome = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    ruolo = db.Column(db.String(40), nullable=False)
    orario_inizio = db.Column(db.Time, nullable=True)
    orario_fine = db.Column(db.Time, nullable=True)
    comune_volontariato = db.Column(db.Integer, db.ForeignKey('comune.id'), nullable=False)
    giorni_disponibili = db.relationship('Giorni_Disponibili', backref='utente', lazy=True)
    prodotti_donati = db.relationship('Donazione', back_populates='donatore', lazy='dynamic')
    prodotti_ritirati = db.relationship('Ritiro', back_populates='bisognoso', lazy='dynamic')


    def __repr__(self):
        return f"Utente('{self.id}', '{self.email}', '{self.nome}', '{self.cognome}', '{self.password}', '{self.ruolo}', '{self.orario_inizio}', '{self.orario_fine}')"


class Giorni_Disponibili(db.Model):
    utente_id = db.Column(db.Integer, db.ForeignKey('utente.id'), primary_key=True)
    lunedi = db.Column(db.Boolean, nullable=False)
    martedi = db.Column(db.Boolean, nullable=False)
    mercoledi = db.Column(db.Boolean, nullable=False)
    giovedi = db.Column(db.Boolean, nullable=False)
    venerdi = db.Column(db.Boolean, nullable=False)
    sabato = db.Column(db.Boolean, nullable=False)
    domenica = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Utente('{self.utente_id}', '{self.lunedi}', '{self.martedi}', '{self.mercoledi}', '{self.giovedi}', '{self.venerdi}', '{self.sabato}', '{self.domenica}')"


# db.drop_all()
db.create_all()

comune_1 = Comune(nome="Verona", cap="3700")
db.session.add(comune_1)
comune_2 = Comune(nome="Rovereto", cap="3900")
db.session.add(comune_2)
comune_3 = Comune(nome="Malcesine", cap="4000")
db.session.add(comune_3)

db.session.commit()

'''
drop database beni_primari;
create database beni_primari;

#POPOLAMENTO
from flaskapp.models import db
from flaskapp import bcrypt
db.drop_all()
db.create_all()
from flaskapp.models import Comune, Prodotto, Utente, Giorni_Disponibili, Comune_Prodotto, Donazione, Ritiro

comune_1 = Comune(nome="Verona", cap="3700")
db.session.add(comune_1)
comune_2 = Comune(nome="Rovereto", cap="3900")
db.session.add(comune_2)

#prodotto_1 = Prodotto(nome="Banane", quantita=654, tipologia="frutta")
#db.session.add(prodotto_1)

pw = bcrypt.generate_password_hash('123').decode('utf-8')
utente_1 = Utente(email="prova@gmail.com", nome="Mario", cognome="Rossi", password=pw, ruolo="donatore", comune_volontariato=1, orario_inizio='00:00:00', orario_fine='00:00:00')
db.session.add(utente_1)


giorni_disponibili_1 = Giorni_Disponibili(utente_id=1, lunedi=0, martedi=0, mercoledi=0, giovedi=0, venerdi=0, sabato=0, domenica=0)
db.session.add(giorni_disponibili_1)
db.session.commit()

# esempi query
Comune.query.all()
Comune.query.first()
comune = Comune.query.filter_by(nome="Rovereto").all()
comune = Comune.query.get(1)
comune
comune.posizioni_prodotto
prodotto = Prodotto.query.first()
for prodotto in Comune.query.first().comuni_prodotti:
    print(prodotto.nome)

#INSERT M2M
db.session.execute(comune_prodotto.insert().values(comune_id=1, prodotto_id=1))
db.session.execute(donazione.insert().values(utente_id=1, prodotto_id=1, quantita=252))
db.session.commit()
#INSERT M2M 2
comune = Comune.query.first()
prodotto = Prodotto(nome="Mela", tipologia="Frutta", quantita="4", comuni_prodotti=[comune])
db.session.add(prodotto)
db.session.commit()
prodotto = Prodotto.query.first()
prodotto.comuni_prodotto.all() = [Comune('1', 'Verona', '3700')]
prodotto.comuni_prodotti.append(rovereto)
db.session.commit()


'''