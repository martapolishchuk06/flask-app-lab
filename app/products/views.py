import os
import uuid
from datetime import datetime
from flask import render_template, abort, redirect, url_for, flash, request
from tinydb import Query
from app.products import products_bp, UPLOAD_FOLDER
from .db import get_db
from .forms import ProductForm

def save_image(file):
    """Збереження зображення з унікальним ім'ям UUID та перевіркою розміру."""
    if not file:
        return None
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > 5 * 1024 * 1024:
        return False

    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return f"uploads/{filename}"

@products_bp.route("/")
def list_products():
    """Відображення списку всіх товарів з TinyDB."""
    db = get_db()
    products = db.table('products').all()
    return render_template("products/products.html", products=products)

@products_bp.route("/add", methods=['GET', 'POST'])
def add_product():
    """Додавання нового товару через WTF-форму."""
    form = ProductForm()
    if form.validate_on_submit():
        db = get_db()
        table = db.table('products')
        
        all_items = table.all()
        new_id = max([item['id'] for item in all_items], default=0) + 1
        
        image_path = "uploads/default.jpg"
        if form.image.data:
            saved_path = save_image(form.image.data)
            if saved_path is False:
                flash('Файл занадто великий! Максимальний розмір — 5 МБ.', 'danger')
                return render_template("products/add_product.html", form=form)
            elif saved_path:
                image_path = saved_path

        new_product = {
            "id": new_id,
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_path,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        table.insert(new_product)
        flash('Товар успішно додано!', 'success')
        return redirect(url_for('products.list_products'))

    return render_template("products/add_product.html", form=form)

@products_bp.route("/<int:product_id>")
def detail_product(product_id):
    """Детальний перегляд інформації про товар."""
    db = get_db()
    Product = Query()
    product = db.table('products').get(Product.id == product_id)
    if not product:
        abort(404)
    return render_template("products/detail_product.html", product=product)

@products_bp.route("/<int:product_id>/edit", methods=['GET', 'POST'])
def edit_product(product_id):
    """Редагування товару."""
    db = get_db()
    table = db.table('products')
    Product = Query()
    product = table.get(Product.id == product_id)
    
    if not product:
        abort(404)
        
    if request.method == 'GET':
        form = ProductForm(data=product)
    else:
        form = ProductForm()

    if form.validate_on_submit():
        image_path = product.get('image', 'uploads/default.jpg')
        if form.image.data:
            saved_path = save_image(form.image.data)
            if saved_path is False:
                flash('Файл занадто великий! Максимальний розмір — 5 МБ.', 'danger')
                return render_template("products/edit_product.html", form=form, product=product)
            elif saved_path:
                image_path = saved_path

        updated_data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_path
        }
        
        table.update(updated_data, Product.id == product_id)
        flash('Товар успішно оновлено!', 'success')
        return redirect(url_for('products.detail_product', product_id=product_id))

    return render_template("products/edit_product.html", form=form, product=product)

@products_bp.route("/<int:product_id>/delete", methods=['POST'])
def delete_product(product_id):
    """Видалення товару за POST-запитом."""
    db = get_db()
    table = db.table('products')
    Product = Query()
    if not table.search(Product.id == product_id):
        abort(404)
        
    table.remove(Product.id == product_id)
    flash('Товар успішно видалено!', 'warning')
    return redirect(url_for('products.list_products'))