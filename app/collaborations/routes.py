from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.collaborations import bp
from app.forms import CollaborationRequestForm
from app.models import CollaborationRequest, CollaborationApplication, Notification

@bp.route('/')
@login_required
def index():
    requests = CollaborationRequest.query.order_by(CollaborationRequest.timestamp.desc()).all()
    return render_template('collaborations/index.html', title='Collaboration Requests', requests=requests)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CollaborationRequestForm()
    if form.validate_on_submit():
        collab = CollaborationRequest(
            title=form.title.data,
            description=form.description.data,
            skills_required=form.skills_required.data,
            team_size=form.team_size.data,
            author=current_user
        )
        db.session.add(collab)
        db.session.commit()
        flash('Collaboration request posted!', 'success')
        return redirect(url_for('collaborations.index'))
    return render_template('collaborations/create.html', title='Post a Request', form=form)

@bp.route('/<int:id>')
@login_required
def view(id):
    req = CollaborationRequest.query.get_or_404(id)
    return render_template('collaborations/view.html', title=req.title, req=req)

@bp.route('/apply/<int:id>', methods=['POST'])
@login_required
def apply(id):
    req = CollaborationRequest.query.get_or_404(id)
    message = request.form.get('message', '')
    
    existing = CollaborationApplication.query.filter_by(request_id=req.id, applicant_id=current_user.id).first()
    if existing:
        flash('You have already applied for this request.', 'warning')
        return redirect(url_for('collaborations.view', id=req.id))
        
    app = CollaborationApplication(request_id=req.id, applicant_id=current_user.id, message=message)
    db.session.add(app)
    
    notification = Notification(user_id=req.user_id, message=f"{current_user.username} applied to your collaboration request.", link=url_for('collaborations.view', id=req.id))
    db.session.add(notification)
    
    db.session.commit()
    flash('Your application has been sent!', 'success')
    return redirect(url_for('collaborations.view', id=req.id))

@bp.route('/application/<int:app_id>/<action>')
@login_required
def manage_application(app_id, action):
    app = CollaborationApplication.query.get_or_404(app_id)
    if app.request.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('collaborations.index'))
        
    if action == 'approve':
        app.status = 'Approved'
        notification = Notification(user_id=app.applicant_id, message=f"Your application for {app.request.title} was approved!", link=url_for('collaborations.view', id=app.request.id))
    elif action == 'reject':
        app.status = 'Rejected'
        notification = Notification(user_id=app.applicant_id, message=f"Your application for {app.request.title} was rejected.", link=url_for('collaborations.view', id=app.request.id))
    
    if action in ['approve', 'reject']:
        db.session.add(notification)
        db.session.commit()
        flash(f'Application {action}d.', 'success')
        
    return redirect(url_for('collaborations.view', id=app.request.id))
