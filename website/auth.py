from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

class Auth():
    
    auth = Blueprint('auth', __name__)

    @auth.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            cpf = request.form.get('cpf')
            password = request.form.get('password')
            user = User.query.filter_by(cpf=cpf).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Login reussi !', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Mot de passe incorrecte, Veuillez réessayer..', category='error')
            else:
                flash('Email n"existe pas ', category='error')

        return render_template("login.html", user=current_user)


    @auth.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('auth.login'))


    @auth.route('/sign-up', methods=['GET', 'POST'])
    def sign_up():
        if request.method == 'POST':
            cpf = request.form.get('cpf')
            first_name = request.form.get('firstName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            
            user = User.query.filter_by(cpf=cpf).first()
            if user:
                flash('Email existe déja', category='error')
            elif len(cpf) < 11:
                flash('Email invalide', category='error')
            elif len(first_name) < 2:
                flash('Le nom doit etre plus long..', category='error')
            elif password1 != password2:
                flash('Verifer votre mot de passe', category='error')
            elif len(password1) < 7:
                flash('Le mot de passe doit contenir au moins 7 caractères.', category='error')
            else:
                new_user = User(first_name=first_name, password=generate_password_hash(
                    password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Bienvenue !', category='success')
                return redirect(url_for('views.home'))

        return render_template("sign_up.html", user=current_user)
