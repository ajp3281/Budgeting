from flask import request, jsonify
from app import app,db
from app.models import Income,Expenses,Category
from marshmallow import Schema, fields, validate
from datetime import datetime, date
from marshmallow.exceptions import ValidationError

def validate_date_range(value):
    min_date = date(2000, 1, 1)
    max_date = date.today()
    if value < min_date or value > max_date:
        raise ValidationError('Date must be between {} and {}'.format(min_date, max_date))

class IncomeSchema(Schema):
    source = fields.Str(required=True, validate=validate.Length(max=100))
    amount = fields.Float(required=True, validate=validate.Range(min=0)) # No negative numbers
    date = fields.Date(required=True, validate=validate_date_range) # Date range validation
    frequency = fields.Str(required=False, validate=validate.OneOf(["Weekly", "Biweekly", "Monthly", "Yearly"])) # Enumeration

class ExpenseSchema(Schema):
    description = fields.Str(required=True, validate=validate.Length(max=100))
    amount = fields.Float(required=True, validate=validate.Range(min=0))
    date = fields.Date(required=True, validate=validate_date_range) 
    category_id = fields.Str(required=True, validate=validate.Length(max=100))

class CategorySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=50))
    description = fields.Str(required=True, validate=validate.Length(max=200))

@app.route('/income', methods=['POST'])
def add_income():
    schema = IncomeSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    source = data['source']
    amount = data['amount']
    date = data['date']
    frequency = data.get('frequency') # Optional field

    income = Income(source=source, amount=amount, date=date, frequency=frequency)
    db.session.add(income)
    db.session.commit()

    return jsonify({'message': 'Income added successfully', 'id': income.id}), 201

@app.route('/income', methods=['GET'])
def get_incomes():
    incomes = Income.query.all()
    income_list = [{'source': income.source, 'amount': income.amount, 'date': income.date.isoformat(), 'frequency': income.frequency} for income in incomes]
    return jsonify(income_list), 200

@app.route('/income/<int:id>', methods=['GET'])
def search_income(id):
    income = Income.query.get(id)
    if income is None:
        abort(404)
    income_data = {
        'source': income.source,
        'amount': income.amount,
        'date': income.date.isoformat(),
        'frequency': income.frequency
    }
    return jsonify(income_data), 200

@app.route('/income/<int:id>', methods=['PUT'])
def update_income(id):
    income = Income.query.get(id)
    if income is None:
        return jsonify({'message': 'Income not found'}), 404
    data = request.json
    income.source = data.get('source', income.source)
    income.amount = data.get('amount', income.amount)
    income.date = data.get('date', income.date)
    income.frequency = data.get('frequency', income.frequency)

    db.session.commit()

    return jsonify({'message': 'Income updated successfully'}), 200

@app.route('/income/<int:id>', methods=['DELETE'])
def del_income(id):
    income = Income.query.get(id)
    if income is None:
        return jsonify({'message': 'Income not found'}), 404
    db.session.delete(income)
    db.session.commit()

    return jsonify({'message': 'Income deleted successfully'}), 200

@app.route('/expenses', methods=['POST'])
def add_expenses():
    schema = ExpenseSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    description= data['description']
    amount = data['amount']
    date = data['date']
    category_id = data.get('category_id') # Optional field

    expense = Expenses(description=description, amount=amount, date=date, category_id=category_id)
    db.session.add(expense)
    db.session.commit()

    return jsonify({'message': 'Expense added successfully'}), 201

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expenses.query.all()
    expense_list = [{'description': expense.description, 'amount': expense.amount, 'date': expense.date.isoformat(), 'category': expense.category_id} for expense in expenses]
    return jsonify(expense_list), 200

@app.route('/expenses/<int:id>', methods=['GET'])
def search_expense(id):
    expense = Expenses.query.get(id)
    if expense is None:
        abort(404)
    expense_data = {
        'description': expense.description,
        'amount': expense.amount,
        'date': expense.date.isoformat(),
        'category': expense.category_id
    }
    return jsonify(expense_data), 200

@app.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    expense = Expenses.query.get(id)
    if expense is None:
        return jsonify({'message': 'Expense not found'}), 404
    data = request.json
    expense.description = data.get('description', expense.description)
    expense.amount = data.get('amount', expense.amount)
    expense.date = data.get('date', expense.date)
    expense.category_id = data.get('category_id', expense.category_id)

    db.session.commit()

    return jsonify({'message': 'Expense updated successfully'}), 200

@app.route('/expenses/<int:id>', methods=['DELETE'])
def del_expense(id):
    expense = Expenses.query.get(id)
    if expense is None:
        return jsonify({'message': 'Expense not found'}), 404
    db.session.delete(expense)
    db.session.commit()

    return jsonify({'message': 'Expense deleted successfully'}), 200

@app.route('/category', methods=['POST'])
def add_category():
    schema = CategorySchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    name= data['name']
    description = data['description']
    category_id = data.get('category_id') 

    category = Category(name=name, description=description, category_id=category_id)
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category added successfully'}), 201

@app.route('/category', methods=['GET'])
def get_category():
    category = Category.query.all()
    category_list = [{'name': category.name, 'description': category.description} for category in category]
    return jsonify(category_list), 200

@app.route('/category/<int:id>', methods=['GET'])
def search_category(id):
    category = Category.query.get(id)
    if category is None:
        abort(404)
    category_data = {
        'name': category.name,
        'description': category.description,
    }
    return jsonify(category_data), 200

@app.route('/category/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if category is None:
        return jsonify({'message': 'Category not found'}), 404
    data = request.json
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)

    db.session.commit()

    return jsonify({'message': 'Category updated successfully'}), 200

@app.route('/category/<int:id>', methods=['DELETE'])
def del_category(id):
    category = Category.query.get(id)
    if category is None:
        return jsonify({'message': 'Category not found'}), 404
    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': 'Category deleted successfully'}), 200
    
    


@app.route('/')
def index():
    return "Welcome to the Budget Tracking API!"