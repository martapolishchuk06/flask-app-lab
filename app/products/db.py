import os
from tinydb import TinyDB

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'products.json')

def get_db():
    return TinyDB(DB_PATH)

def init_db():
    db = get_db()
    products_table = db.table('products')
    if len(products_table) == 0:
        initial_products = [
            {
                "id": 1,
                "name": "Laptop",
                "price": 1200.00,
                "category": "Електроніка",
                "quantity": 10,
                "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам'яті та SSD на 512 ГБ.",
                "image": "images/default.jpg",
                "created_at": "2025-01-01 12:00:00"
            },
            {
                "id": 2,
                "name": "Phone",
                "price": 800.00,
                "category": "Смартфони",
                "quantity": 15,
                "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000 мА·год.",
                "image": "images/default.jpg",
                "created_at": "2025-01-01 12:00:00"
            },
            {
                "id": 3,
                "name": "PC",
                "price": 1800.00,
                "category": "Електроніка",
                "quantity": 5,
                "content": "Настільний комп'ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD.",
                "image": "images/default.jpg",
                "created_at": "2025-01-01 12:00:00"
            }
        ]
        products_table.insert_multiple(initial_products)