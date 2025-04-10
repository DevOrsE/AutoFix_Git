from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Автомобили, НомерЗапчасти, ВидРабот, Заказы, Владельцы
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-super-secret-key'

SQLALCHEMY_DATABASE_URI = (
    'mssql+pyodbc://DevOrsE:DevOrsE#2025@localhost/Database_fixauto?driver=ODBC+Driver+17+for+SQL+Server'
)
# Trusted connection to SQL Server (Windows auth)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://DevOrsE:DevOrsE#2025@localhost/Database_fixauto?driver=ODBC+Driver+17+for+SQL+Server'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.context_processor
def inject_user():
    user = None
    if "user_id" in session:
        user = Владельцы.query.filter_by(Код_владельца=session["user_id"]).first()
    return dict(current_user=user)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/reviews")
def reviews():
    return render_template("reviews.html")

@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        action = request.form.get("action")
        login = request.form.get("login")
        password = request.form.get("password")

        if action == "login":
            user = Владельцы.query.filter_by(Логин=login).first()
            if user and check_password_hash(user.Пароль, password):
                session["user_id"] = user.Код_владельца
                flash("Успешный вход!", "success")
                return redirect(url_for("account"))
            else:
                flash("Неверный логин или пароль", "danger")

        elif action == "register":
            if Владельцы.query.filter_by(Логин=login).first():
                flash("Пользователь с таким логином уже существует", "danger")
            else:
                try:
                    new_user = Владельцы(
                        Фамилия=request.form.get("last_name"),
                        Имя=request.form.get("first_name"),
                        Отчество="-",
                        Телефон=request.form.get("phone"),
                        Примечание="-",
                        Логин=login,
                        Пароль=generate_password_hash(password)
                    )
                    db.session.add(new_user)
                    db.session.commit()

                    # 🔐 Автоматический вход после регистрации
                    session["user_id"] = new_user.Код_владельца
                    flash("Регистрация успешна! Вы вошли в аккаунт", "success")
                    return redirect(url_for("account"))
                except Exception as e:
                    db.session.rollback()
                    flash(f"Ошибка при регистрации: {e}", "danger")

    return render_template("auth.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из аккаунта.", "info")
    return redirect(url_for("index"))

@app.route("/account", methods=["GET", "POST"])
def account():
    if "user_id" not in session:
        flash("Пожалуйста, войдите в аккаунт", "warning")
        return redirect(url_for("auth"))

    user = Владельцы.query.get(session["user_id"])
    cars = Автомобили.query.filter_by(Код_владельца=user.Код_владельца).all()

    # Получаем уникальные марки и кузова из таблицы Автомобили
    unique_brands = db.session.query(МоделиАвто.Марка).distinct().all()
    unique_bodies = db.session.query(МоделиАвто.Кузов).distinct().all()
    unique_brands = [row[0] for row in unique_brands]
    unique_bodies = [row[0] for row in unique_bodies]

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "add":
            # Добавление нового авто
            new_car = Автомобили(
                Марка_автомобиля=request.form.get("brand"),
                Код_владельца=user.Код_владельца,
                Регистрационный_знак=request.form.get("plate"),
                Год_выпуска=int(request.form.get("year")),
                Кузов=request.form.get("body"),
                Примечание=request.form.get("note") or "-"
            )
            db.session.add(new_car)
            db.session.commit()
            flash("Автомобиль добавлен", "success")

        elif form_type == "edit":
            # Редактирование авто
            car_id = int(request.form.get("car_id"))
            car = Автомобили.query.get_or_404(car_id)

            if car.Код_владельца != user.Код_владельца:
                flash("Нет доступа к этому автомобилю", "danger")
                return redirect(url_for("account"))

            car.Марка_автомобиля = request.form.get("brand")
            car.Регистрационный_знак = request.form.get("plate")
            car.Год_выпуска = int(request.form.get("year"))
            car.Кузов = request.form.get("body")
            car.Примечание = request.form.get("note")
            db.session.commit()
            flash("Данные авто обновлены", "success")

        return redirect(url_for("account"))

    return render_template(
        "account.html",
        user=user,
        cars=cars,
        unique_brands=unique_brands,
        unique_bodies=unique_bodies
    )

@app.route("/order", methods=["GET", "POST"])
def order():
    if "user_id" not in session:
        flash("Войдите в аккаунт", "warning")
        return redirect(url_for("auth"))

    cars = Автомобили.query.filter_by(Код_владельца=session["user_id"]).all()
    parts = НомерЗапчасти.query.all()
    works = ВидРабот.query.all()
    success = False

    if request.method == "POST":
        new_order = Заказы(
            Код_автомобиля=request.form.get("car_id"),
            Дата_поступления=date.today(),
            Код_работы=request.form.get("repair_id"),
            Номер_запчасти=request.form.get("part_id"),
            Количество_запчастей=int(request.form.get("qty")),
            Примечание=request.form.get("note")
        )
        try:
            db.session.add(new_order)
            db.session.commit()
            success = True
        except Exception:
            db.session.rollback()
            flash("Ошибка при оформлении заказа", "danger")

    return render_template("order.html", cars=cars, parts=parts, works=works, success=success)

if __name__ == "__main__":
    app.run(debug=True)