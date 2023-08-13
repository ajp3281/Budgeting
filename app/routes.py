from flask import request, jsonify
from app import app,db
from app.models import Income,Expenses,Category
from datetime import datetime

@app.route('/income', methods=['POST'])
def add_income():
    data = request.json
    source = data['source']
    amount = data['amount']
    date_string = data['date']
    date = datetime.strptime(date_string, '%Y-%m-%d').date()
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
    db.session.commit

    return jsonify({'message': 'Income deleted successfully'}), 200

@app.route('/expenses', methods=['POST'])
def add_expenses():
    data = request.json
    description= data['description']
    amount = data['amount']
    date_string = data['date']
    date = datetime.strptime(date_string, '%Y-%m-%d').date()
    category_id = data.get('category_id') # Optional field

    expense = Expenses(description=description, amount=amount, date=date, category_id=category_id)
    db.session.add(expense)
    db.session.commit()

    return jsonify({'message': 'Expense added successfully'}), 201

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expense = Expenses.query.all()
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
    expense.description = data.get('source', expense.description)
    expense.amount = data.get('amount', expense.amount)
    expense.date = data.get('date', expense.date)
    expense.category = data.get('frequency', expense.category_id)

    db.session.commit()

    return jsonify({'message': 'Expense updated successfully'}), 200

@app.route('/expense/<int:id>', methods=['DELETE'])
def del_expense(id):
    expense = Expenses.query.get(id)
    if expense is None:
        return jsonify({'message': 'Expense not found'}), 404
    db.session.delete(expense)
    db.session.commit()

    return jsonify({'message': 'Expense deleted successfully'}), 200

@app.route('/category', methods=['POST'])
def add_category():
    data = request.json
    name= data['name']
    description = data['description']
    category_id = data.get('category_id') 

    category = Category(name=name, description=description, category_id=category_id)
    db.session.add(Category)
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
    db.session.commit

    return jsonify({'message': 'Category deleted successfully'}), 200
    
    


@app.route('/')
def index():
    return "Welcome to the Budget Tracking API!"