from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Optional
from flask_wtf.recaptcha import RecaptchaField

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

class AddCarForm(FlaskForm):
    model_id = SelectField('Model', coerce=int, validators=[DataRequired()])
    plate = StringField('Plate number', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    note = TextAreaField('Note')
    submit = SubmitField('Add Car')

class DeleteCarForm(FlaskForm):
    pass  # только CSRF токен

class EmptyForm(FlaskForm):
    pass