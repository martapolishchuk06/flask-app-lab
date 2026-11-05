import pytest
from app import create_app
from app.products.db import get_db

@pytest.fixture
def client():
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        # Ініціалізація тестового запису в базі
        db = get_db()
        table = db.table('products')
        if not table.search(pytest.importorskip("tinydb").Query().id == 1):
            table.insert({
                "id": 1,
                "name": "Laptop",
                "price": 1200.00,
                "category": "Електроніка",
                "quantity": 10,
                "content": "Тестовий опис",
                "image": "uploads/default.jpg",
                "created_at": "2025-01-01 12:00:00"
            })
            
        with app.test_client() as client:
            yield client

def test_list_products(client):
    response = client.get('/products/')
    assert response.status_code == 200

def test_add_product(client):
    response = client.post('/products/add', data={
        'name': 'Тестовий Товар',
        'content': 'Опис тестового товару',
        'price': '99.99',
        'category': 'Електроніка',
        'quantity': 10
    }, follow_redirects=True)
    assert response.status_code == 200

def test_detail_product(client):
    response = client.get('/products/1')
    assert response.status_code == 200

def test_edit_product(client):
    response = client.post('/products/1/edit', data={
        'name': 'Оновлений Ноутбук',
        'content': 'Оновлений опис товару',
        'price': '1500.00',
        'category': 'Електроніка',
        'quantity': 8
    }, follow_redirects=True)
    assert response.status_code == 200

def test_delete_product(client):
    response = client.post('/products/1/delete', follow_redirects=True)
    assert response.status_code == 200