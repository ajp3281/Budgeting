from app import app, db
from app.models import User
from flask_testing import TestCase
import unittest
import json

class AuthTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_auth.db'  # Use a test database for auth
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_registration(self):
        # Test registration with valid data
        response = self.client.post('/register',
                                    data=json.dumps({
                                        'username': 'testuser',
                                        'password': 'testpassword'
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.json['message'])

        # Test registration with existing username
        response = self.client.post('/register',
                                    data=json.dumps({
                                        'username': 'testuser',
                                        'password': 'anotherpassword'
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already exists', response.json['message'])

    def test_login(self):
        # Register user first
        self.client.post('/register',
                         data=json.dumps({
                             'username': 'testuser',
                             'password': 'testpassword'
                         }),
                         content_type='application/json')

        # Test login with valid credentials
        response = self.client.post('/login',
                                    data=json.dumps({
                                        'username': 'testuser',
                                        'password': 'testpassword'
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

        # Test login with invalid credentials
        response = self.client.post('/login',
                                    data=json.dumps({
                                        'username': 'testuser',
                                        'password': 'wrongpassword'
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Password is invalid', response.json['message'])

if __name__ == '__main__':
    unittest.main()
