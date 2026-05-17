from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.posts import bp
from app.forms import PostForm, CommentForm
from app.models import Post, Comment, Like, SavedPost, Notification
from app.users.routes import save_picture

@bp.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = None
        if form.image.data:
            picture_file = save_picture(form.image.data)
        post = Post(content=form.content.data, image=picture_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!', 'success')
        return redirect(url_for('posts.feed'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('posts/feed.html', title='Feed', form=form, posts=posts.items, next_url=posts.next_num if posts.has_next else None, prev_url=posts.prev_num if posts.has_prev else None)

@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        
        if post.user_id != current_user.id:
            notification = Notification(user_id=post.user_id, message=f"{current_user.username} commented on your post.", link=url_for('posts.post', post_id=post.id))
            db.session.add(notification)
            
        db.session.commit()
        flash('Your comment has been added.', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('posts/post.html', title='Post', post=post, form=form)

@bp.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'status': 'unliked', 'likes_count': post.likes.count()})
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        
        if post.user_id != current_user.id:
            notification = Notification(user_id=post.user_id, message=f"{current_user.username} liked your post.", link=url_for('posts.post', post_id=post.id))
            db.session.add(notification)
            
        db.session.commit()
        return jsonify({'status': 'liked', 'likes_count': post.likes.count()})

@bp.route('/save/<int:post_id>', methods=['POST'])
@login_required
def save_post(post_id):
    post = Post.query.get_or_404(post_id)
    saved = SavedPost.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if saved:
        db.session.delete(saved)
        db.session.commit()
        return jsonify({'status': 'unsaved'})
    else:
        new_saved = SavedPost(user_id=current_user.id, post_id=post_id)
        db.session.add(new_saved)
        db.session.commit()
        return jsonify({'status': 'saved'})

@bp.route('/saved')
@login_required
def saved_posts():
    saved_posts = SavedPost.query.filter_by(user_id=current_user.id).order_by(SavedPost.timestamp.desc()).all()
    posts = [saved.post for saved in saved_posts]
    return render_template('posts/saved.html', title='Saved Posts', posts=posts)

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    from sqlalchemy import func
    posts = db.session.query(Post).outerjoin(Like).group_by(Post.id).order_by(func.count(Like.id).desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('posts/explore.html', title='Explore', posts=posts.items)
