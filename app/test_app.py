from app import app, db
from app.models import Income
from flask_testing import TestCase

class AppTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a test database
        return app

    def setUp(self):
        db.create_all()
        test_income = Income(source='Salary', amount=5000, date='2022-08-10')
        db.session.add(test_income)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_incomes(self):
        response = self.client.get('/income')
        self.assertEqual(response.status_code, 200)
        incomes = response.json
        self.assertEqual(len(incomes), 1)
        self.assertEqual(incomes[0]['source'], 'Salary')
        self.assertEqual(incomes[0]['amount'], 5000)
        self.assertEqual(incomes[0]['date'], '2022-08-10')

if __name__ == '__main__':
    unittest.main()
