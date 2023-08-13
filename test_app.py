from app import app, db
from app.models import Category
from flask_testing import TestCase
from datetime import datetime
import unittest

class CategoriesTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()
        test_category = Category(name='Food', description='All food-related expenses')
        db.session.add(test_category)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_categories(self):
        response = self.client.get('/category')
        self.assertEqual(response.status_code, 200)
        categories = response.json
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0]['name'], 'Food')
        self.assertEqual(categories[0]['description'], 'All food-related expenses')



if __name__ == '__main__':
    unittest.main()
