from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.models import Owner
from app.extensions import db
from app.decorators import admin_required

# Важно: имя должно быть "admin", чтобы работал url_for('admin.change_role')
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/users")
@login_required
@admin_required
def users():
    users = Owner.query.filter(Owner.id != current_user.id).all()
    return render_template("account_admin.html", users=users)

@admin_bp.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = Owner.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("❌ Вы не можете удалить себя", "warning")
        return redirect(url_for("main.account"))

    if user.cars:
        flash("🚫 Невозможно удалить пользователя с зарегистрированными автомобилями", "danger")
        return redirect(url_for("main.account"))

    db.session.delete(user)
    db.session.commit()
    flash("✅ Пользователь успешно удалён", "success")
    return redirect(url_for("main.account"))


@admin_bp.route("/admin/change_role/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def change_role(user_id):
    user = Owner.query.get_or_404(user_id)
    new_role = request.form.get("role")

    if new_role in ["user", "manager", "admin"]:
        user.role = new_role
        db.session.commit()
        flash(f"✅ Роль пользователя обновлена на '{new_role}'", "success")
    else:
        flash("❌ Недопустимая роль", "danger")

    return redirect(url_for("main.account"))
