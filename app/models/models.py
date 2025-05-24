# app/models/models.py
from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class Owner(UserMixin, db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default="user")
    cars = db.relationship("Car", backref="owner", cascade="all, delete-orphan")


class CarModel(db.Model):
    __tablename__ = 'car_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cars = db.relationship('Car', backref='model', lazy=True)


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('car_models.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    plate_number = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer)
    note = db.Column(db.Text)

    # ✅ Удалили car = ... в Order, поэтому оставляем backref здесь
    orders = db.relationship('Order', backref='car', lazy=True, cascade="all, delete-orphan")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String, default="ожидает")
    fail_reason = db.Column(db.String, nullable=True)
    total_price = db.Column(db.Float, nullable=False)
    master_fee = db.Column(db.Float, nullable=False)

    # ❌ Удалено:
    # car = db.relationship("Car", backref="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class ServiceType(db.Model):
    __tablename__ = 'service_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


class PartNumber(db.Model):
    __tablename__ = 'part_numbers'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey("part_numbers.id"), nullable=False)
    service_type_id = db.Column(db.Integer, db.ForeignKey("service_types.id"), nullable=False)
    body_part_id = db.Column(db.Integer, db.ForeignKey("body_parts.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)

    order = db.relationship("Order", back_populates="items")
    part = db.relationship("PartNumber", backref="order_items")
    service_type = db.relationship("ServiceType", backref="order_items")
    body_part = db.relationship("BodyPart", back_populates="order_items")


class BodyPart(db.Model):
    __tablename__ = "body_parts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    order_items = db.relationship("OrderItem", back_populates="body_part")
