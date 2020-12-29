from datetime import datetime
from sicinfra import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', cascade="all,delete", backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Campi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    edificios = db.relationship('Edificios', cascade="all,delete", backref='Campus de localizacao', lazy=True)

    def __repr__(self):
        return f"{self.id}"

class Edificios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sigla = db.Column(db.String(10))
    id_campus = db.Column(db.Integer, db.ForeignKey('campi.id'), nullable=False)
    num_ambientes = db.Column(db.Integer)
    area_total_construida = db.Column(db.Float(precision=',2'))
    area_util_construida = db.Column(db.Float(precision=',2'))
    uso_principal = db.Column(db.String(30))
    uso_secundario = db.Column(db.String(30))
    ambientes = db.relationship('Ambientes', cascade="all,delete", backref='Edificio de localizacao', lazy=True)

class Ambientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endereco = db.Column(db.String(15), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    area_total = db.Column(db.Float(precision=',2'), nullable=False)
    area_util = db.Column(db.Float(precision=',2'), nullable=False)
    uso = db.Column(db.String(30), nullable=False)
    id_edificio = db.Column(db.Integer, db.ForeignKey('edificios.id'), nullable=False)