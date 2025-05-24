# app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import Owner
from app.extensions import db
from app.forms.forms import RegistrationForm, LoginForm
from flask_login import login_user
from flask_login import logout_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth", methods=["GET", "POST"])
def auth():
    form = LoginForm()
    if form.validate_on_submit():
        user = Owner.query.filter_by(login=form.login.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Вход выполнен успешно.", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Неверный логин или пароль", "danger")
    return render_template("auth.html", form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = Owner.query.filter_by(login=form.login.data).first()
        if existing_user:
            flash("User already exists", "danger")
        else:
            new_user = Owner(
                login=form.login.data,
                password=generate_password_hash(form.password.data),
                phone = form.phone.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Регистрация прошла успешно!", "success")
            return redirect(url_for("auth.auth"))
    return render_template("register.html", form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Выход выполнен успешно.", "info")
    return redirect(url_for("auth.auth"))