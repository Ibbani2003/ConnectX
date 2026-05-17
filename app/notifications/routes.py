from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.notifications import bp
from app.models import Notification

@bp.route('/')
@login_required
def index():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    return render_template('notifications/index.html', title='Notifications', notifications=notifications)

@bp.route('/read/<int:id>')
@login_required
def read(id):
    notification = Notification.query.get_or_404(id)
    if notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
        if notification.link:
            return redirect(notification.link)
    return redirect(url_for('notifications.index'))
