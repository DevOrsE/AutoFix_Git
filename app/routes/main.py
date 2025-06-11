from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from app.extensions import db
from app.models.models import CarModel, Car, Order, Owner, OrderItem
from app.forms.forms import AddCarForm, DeleteCarForm, AdminActionForm
from sqlalchemy.orm import joinedload
from weasyprint import HTML
import tempfile

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/gallery')
def gallery():
    return render_template('gallery.html')

@main_bp.route('/account', methods=["GET", "POST"])
@login_required
def account():
    if current_user.role == "admin":
        users = Owner.query.filter(Owner.id != current_user.id).all()
        admin_form = AdminActionForm()
        return render_template("account_admin.html", users=users, admin_form=admin_form)

    elif current_user.role == "manager":
        sort = request.args.get("sort", "date_desc")
        query = db.session.query(Order).select_from(Order) \
            .join(Car, Order.car_id == Car.id) \
            .join(Owner, Car.owner_id == Owner.id) \
            .add_entity(Car) \
            .add_entity(Owner)

        if sort == "date_asc":
            query = query.order_by(Order.created_at.asc())
        elif sort == "price_desc":
            query = query.order_by(Order.total_price.desc())
        elif sort == "price_asc":
            query = query.order_by(Order.total_price.asc())
        elif sort == "status":
            query = query.order_by(Order.status)
        else:
            query = query.order_by(Order.created_at.desc())

        orders = query.all()
        return render_template("account_manager.html", orders=orders, sort=sort)

    form = AddCarForm()
    form.model_id.choices = [(model.id, model.name) for model in CarModel.query.all()]

    if form.validate_on_submit():
        new_car = Car(
            model_id=form.model_id.data,
            owner_id=current_user.id,
            plate_number=form.plate.data,
            year=form.year.data,
            note=form.note.data
        )
        db.session.add(new_car)
        db.session.commit()
        flash("Автомобиль успешно добавлен!", "success")
        return redirect(url_for('main.account'))

    cars = Car.query.filter_by(owner_id=current_user.id).all()
    orders = Order.query \
    .join(Car) \
    .filter(Car.owner_id == current_user.id) \
    .options(
        joinedload(Order.items).joinedload(OrderItem.part),
        joinedload(Order.items).joinedload(OrderItem.service_type),
        joinedload(Order.items).joinedload(OrderItem.body_part)
    ).all()
    delete_forms = {car.id: DeleteCarForm() for car in cars}

    return render_template(
        'account.html',
        form=form,
        delete_forms=delete_forms,
        cars=cars,
        orders=orders,
        user=current_user
    )

@main_bp.route('/orders/<int:order_id>/receipt')
@login_required
def order_receipt_pdf(order_id):
    order = Order.query.options(
        joinedload(Order.items).joinedload(OrderItem.body_part),
        joinedload(Order.items).joinedload(OrderItem.service_type)
    ).get_or_404(order_id)

    qr_url = url_for('static', filename='images/qr.jpg', _external=True)
    html = render_template("pdf/order_template.html", order=order, qr_path=qr_url)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        HTML(string=html).write_pdf(pdf_file.name)
        return send_file(pdf_file.name,
                         download_name=f"receipt_order_{order.id}.pdf",
                         mimetype="application/pdf")