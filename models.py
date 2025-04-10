from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Владельцы(db.Model):
    __tablename__ = 'Владельцы'
    Код_владельца = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Имя = db.Column(db.String(100), nullable=False)
    Фамилия = db.Column(db.String(100), nullable=False)
    Отчество = db.Column(db.String(100), nullable=False)
    Телефон = db.Column(db.String(20), nullable=False)
    Примечание = db.Column(db.String(256), unique=True, nullable=False)
    Логин = db.Column(db.String(50), unique=True, nullable=False)
    Пароль = db.Column(db.String(256), nullable=False)
    Роль = db.Column(db.String(20), nullable=False, default="user")  # user, manager, admin

class МоделиАвто(db.Model):
    __tablename__ = 'МоделиАвто'
    Код_модели = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Марка = db.Column(db.String(40), nullable=False)
    Модель = db.Column(db.String(40), nullable=False)
    Кузов = db.Column(db.String(40), nullable=False)

class Автомобили(db.Model):
    __tablename__ = 'Автомобили'
    Код_автомобиля = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Код_модели = db.Column(db.Integer, db.ForeignKey('МоделиАвто.Код_модели'), nullable=False)
    Код_владельца = db.Column(db.Integer, db.ForeignKey('Владельцы.Код_владельца'), nullable=False)
    Регистрационный_знак = db.Column(db.String(40), nullable=False)
    Год_выпуска = db.Column(db.Integer, nullable=False)
    Примечание = db.Column(db.String(100))
    владелец = db.relationship('Владельцы', backref=db.backref('автомобили', lazy=True))
    модель = db.relationship('МоделиАвто', backref=db.backref('автомобили', lazy=True))

class ВидРабот(db.Model):
    __tablename__ = 'ВидРабот'
    Код_работы = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Название = db.Column(db.String(100), nullable=False)
    Стоимость = db.Column(db.Integer, nullable=False)

class НомерЗапчасти(db.Model):
    __tablename__ = 'НомерЗапчасти'
    Номер_запчасти = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Название = db.Column(db.String(100), nullable=False)
    Цена = db.Column(db.Integer, nullable=False)

class Заказы(db.Model):
    __tablename__ = 'Заказы'
    Код_заказа = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Код_автомобиля = db.Column(db.Integer, db.ForeignKey('Автомобили.Код_автомобиля'), nullable=False)
    Дата_поступления = db.Column(db.Date, nullable=False)
    Код_работы = db.Column(db.Integer, db.ForeignKey('ВидРабот.Код_работы'), nullable=False)
    Номер_запчасти = db.Column(db.Integer, db.ForeignKey('НомерЗапчасти.Номер_запчасти'), nullable=True)
    Количество_запчастей = db.Column(db.Integer)
    Примечание = db.Column(db.String(100))
    Статус = db.Column(db.String(50), default="Ожидает выполнения")  # Выполнен / Закрыт