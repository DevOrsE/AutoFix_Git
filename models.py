from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Автомобили(db.Model):
    __tablename__ = 'Автомобили'
    Код_автомобиля = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Марка_автомобиля = db.Column(db.String(40), nullable=False)
    Код_владельца = db.Column(db.Integer, db.ForeignKey('Владельцы.Код_владельца'), nullable=False)
    Регистрационный_знак = db.Column(db.String(40), nullable=False)
    Год_выпуска = db.Column(db.Integer, nullable=False)
    Кузов = db.Column(db.String(40), nullable=False)
    Примечание = db.Column(db.String(40), nullable=False)

class Владельцы(db.Model):
    __tablename__ = 'Владельцы'
    Код_владельца = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Фамилия = db.Column(db.String(50))
    Имя = db.Column(db.String(50))
    Отчество = db.Column(db.String(50))
    Терефон = db.Column(db.String(20))
    Примечание = db.Column(db.String(100))
    Логин = db.Column(db.String(50), unique=True)
    Пароль = db.Column(db.String(256))

class НомерЗапчасти(db.Model):
    __tablename__ = 'Номер_запчасти'
    Номер_запчасти = db.Column(db.Integer, primary_key=True)
    Наименование = db.Column(db.String(40), nullable=False)
    Стоймость = db.Column(db.Float, nullable=False)
    Гарантия = db.Column(db.Integer, nullable=False)

class ВидРабот(db.Model):
    __tablename__ = 'Вид_работ'
    Код_работы = db.Column(db.Integer, primary_key=True)
    Наименование = db.Column(db.String(40), nullable=False)
    Стоймость_работ = db.Column(db.Float, nullable=False)
    Срок_выполнения = db.Column(db.Integer, nullable=False)
    Гарантия = db.Column(db.Integer, nullable=False)

class Заказы(db.Model):
    __tablename__ = 'Заказы'
    Номер_заказа = db.Column(db.Integer, primary_key=True)
    Код_автомобиля = db.Column(db.Integer, db.ForeignKey('Автомобили.Код_автомобиля'), nullable=False)
    Дата_поступления = db.Column(db.Date, nullable=False)
    Код_работы = db.Column(db.Integer, db.ForeignKey('Вид_работ.Код_работы'), nullable=False)
    Номер_запчасти = db.Column(db.Integer, db.ForeignKey('Номер_запчасти.Номер_запчасти'), nullable=False)
    Количество_запчастей = db.Column(db.Integer, nullable=False)
    Примечание = db.Column(db.String(40), nullable=False)