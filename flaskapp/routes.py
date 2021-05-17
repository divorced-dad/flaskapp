from datetime import datetime
from flask import url_for, render_template, flash, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, DonazioneForm, RitiroForm
from flaskapp.models import Comune, Prodotto, Utente, Giorni_Disponibili, Comune_Prodotto, Donazione, Ritiro
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/index")
def index():
    prodotti = Prodotto.query.all()
    comuni_prodotti = Comune_Prodotto.query.all()
    donazioni = Donazione.query.all()
    utenti = Utente.query.all()
    return render_template("index.html", 
                           prodotti=prodotti,
                           comuni_prodotti=comuni_prodotti,
                           donazioni=donazioni,
                           utenti=utenti,
                           title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        utente = Utente(email=form.email.data, nome=form.nome.data,
                        cognome=form.cognome.data,
                        password=hashed_password, ruolo=form.ruolo.data, 
                        comune_volontariato=form.comune_volontariato.data,
                        orario_inizio='00:00:00',
                        orario_fine='00:00:00')
        db.session.add(utente)
        db.session.commit()
        utente_id = Utente.query.filter_by(email=utente.email).first().id

        giorni_disponibili = Giorni_Disponibili(utente_id=utente_id, lunedi=0, martedi=0, 
                            mercoledi=0, giovedi=0, venerdi=0, sabato=0, domenica=0)
        db.session.add(giorni_disponibili)
        db.session.commit()

        flash('Account creato! Puoi ora effettuare il login', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        utente = Utente.query.filter_by(email=form.email.data).first()
        print(utente)
        print(form.password.data)
        print(bcrypt.check_password_hash(utente.password, form.password.data))
        if utente and bcrypt.check_password_hash(utente.password, form.password.data):
            login_user(utente)
            return redirect(url_for('index'))
        else:
            flash('Login non riuscito. Contralla email e password', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    giorni_disponibili = Giorni_Disponibili.query.filter_by(
                         utente_id=current_user.id).first()
    comune = Comune.query.filter_by(id=current_user.comune_volontariato).first()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.ruolo = form.ruolo.data
        print(form.comune_volontariato.data)
        current_user.orario_inizio = form.orario_inizio.data
        current_user.comune_volontariato = form.comune_volontariato.data
        current_user.orario_inizio = form.orario_inizio.data
        current_user.orario_fine = form.orario_fine.data
        giorni_disponibili = Giorni_Disponibili.query.filter_by(utente_id=current_user.id).first()
        giorni_disponibili.lunedi = form.lunedi.data
        giorni_disponibili.martedi = form.martedi.data
        giorni_disponibili.mercoledi = form.mercoledi.data
        giorni_disponibili.giovedi = form.giovedi.data
        giorni_disponibili.venerdi = form.venerdi.data
        giorni_disponibili.sabato = form.sabato.data
        giorni_disponibili.domenica = form.domenica.data
        db.session.commit()
        flash('Il tuo account e\' stato aggiornato!', 'success')
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.ruolo.data = current_user.ruolo
        form.comune_volontariato.data = current_user.comune_volontariato
        form.orario_inizio.data = current_user.orario_inizio
        form.orario_fine.data = current_user.orario_fine
        form.lunedi.data = giorni_disponibili.lunedi
        form.martedi.data = giorni_disponibili.martedi
        form.mercoledi.data = giorni_disponibili.mercoledi
        form.giovedi.data = giorni_disponibili.giovedi
        form.venerdi.data = giorni_disponibili.venerdi
        form.sabato.data = giorni_disponibili.sabato
        form.domenica.data = giorni_disponibili.domenica
    return render_template("account.html", title="Account", form=form, comune=comune,
                           giorni_disponibili=giorni_disponibili)
                    

@app.route("/new_donazione", methods=['GET', 'POST'])
@login_required
def new_donazione():
    form = DonazioneForm()
    if form.validate_on_submit():
        prodotto = Prodotto.query.filter_by(nome=form.nome.data).first()
        if prodotto is None:
            prodotto = Prodotto(nome=form.nome.data,
                                tipologia=form.tipologia.data,
                                quantita=form.quantita.data)
            db.session.add(prodotto)
            db.session.commit()
        
        prodotto = Prodotto.query.filter_by(nome=form.nome.data).first()
        exists_comune_prodotto = False
        for comune_prodotto in Comune_Prodotto.query.all():
            if comune_prodotto.comune_id == int(form.comune.data)\
                and comune_prodotto.prodotto_id == prodotto.id:
                exists_comune_prodotto = True
        if not exists_comune_prodotto:
            comune_prodotto = Comune_Prodotto(comune_id=form.comune.data,
                                              prodotto_id=prodotto.id,
                                              quantita=form.quantita.data)
            db.session.add(comune_prodotto)
            db.session.commit()
        else:
            comune_prodotto = Comune_Prodotto.query.filter_by(\
                              prodotto_id=prodotto.id, comune_id=form.comune.data).first()
            comune_prodotto.quantita += int(form.quantita.data)
            db.session.commit()

        donazione = Donazione(utente_id=current_user.id,
                              prodotto_id=prodotto.id,
                              quantita=form.quantita.data)
        prodotto.quantita += int(form.quantita.data) # quantita' complessiva del prodotto
        db.session.add(donazione)
        db.session.commit()

        flash("Donazione effettuata!", "success")
        return redirect(url_for('index'))
    return render_template("new_donazione.html", title="Nuova donazione", form=form)


@app.route("/new_ritiro", methods=['GET', 'POST'])
@login_required
def new_ritiro():
    form = RitiroForm()
    if form.validate_on_submit():
        quantita_disponibile = Comune_Prodotto.query.filter_by( prodotto_id=form.nome.data,
                               comune_id=form.comune.data).first().quantita
        if int(quantita_disponibile) < int(form.quantita.data):
            flash("Quantita' superiore alla quantita' disponibile", "danger")
        else:
            flash("Ritiro prodotto effettuato!", "success")
            return redirect(url_for('index'))
    return render_template("new_ritiro.html", title="Nuova ritiro", form=form)



