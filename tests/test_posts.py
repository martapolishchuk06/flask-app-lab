import unittest
from app import create_app, db
from app.posts.models import Post

class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        """US01: Створення поста"""
        response = self.client.post('/post/create', data={
            'title': 'Test Post',
            'content': 'Test Content',
            'category': 'news'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)

    def test_list_posts(self):
        """US02: Перегляд списку постів"""
        post = Post(title='Sample Post', content='Content sample', category='tech')
        db.session.add(post)
        db.session.commit()

        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sample Post', response.data)

    def test_view_post_detail(self):
        """US03: Перегляд одного поста"""
        post = Post(title='Detail Post', content='Detail Content', category='publication')
        db.session.add(post)
        db.session.commit()

        response = self.client.get(f'/post/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Detail Content', response.data)

    def test_update_post(self):
        """US04: Редагування поста"""
        post = Post(title='Old Title', content='Old Content', category='news')
        db.session.add(post)
        db.session.commit()

        response = self.client.post(f'/post/{post.id}/update', data={
            'title': 'Updated Title',
            'content': 'Updated Content',
            'category': 'news'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Title', response.data)

    def test_delete_post(self):
        """US05: Видалення поста"""
        post = Post(title='To Delete', content='Content', category='other')
        db.session.add(post)
        db.session.commit()

        response = self.client.post(f'/post/{post.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'To Delete', response.data)

    def test_404_not_found(self):
        """US06: Перевірка 404 при відсутності поста"""
        response = self.client.get('/post/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()