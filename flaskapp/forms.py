from flask.helpers import url_for
from flask_wtf import FlaskForm
import sqlalchemy
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_components import TimeField
from flaskapp.models import Comune, Prodotto, Utente, Giorni_Disponibili, Comune_Prodotto, Donazione, Ritiro


class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=40)])
    cognome = StringField('Cognome', validators=[DataRequired(), Length(min=2, max=40)])
    ruolo = SelectField(' Ruolo', choices=['Volontario', 'Donatore', 'Bisognoso'])
    choices = []
    try:
        for comune in Comune.query.all():
            choices.append((comune.id, comune.nome))
    except sqlalchemy.exc.ProgrammingError:
        pass
        # print("Table 'beni_primari.comune' doesn't exist")
    comune_volontariato = SelectField('Comune volontariato', choices=choices)
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Conferma la password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        email = Utente.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email gia\' utilizzata. Prova con una email diversa.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    ruolo = SelectField(' Ruolo', choices=['Volontario', 'Donatore', 'Bisognoso'])
    choices = []
    try:
        for comune in Comune.query.all():
            choices.append((comune.id, comune.nome))
    except sqlalchemy.exc.InternalError or sqlalchemy.exc.ProgrammingError:
        pass
        # print("Table 'beni_primari.comune' doesn't exist")
    comune_volontariato = SelectField('Comune volontariato', choices=choices)
    orario_inizio = TimeField('Orario di inizio')
    orario_fine = TimeField('Orario di fine')
    lunedi = BooleanField('Lunedi\'')
    martedi = BooleanField('Martedi\'')
    mercoledi = BooleanField('Mercoledi\'')
    giovedi = BooleanField('Giovedi\'')
    venerdi = BooleanField('Venerdi\'')
    sabato = BooleanField('Sabato')
    domenica = BooleanField('Domenica')
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=40)])
    submit = SubmitField('Aggiorna dati Account')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = Utente.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email gia\' utilizzata. Prova con una email diversa.')
    
    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        result = True
        print("aSSSSS")
        print(self.orario_inizio)
        print(type(self.orario_inizio))
        if self.orario_fine.data < self.orario_inizio.data:
            result = False
            self.orario_fine.errors.append('L\'orario di fine deve essere successivo all\'orario d\'inizio.')
        return result
    
    # def validate_orario_fine_orario_inizio(self, orario_fine, orario_inizio):
    #     print(orario_inizio)
    #     print(orario_fine)
        
    #         raise ValidationError('L\'orario di fine deve essere successivo all\'orario d\'inizio.')


class DonazioneForm(FlaskForm):
    nome = StringField('Nome Prodotto', validators=[DataRequired(), Length(min=2, max=40)])
    tipologia = StringField('Tipologia', validators=[DataRequired(), Length(min=2, max=40)])
    quantita = IntegerField('Quantita\'', validators=[DataRequired()])
    choices = []
    try:
        for comune in Comune.query.all():
            choices.append((comune.id, comune.nome))
    except sqlalchemy.exc.InternalError or sqlalchemy.exc.ProgrammingError:
        pass
        # print("Table 'beni_primari.comune' doesn't exist")
    comune = SelectField('Comune di destinazione', choices=choices)
    submit = SubmitField('Dona')


class RitiroForm(FlaskForm):
    choices = []
    try:
        for prodotto in Prodotto.query.all():
            choices.append((prodotto.id, prodotto.nome))
    except sqlalchemy.exc.InternalError or sqlalchemy.exc.ProgrammingError:
        pass
    nome = SelectField('Seleziona un prodotto', choices=choices)
    quantita = IntegerField('Quantita\'', validators=[DataRequired()])
    choices = []
    try:
        for comune in Comune.query.all():
            choices.append((comune.id, comune.nome))
    except sqlalchemy.exc.InternalError or sqlalchemy.exc.ProgrammingError:
        pass
        # print("Table 'beni_primari.comune' doesn't exist")
    comune = SelectField('Comune sede del prodotto', choices=choices)
    submit = SubmitField('Dona')