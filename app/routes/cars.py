from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.models import Car, CarModel

cars_bp = Blueprint("cars", __name__)

# Редактирование машины
@cars_bp.route("/edit_car/<int:car_id>", methods=["GET", "POST"])
@login_required
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)

    # Проверка: только владелец может редактировать
    if car.owner_id != current_user.id:
        flash("Вы не можете редактировать чужую машину.", "danger")
        return redirect(url_for("main.account"))

    models = CarModel.query.all()

    if request.method == "POST":
        car.model_id = int(request.form["model_id"])
        car.plate_number = request.form["plate"]
        car.year = int(request.form["year"])
        car.note = request.form.get("note", "")
        db.session.commit()
        flash("Данные автомобиля обновлены!", "success")
        return redirect(url_for("main.account"))

    return render_template("edit_car.html", car=car, models=models)

# Удаление машины
@cars_bp.route("/delete_car/<int:car_id>", methods=["POST"])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)

    # Проверка: только владелец может удалять
    if car.owner_id != current_user.id:
        flash("Вы не можете удалить чужую машину.", "warning")
        return redirect(url_for("main.account"))

    db.session.delete(car)
    db.session.commit()
    flash("Автомобиль удалён.", "success")
    return redirect(url_for("main.account"))