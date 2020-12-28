import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from sicinfra import app, db, bcrypt
from sicinfra.forms import RegistrationForm, LoginForm, UpdateAccountForm, CampusForm, EdificioForm
from sicinfra.models import User, Post, Campi, Edificios
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/campi")
def campi():
    campi = Campi.query.all()
    return render_template('campi.html', title='Campi', campi=campi)

@app.route("/edificios")
def edificios():
    edificios = Edificios.query.all()
    return render_template('edificios.html', title='Edificios', edificios=edificios)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/campi/novo", methods=['GET', 'POST'])
@login_required
def novo_campus():
    form = CampusForm()
    if form.validate_on_submit():
        campus = Campi(nome=form.nome.data)
        db.session.add(campus)
        db.session.commit()
        flash("Novo campus criado!", "success")
        return redirect(url_for('home'))
    return render_template('criar_campus.html', title='Novo Campus',
                            form=form, legend='Novo Campus')

@app.route("/edificios/novo", methods=['GET', 'POST'])
@login_required
def novo_edificio():
    form = EdificioForm()
    if form.validate_on_submit():
        nome_campus_origem = form.nome_campus.data.nome
        campus_origem = Campi.query.filter_by(nome=nome_campus_origem).first()
        edificio = Edificios(nome=form.nome.data, sigla=form.sigla.data, id_campus=campus_origem.id)
        db.session.add(edificio)
        db.session.commit()
        flash("Novo edificio criado!", "success")
        return redirect(url_for('home'))
    return render_template('criar_edificio.html', title='Novo Edificio',
                            form=form, legend='Novo Edificio')

@app.route("/campi/<int:campus_id>")
def campus(campus_id):
    campus = Campi.query.get_or_404(campus_id)
    return render_template('campus.html', title=campus.nome, campus=campus)

@app.route("/edificios/<int:edificio_id>")
def edificio(edificio_id):
    edificio = Edificios.query.get_or_404(edificio_id)
    return render_template('edificio.html', title=edificio.nome, edificio=edificio)

@app.route("/campi/<int:campus_id>/update", methods=['GET', 'POST'])
@login_required
def update_campus(campus_id):
    campus = Campi.query.get_or_404(campus_id)
    form = CampusForm()
    if form.validate_on_submit():
        campus.nome = form.nome.data
        db.session.commit()
        flash('O campus foi atualizado!', 'success')
        return redirect(url_for('campi', campus_id=campus.id))
    elif request.method == 'GET':
        form.nome.data = campus.nome
    return render_template('criar_campus.html', title="Editar Campus",
                            form=form, legend='Editar Campus')

@app.route("/edificios/<int:edificio_id>/update", methods=['GET', 'POST'])
@login_required
def update_edificio(edificio_id):
    edificio = Edificios.query.get_or_404(edificio_id)
    form = EdificioForm()
    if form.validate_on_submit():
        nome_campus_origem = form.nome_campus.data.nome
        campus_origem = Campi.query.filter_by(nome=nome_campus_origem).first()
        edificio = Edificios(nome=form.nome.data, sigla=form.sigla.data, id_campus=campus_origem.id)
        db.session.commit()
        flash('O edificio foi atualizado!', 'success')
        return redirect(url_for('edificios', edificio_id=edificio.id))
    elif request.method == 'GET':
        form.nome.data = edificio.nome
    return render_template('criar_edificio.html', title="Editar Edificio",
                            form=form, legend='Editar Edificio')


@app.route("/campi/<int:campus_id>/deletar", methods=['POST'])
@login_required
def deletar_campus(campus_id):
    campus = Campi.query.get_or_404(campus_id)
    db.session.delete(campus)
    db.session.commit()
    flash('O campus foi deletado!', 'success')
    return redirect(url_for('campi', campus_id=campus.id))

@app.route("/edificios/<int:edificio_id>/deletar", methods=['POST'])
@login_required
def deletar_edificio(edificio_id):
    edificio = Edificios.query.get_or_404(edificio_id)
    db.session.delete(edificio)
    db.session.commit()
    flash('O edificio foi deletado!', 'success')
    return redirect(url_for('edificios', edificio_id=edificio.id))
