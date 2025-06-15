from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.models import Car, Order
from app.forms import CarForm
from flask_wtf import FlaskForm

cars_bp = Blueprint("cars", __name__)


class DummyDeleteForm(FlaskForm):
    pass


@cars_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = CarForm()
    cars = Car.query.filter_by(owner_id=current_user.id).all()
    orders = Order.query.filter_by(user_id=current_user.id).all()
    delete_forms = {car.id: DummyDeleteForm() for car in cars}

    if form.validate_on_submit():
        new_car = Car(
            owner_id=current_user.id,
            model_id=form.model_id.data,
            plate_number=form.plate.data,
            year=form.year.data,
            note=form.note.data,
        )
        db.session.add(new_car)
        db.session.commit()
        flash("Автомобиль успешно добавлен", "success")
        return redirect(url_for("cars.account"))

    return render_template(
        "account.html",
        user=current_user,
        cars=cars,
        orders=orders,
        delete_forms=delete_forms,
        form=form,
    )


@cars_bp.route("/car/<int:car_id>/edit", methods=["GET", "POST"])
@login_required
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.owner_id != current_user.id:
        flash("Доступ запрещён", "danger")
        return redirect(url_for("cars.account"))

    form = CarForm(obj=car)
    if form.validate_on_submit():
        car.model_id = form.model_id.data
        car.plate_number = form.plate.data
        car.year = form.year.data
        car.note = form.note.data
        db.session.commit()
        flash("Автомобиль обновлён", "success")
        return redirect(url_for("cars.account"))

    return render_template("edit_car.html", form=form)


@cars_bp.route("/car/<int:car_id>/delete", methods=["POST"])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.owner_id != current_user.id:
        flash("Доступ запрещён", "danger")
        return redirect(url_for("cars.account"))

    db.session.delete(car)
    db.session.commit()
    flash("Автомобиль удалён", "success")
    return redirect(url_for("cars.account"))
