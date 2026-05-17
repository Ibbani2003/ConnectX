import os
import secrets
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.users import bp
from app.forms import UpdateProfileForm
from app.models import User, Post

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@bp.route('/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('users/profile.html', user=user, posts=posts)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        if form.profile_image.data:
            picture_file = save_picture(form.profile_image.data)
            current_user.profile_image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.full_name = form.full_name.data
        current_user.bio = form.bio.data
        current_user.college_name = form.college_name.data
        current_user.department = form.department.data
        current_user.skills = form.skills.data
        current_user.github_link = form.github_link.data
        current_user.linkedin_link = form.linkedin_link.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('users.profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.full_name.data = current_user.full_name
        form.bio.data = current_user.bio
        form.college_name.data = current_user.college_name
        form.department.data = current_user.department
        form.skills.data = current_user.skills
        form.github_link.data = current_user.github_link
        form.linkedin_link.data = current_user.linkedin_link
    return render_template('users/edit_profile.html', title='Edit Profile', form=form)

@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.', 'danger')
        return redirect(url_for('posts.feed'))
    if user == current_user:
        flash('You cannot follow yourself!', 'warning')
        return redirect(url_for('users.profile', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are following {username}!', 'success')
    return redirect(url_for('users.profile', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.', 'danger')
        return redirect(url_for('posts.feed'))
    if user == current_user:
        flash('You cannot unfollow yourself!', 'warning')
        return redirect(url_for('users.profile', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You are not following {username}.', 'info')
    return redirect(url_for('users.profile', username=username))

@bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    if query:
        users = User.query.filter(User.username.ilike(f'%{query}%') | User.full_name.ilike(f'%{query}%')).all()
    else:
        users = []
    return render_template('users/search.html', title='Search Users', users=users, query=query)
