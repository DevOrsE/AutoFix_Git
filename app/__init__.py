# app/__init__.py
from flask import Flask
from app.settings import Config
from app.extensions import csrf, db, login_manager
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.cars import cars_bp
from app.routes.orders import orders_bp, confirm_order
from app.routes.admin_routes import admin_bp
from app.models.models import Owner

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 👇 Настройки для капчи
    app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc0oDgrAAAAAIhJrb9_xCx-_-7WvmOnKYkduJLc'
    app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc0oDgrAAAAAJyghoxzOwimuKh5llagMXxEMfLl'
    app.config['RECAPTCHA_PARAMETERS'] = {'hl': 'ru'}

    csrf.init_app(app)
    csrf.exempt(confirm_order)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return Owner.query.get(int(user_id))

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cars_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)

    return app