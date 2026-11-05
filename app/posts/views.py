from flask import render_template, redirect, url_for, flash, request
from app import db
from app.posts import post_bp
from app.posts.models import Post
from app.posts.forms import PostForm

@post_bp.route('/')
def list_posts():
    posts = db.session.scalars(db.select(Post).order_by(Post.posted.desc())).all()
    return render_template('posts/index.html', posts=posts, title="Список постів")

@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.list_posts'))
    return render_template('posts/create_post.html', form=form, title="Створити пост")

@post_bp.route('/<int:id>')
def show_post(id):
    post = db.get_or_404(Post, id)
    return render_template('posts/post_detail.html', post=post, title=post.title)

@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        db.session.commit()
        flash('Пост успішно оновлено!', 'info')
        return redirect(url_for('posts.show_post', id=post.id))
    return render_template('posts/edit_post.html', form=form, post=post, title="Редагувати пост")

@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Пост успішно видалено!', 'danger')
        return redirect(url_for('posts.list_posts'))
    return render_template('posts/confirm_delete.html', post=post, title="Видалення поста")