from flask import render_template
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html', title='Welcome to ConnectX')

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    from app.extensions import db
    db.session.rollback()
    return render_template('500.html'), 500
