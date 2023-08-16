from flask import request, jsonify, send_from_directory
from app import app,db
from app.models import Income,Expenses,Category
from marshmallow import Schema, fields, validate
from datetime import datetime, date
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import create_access_token

def validate_date_range(value):
    min_date = date(2000, 1, 1)
    max_date = date.today()
    if value < min_date or value > max_date:
        raise ValidationError('Date must be between {} and {}'.format(min_date, max_date))

class RegistrationSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=5,max=50))
    password = fields.Str(required=True, validate=validate.Length(min=5,max=50))

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=5,max=50))
    password = fields.Str(required=True, validate=validate.Length(min=5,max=50))

class IncomeSchema(Schema):
    source = fields.Str(required=True, validate=validate.Length(max=100))
    amount = fields.Float(required=True, validate=validate.Range(min=0)) # No negative numbers
    date = fields.Date(required=True, validate=validate_date_range) # Date range validation
    frequency = fields.Str(required=False, validate=validate.OneOf(["Weekly", "Biweekly", "Monthly", "OneTime"])) # Enumeration

class ExpenseSchema(Schema):
    description = fields.Str(required=True, validate=validate.Length(max=100))
    amount = fields.Float(required=True, validate=validate.Range(min=0))
    date = fields.Date(required=True, validate=validate_date_range)

@app.route('/register', methods=['POST'])
def regiser():
    schema = RegistrationSchema()
    try: 
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    if User.query.filter.by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 401

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    schema = LoginSchema()
    try: 
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user = User.query.filter_by(username=data['username']).first()
    if user is None:
        return jsonify({'message': 'Invalid username or password'}), 401
    if not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=user.username)
    return jsonify({'access_token' : access_token}), 200

@app.route('/income.html')
def income_page():
    return app.send_static_file('income.html')  

@app.route('/expenses.html')
def expenses_page():
    return app.send_static_file('expenses.html')   

@app.route('/api/income', methods=['POST'])
def add_income():
    schema = IncomeSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    source = data['source']
    amount = data['amount']
    date = data['date']
    frequency = data.get('frequency') 

    income = Income(source=source, amount=amount, date=date, frequency=frequency)
    db.session.add(income)
    db.session.commit()

    return jsonify({'message': 'Income added successfully', 'id': income.id}), 201

@app.route('/api/income', methods=['GET'])
def get_incomes():
    incomes = Income.query.all()
    income_list = [{'id': income.id, 'source': income.source, 'amount': income.amount, 'date': income.date.isoformat(), 'frequency': income.frequency} for income in incomes]
    return jsonify(income_list), 200

@app.route('/api/income/<int:id>', methods=['GET'])
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

@app.route('/api/income/<int:id>', methods=['PUT'])
def update_income(id):
    income = Income.query.get(id)
    if income is None:
        return jsonify({'message': 'Income not found'}), 404
    data = request.json
    income.source = data.get('source', income.source)
    income.amount = data.get('amount', income.amount)
    date_str = data.get('date', None)
    if date_str:
        income.date = datetime.strptime(date_str, '%Y-%m-%d').date()
    income.frequency = data.get('frequency', income.frequency)

    db.session.commit()

    return jsonify({'message': 'Income updated successfully'}), 200

@app.route('/api/income/<int:id>', methods=['DELETE'])
def del_income(id):
    income = Income.query.get(id)
    if income is None:
        return jsonify({'message': 'Income not found'}), 404
    db.session.delete(income)
    db.session.commit()

    return jsonify({'message': 'Income deleted successfully'}), 200

@app.route('/api/expenses', methods=['POST'])
def add_expenses():
    schema = ExpenseSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        print(err.messages)
        print(request.json)
        return jsonify(err.messages), 400
    description= data['description']
    amount = data['amount']
    date = data['date']
    category_id = data.get('category_id') # Optional field

    expense = Expenses(description=description, amount=amount, date=date, category_id=category_id)
    db.session.add(expense)
    db.session.commit()

    return jsonify({'message': 'Expense added successfully'}), 201

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    expenses = Expenses.query.all()
    expense_list = [{'id': expense.id,'description': expense.description, 'amount': expense.amount, 'date': expense.date.isoformat(), 'category': expense.category_id} for expense in expenses]
    return jsonify(expense_list), 200

@app.route('/api/expenses/<int:id>', methods=['GET'])
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

@app.route('/api/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    expense = Expenses.query.get(id)
    if expense is None:
        return jsonify({'message': 'Expense not found'}), 404
    data = request.json
    expense.description = data.get('description', expense.description)
    expense.amount = data.get('amount', expense.amount)
    date_str = data.get('date', None)
    if date_str:
        expense.date = datetime.strptime(date_str, '%Y-%m-%d').date()
    expense.category_id = data.get('category_id', expense.category_id)

    db.session.commit()

    return jsonify({'message': 'Expense updated successfully'}), 200

@app.route('/api/expenses/<int:id>', methods=['DELETE'])
def del_expense(id):
    expense = Expenses.query.get(id)
    if expense is None:
        return jsonify({'message': 'Expense not found'}), 404
    db.session.delete(expense)
    db.session.commit()

    return jsonify({'message': 'Expense deleted successfully'}), 200
    
@app.route('/summary.html')
def summary_page():
    return app.send_static_file('summary.html')

@app.route('/api/summary', methods=['GET'])
def get_summary():
    incomes = Income.query.all()
    expenses = Expenses.query.all()

    # Calculate total monthly income
    total_income = 0
    for income in incomes:
        amount = income.amount
        frequency = income.frequency
        if frequency == "Weekly":
            amount *= 4
        elif frequency == "Biweekly":
            amount *= 2
        total_income += amount

    # Calculate total monthly expenses
    total_expenses = sum(expense.amount for expense in expenses)

    # Calculate monthly balance
    monthly_balance = total_income - total_expenses

    summary_data = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'monthly_balance': monthly_balance
    }
    
    return jsonify(summary_data), 200


@app.route('/')
def index():
    return "Welcome to the Budget Tracking API!"