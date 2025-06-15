from wtforms.validators import EqualTo, Optional
from flask_wtf.recaptcha import RecaptchaField
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length
from app.models.models import CarModel
from wtforms.validators import Regexp
from wtforms import SelectField
from datetime import datetime

year_choices = [(str(y), str(y)) for y in range(2001, datetime.now().year + 1)]

class RegistrationForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    phone = StringField("Phone", validators=[Length(min=5, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')])
    recaptcha = RecaptchaField()  # 👈 добавили
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    recaptcha = RecaptchaField()  # 👈 добавили
    submit = SubmitField("Log In")

class AdminActionForm(FlaskForm):
    role = SelectField("Роль", choices=[("user", "User"), ("manager", "Manager"), ("admin", "Admin")], validators=[DataRequired()])
    submit = SubmitField("Изменить")

class RegistrationForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    phone = StringField("Phone", validators=[Length(min=5, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[
    DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class OrderForm(FlaskForm):
    car_id = SelectField("Машина", coerce=int, validators=[DataRequired()])
    service_type_id = SelectField("Тип услуги", coerce=int, validators=[DataRequired()])
    part_number_id = SelectField("Номер запчасти (необязательно)", coerce=int, validators=[Optional()])
    description = TextAreaField("Описание", validators=[DataRequired()])
    submit = SubmitField("Оформить заказ")

class CarForm(FlaskForm):
    model_id = SelectField('Модель автомобиля', coerce=int, validators=[DataRequired()])
    plate = StringField("Госномер", validators=[
        DataRequired(),
        Regexp(r'^[А-Яа-я]{2}\d{3}[А-Яа-я]$', message="Формат: две буквы, три цифры, одна буква. Пример: НЕ467А")
    ])
    year = SelectField("Год выпуска", choices=year_choices)
    note = TextAreaField('Заметка')
    submit = SubmitField('Добавить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_id.choices = [(m.id, m.name) for m in CarModel.query.order_by(CarModel.name).all()]

class DeleteCarForm(FlaskForm):
    pass  # только CSRF токен

class EmptyForm(FlaskForm):
    pass