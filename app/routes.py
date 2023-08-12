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

@app.route('/income<int:id'>, methods=['DELETE'])
def del_income(id):
    income = Income.query.get(id)
    if income is None:
        return jsonify({'message': 'Income not found'}), 404
    db.session.delete(income)
    db.session.commit

    return jsonify({'message': 'Income deleted successfully'}), 200
    
    


@app.route('/')
def index():
    return "Welcome to the Budget Tracking API!"