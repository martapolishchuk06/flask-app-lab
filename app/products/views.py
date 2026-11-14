import os
import uuid
from flask import render_template, redirect, url_for, flash, request
from app import db
from app.products import products_bp, UPLOAD_FOLDER
from .models import Product
from .forms import ProductForm

def save_image(file):
    """Збереження зображення з унікальним ім'ям UUID та перевіркою розміру."""
    if not file or not file.filename:
        return None
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > 5 * 1024 * 1024:
        return False

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return f"uploads/{filename}"

@products_bp.route("/")
def list_products():
    """Відображення списку всіх товарів з бази даних."""
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("products/products.html", products=products)

@products_bp.route("/add", methods=['GET', 'POST'])
def add_product():
    """Додавання нового товару через WTF-форму."""
    form = ProductForm()
    if form.validate_on_submit():
        image_path = "uploads/default.jpg"
        if form.image.data:
            saved_path = save_image(form.image.data)
            if saved_path is False:
                flash('Файл занадто великий! Максимальний розмір — 5 МБ.', 'danger')
                return render_template("products/add_product.html", form=form)
            elif saved_path:
                image_path = saved_path

        new_product = Product(
            name=form.name.data,
            content=form.content.data,
            price=float(form.price.data),
            category=form.category.data,
            quantity=form.quantity.data,
            image=image_path
        )
        
        db.session.add(new_product)
        db.session.commit()
        flash('Товар успішно додано!', 'success')
        return redirect(url_for('products.list_products'))

    return render_template("products/add_product.html", form=form)

@products_bp.route("/<int:product_id>")
def detail_product(product_id):
    """Детальний перегляд інформації про товар."""
    product = Product.query.get_or_404(product_id)
    return render_template("products/detail_product.html", product=product)

@products_bp.route("/<int:product_id>/edit", methods=['GET', 'POST'])
def edit_product(product_id):
    """Редагування товару."""
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        image_path = product.image or "uploads/default.jpg"
        if form.image.data and getattr(form.image.data, 'filename', None):
            saved_path = save_image(form.image.data)
            if saved_path is False:
                flash('Файл занадто великий! Максимальний розмір — 5 МБ.', 'danger')
                return render_template("products/edit_product.html", form=form, product=product)
            elif saved_path:
                image_path = saved_path

        product.name = form.name.data
        product.content = form.content.data
        product.price = float(form.price.data)
        product.category = form.category.data
        product.quantity = form.quantity.data
        product.image = image_path

        db.session.commit()
        flash('Товар успішно оновлено!', 'success')
        return redirect(url_for('products.detail_product', product_id=product.id))

    return render_template("products/edit_product.html", form=form, product=product)

@products_bp.route("/<int:product_id>/delete", methods=['POST'])
def delete_product(product_id):
    """Видалення товару за POST-запитом."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Товар успішно видалено!', 'warning')
    return redirect(url_for('products.list_products'))