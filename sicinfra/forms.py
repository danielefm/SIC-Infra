from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sicinfra.models import User, Campi, Ambientes, Edificios


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class CampusForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    criar = SubmitField('Criar')

def campus_query():
    return Campi.query

class EdificioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sigla = StringField('Sigla')
    nome_campus = QuerySelectField(query_factory=campus_query, allow_blank=False, get_label='nome')
    criar = SubmitField('Criar')

def edificio_query():
    return Edificios.query

opcoes_uso = [(9,'Escritórios'), (11,'Laboratórios e Estúdios'), (13,'Escolas em geral'),(18,'Museus e bibliotecas'),(22,'Artes cênicas e auditórios'),(25,'Restaurantes'),(29,'Hospitais Veterinários'),(30,'Hospitais em geral'),(37,'Depósitos')]

class AmbienteForm(FlaskForm):
    endereco = StringField('Endereço (Ex.: AT-15/25)', validators=[DataRequired()])
    descricao = StringField('Descrição (Ex.: Copa)', validators=[DataRequired()])
    area_total = DecimalField('Área Total', validators=[DataRequired()])
    area_util = DecimalField('Área Útil', validators=[DataRequired()])
    uso = SelectField('Uso', validators=[DataRequired()], choices=opcoes_uso)
    nome_edificio = QuerySelectField(query_factory=edificio_query, allow_blank=False, get_label='nome')
    criar = SubmitField('Criar')