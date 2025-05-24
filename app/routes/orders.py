from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.forms import OrderForm
from app.extensions import db
from app.models.models import Order, OrderItem, ServiceType, Car, PartNumber
from app.models.models import BodyPart

orders_bp = Blueprint("orders", __name__)

# Страница выбора работ
@orders_bp.route("/order", methods=["GET", "POST"])
@login_required
def create_order():
    form = OrderForm()
    form.car_id.choices = [(car.id, f"{car.model.name} - {car.plate_number}") for car in Car.query.filter_by(owner_id=current_user.id)]
    form.service_type_id.choices = [(s.id, s.name) for s in ServiceType.query.all()]
    form.part_number_id.choices = [(0, "None")] + [(p.id, f"{p.code} - {p.description}") for p in PartNumber.query.all()]

    cars = Car.query.filter_by(owner_id=current_user.id).all()
    services = ServiceType.query.all()
    parts = PartNumber.query.all()
    body_parts = BodyPart.query.all()

    return render_template("order.html", form=form, cars=cars, services=services, parts=parts, body_parts=body_parts)

# Подтверждение и сохранение заказа
@orders_bp.route("/confirm", methods=["POST"])
@login_required
def confirm_order():
    print("\n=== ЗАПРОС НА /confirm ===")
    try:
        if not request.is_json:
            print("❌ НЕ JSON (Content-Type не application/json)")
            return jsonify(success=False, message="Ожидался JSON-запрос"), 400

        data = request.get_json(force=True)
        print("✅ JSON parsed:", data)

        car_id = data.get("car_id")
        items_data = data.get("items")

        if not car_id or not items_data:
            return jsonify(success=False, message="Недостаточно данных"), 400

        car_id = int(car_id)

        # Словари
        parts_dict = {p.id: p for p in PartNumber.query.all()}
        services_dict = {s.id: s for s in ServiceType.query.all()}

        description_lines = []
        total_price = 0
        items = []

        for i, item in enumerate(items_data):
            try:
                service_id = int(item.get("service_id"))
                part_id = int(item.get("part_id"))
                body_part_id = int(item.get("body_part_id"))
                price = float(item.get("price"))
            except (TypeError, ValueError) as e:
                return jsonify(success=False, message=f"Ошибка в item[{i}] — {e}"), 400

            service = services_dict.get(service_id)
            part = parts_dict.get(part_id)

            if not service or not part:
                return jsonify(success=False, message=f"Некорректные ID в item[{i}]"), 400

            description_lines.append(f"{service.name} — {part.code}")
            total_price += price
            items.append((service_id, part_id, body_part_id, price))

        master_fee = round(total_price * 0.15, 2)

        new_order = Order(
            car_id=car_id,
            description="\n".join(description_lines),
            total_price=total_price + master_fee,
            master_fee=master_fee
        )
        db.session.add(new_order)
        db.session.flush()

        for service_id, part_id, body_part_id, price in items:
            db.session.add(OrderItem(
                order_id=new_order.id,
                service_type_id=service_id,
                part_id=part_id,
                body_part_id=body_part_id,
                price=price
            ))

        db.session.commit()
        print("✅ Заказ сохранён успешно")
        return jsonify(success=True)

    except Exception as e:
        print("❌ ОБЩАЯ ОШИБКА:", e)
        db.session.rollback()
        return jsonify(success=False, message=f"Ошибка: {e}"), 500


@orders_bp.route("/orders/<int:order_id>/mark_done", methods=["POST"])
@login_required
def mark_done(order_id):
    print(f"🛠️ POST на /mark_done: order_id={order_id}")
    order = Order.query.get_or_404(order_id)
    order.status = "выполнено"
    db.session.commit()
    flash("Заказ отмечен как выполненный", "success")
    return redirect(url_for("main.account"))

@orders_bp.route("/orders/<int:order_id>/mark_failed", methods=["POST"])
@login_required
def mark_failed(order_id):
    order = Order.query.get_or_404(order_id)
    reason = request.form.get("reason")
    if not reason:
        flash("Укажите причину отказа", "warning")
        return redirect(url_for("main.account"))
    order.status = "невозможно"
    order.fail_reason = reason
    db.session.commit()
    flash("Заказ отмечен как невозможный", "danger")
    return redirect(url_for("main.account"))