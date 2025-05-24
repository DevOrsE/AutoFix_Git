# app/routes/__init__.py
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.cars import cars_bp

"""
Пакет маршрутов:
- main.py — главная, галерея, отзывы
- auth.py — авторизация, регистрация
- cars.py — управление автомобилями
"""