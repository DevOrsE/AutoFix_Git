from flask_login import current_user
from flask import redirect, url_for, flash
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Доступ только для администратора.", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'manager':
            flash("Доступ только для менеджера.", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated_function
