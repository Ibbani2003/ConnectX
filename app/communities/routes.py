from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.communities import bp
from app.forms import CommunityForm, PostForm
from app.models import Community, Post
from app.users.routes import save_picture

@bp.route('/')
@login_required
def list_communities():
    communities = Community.query.all()
    return render_template('communities/list.html', title='Communities', communities=communities)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CommunityForm()
    if form.validate_on_submit():
        community = Community(name=form.name.data, description=form.description.data, creator_id=current_user.id)
        community.members.append(current_user)
        db.session.add(community)
        db.session.commit()
        flash('Community created successfully!', 'success')
        return redirect(url_for('communities.view', id=community.id))
    return render_template('communities/create.html', title='Create Community', form=form)

@bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def view(id):
    community = Community.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit() and current_user in community.members:
        picture_file = None
        if form.image.data:
            picture_file = save_picture(form.image.data)
        post = Post(content=form.content.data, image=picture_file, author=current_user, community=community)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live in the community!', 'success')
        return redirect(url_for('communities.view', id=community.id))
    posts = community.posts.order_by(Post.timestamp.desc()).all()
    return render_template('communities/view.html', title=community.name, community=community, form=form, posts=posts)

@bp.route('/join/<int:id>')
@login_required
def join(id):
    community = Community.query.get_or_404(id)
    if current_user not in community.members:
        community.members.append(current_user)
        db.session.commit()
        flash(f'You joined {community.name}!', 'success')
    return redirect(url_for('communities.view', id=community.id))

@bp.route('/leave/<int:id>')
@login_required
def leave(id):
    community = Community.query.get_or_404(id)
    if current_user in community.members:
        community.members.remove(current_user)
        db.session.commit()
        flash(f'You left {community.name}.', 'info')
    return redirect(url_for('communities.view', id=community.id))
