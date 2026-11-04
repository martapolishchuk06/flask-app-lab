import os
from flask import Blueprint
from .db import init_db

products_bp = Blueprint('products', __name__, template_folder='templates', static_folder='static', url_prefix='/products')

UPLOAD_FOLDER = os.path.join(products_bp.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

from . import views