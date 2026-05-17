from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.messages import bp
from app.forms import MessageForm
from app.models import Message, User, Notification
from sqlalchemy import or_, and_

@bp.route('/')
@login_required
def inbox():
    messages = Message.query.filter(
        or_(Message.recipient_id == current_user.id, Message.sender_id == current_user.id)
    ).order_by(Message.timestamp.desc()).all()
    
    # Get unique users conversed with
    users_dict = {}
    for msg in messages:
        other_user = msg.sender if msg.recipient_id == current_user.id else msg.recipient
        if other_user.id not in users_dict:
            users_dict[other_user.id] = {'user': other_user, 'last_message': msg}
            
    conversations = list(users_dict.values())
    return render_template('messages/inbox.html', title='Messages', conversations=conversations)

@bp.route('/<username>', methods=['GET', 'POST'])
@login_required
def chat(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        flash('You cannot message yourself.', 'warning')
        return redirect(url_for('messages.inbox'))
        
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.body.data)
        db.session.add(msg)
        
        notification = Notification(user_id=user.id, message=f"New message from {current_user.username}", link=url_for('messages.chat', username=current_user.username))
        db.session.add(notification)
        
        db.session.commit()
        return redirect(url_for('messages.chat', username=username))
        
    messages = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.recipient_id == user.id),
            and_(Message.sender_id == user.id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.timestamp.asc()).all()
    
    # Mark messages as read
    for msg in messages:
        if msg.recipient_id == current_user.id and not msg.is_read:
            msg.is_read = True
    db.session.commit()
    
    return render_template('messages/chat.html', title=f'Chat with {username}', user=user, messages=messages, form=form)
