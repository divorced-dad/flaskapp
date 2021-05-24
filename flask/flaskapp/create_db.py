from flaskapp import db
from flaskapp.models import Comune, Prodotto, Utente, Giorni_Disponibili, Comune_Prodotto, Donazione, Ritiro


def create():
    # db.drop_all()
    db.create_all()

    comune_1 = Comune(nome="Verona", cap="3700")
    db.session.add(comune_1)
    comune_2 = Comune(nome="Rovereto", cap="3900")
    db.session.add(comune_2)
    comune_3 = Comune(nome="Malcesine", cap="4000")
    db.session.add(comune_3)

    db.session.commit()