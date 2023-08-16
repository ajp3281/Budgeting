const apiUrl = 'http://127.0.0.1:5000/api/expenses';

async function fetchExpenses() {
    const response = await fetch(apiUrl);
    const expenses = await response.json();
    return expenses;
  }
  

async function addExpense() {
  const description = document.getElementById('description').value;
  const amount = document.getElementById('amount').value;
  const date = document.getElementById('date').value;

  const expenseData = {
    description,
    amount,
    date,
  };

  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(expenseData),
  });

  if (response.ok) {
    loadExpenses();
  }
}

async function deleteExpense(id) {
    console.log("Editing expense with ID:", id);
  const response = await fetch(`${apiUrl}/${id}`, {
    method: 'DELETE',
  });
  if (response.ok) {
    loadExpenses();
  }
}

let editingExpenseId = null;

async function editExpense(id) {
  editingExpenseId = id;

  const response = await fetch(`${apiUrl}/${id}`);
  const expense = await response.json();

  document.getElementById('editDescription').value = expense.description;
  document.getElementById('editAmount').value = expense.amount;
  document.getElementById('editDate').value = expense.date;

  document.getElementById('editForm').style.display = 'block';
}

async function submitEdit() {
  const description = document.getElementById('editDescription').value;
  const amount = document.getElementById('editAmount').value;
  const date = document.getElementById('editDate').value;

  const expenseData = {
    description,
    amount,
    date,
  };

  const response = await fetch(`${apiUrl}/${editingExpenseId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(expenseData),
  });

  if (response.ok) {
    loadExpenses();
  }

  document.getElementById('editForm').style.display = 'none';
}

function cancelEdit() {
  document.getElementById('editForm').style.display = 'none';
}

function loadExpenses() {
    console.log("loading expenses")
  fetchExpenses().then((expenses) => {
    const tableBody = document.getElementById('expenseTableBody');
    tableBody.innerHTML = '';

    expenses.forEach((expense) => {
      console.log(expense.id)
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${expense.description}</td>
        <td>${expense.amount}</td>
        <td>${expense.date}</td>
        <td><button onclick="editExpense(${expense.id})">Edit</button></td>
        <td><button onclick="deleteExpense(${expense.id})">Delete</button></td>
      `;
      tableBody.appendChild(row);
    });
  });
}

window.onload = loadExpenses;
