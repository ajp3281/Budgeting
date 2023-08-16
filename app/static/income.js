const apiUrl = 'http://127.0.0.1:5000/api/income';

async function fetchIncomes() {
  const response = await fetch(apiUrl);
  return response.json();
}

async function addIncome() {
  const source = document.getElementById('source').value;
  const amount = document.getElementById('amount').value;
  const date = document.getElementById('date').value;
  const frequency = document.getElementById('frequency').value;

  const incomeData = {
    source,
    amount,
    date,
    frequency,
  };

  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(incomeData),
  });

  if (response.ok) {
    loadIncomes();
  }
}

async function deleteIncome(id) {
  const response = await fetch(`${apiUrl}/${id}`, {
    method: 'DELETE',
  });

  if (response.ok) {
    loadIncomes();
  }
}

async function editIncome(id) {
  const source = document.getElementById('source').value;
  const amount = document.getElementById('amount').value;
  const date = document.getElementById('date').value;
  const frequency = document.getElementById('frequency').value;

  const incomeData = {
    source,
    amount,
    date,
    frequency,
  };

  const response = await fetch(`${apiUrl}/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(incomeData),
  });

  if (response.ok) {
    loadIncomes();
  }
}

// Global variable to hold the current editing income ID
let editingIncomeId = null;

// Function to start editing an income record
async function editIncome(id) {
  // Store the editing ID
  editingIncomeId = id;

  // Fetch the current income data
  const response = await fetch(`${apiUrl}/${id}`);
  const income = await response.json();

  // Fill the edit form with the current values
  document.getElementById('editSource').value = income.source;
  document.getElementById('editAmount').value = income.amount;
  document.getElementById('editDate').value = income.date;
  document.getElementById('editFrequency').value = income.frequency;

  // Show the edit form
  document.getElementById('editForm').style.display = 'block';
}

// Function to submit the edited income record
async function submitEdit() {
  // Get the updated values from the edit form
  const source = document.getElementById('editSource').value;
  const amount = document.getElementById('editAmount').value;
  const date = document.getElementById('editDate').value;
  const frequency = document.getElementById('editFrequency').value;

  // Create the updated income data object
  const incomeData = {
    source,
    amount,
    date,
    frequency,
  };

  // Send the updated income data to the server
  const response = await fetch(`${apiUrl}/${editingIncomeId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(incomeData),
  });

  if (response.ok) {
    loadIncomes();
  }

  // Hide the edit form
  document.getElementById('editForm').style.display = 'none';
}

function cancelEdit() {
  document.getElementById('editForm').style.display = 'none';
}


function loadIncomes() {
  fetchIncomes().then((incomes) => {
    const tableBody = document.getElementById('incomeTableBody');
    tableBody.innerHTML = '';

    incomes.forEach((income) => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${income.source}</td>
        <td>${income.amount}</td>
        <td>${income.date}</td>
        <td>${income.frequency}</td>
        <td><button onclick="editIncome(${income.id})">Edit</button></td>
        <td><button onclick="deleteIncome(${income.id})">Delete</button></td>
      `;
      tableBody.appendChild(row);
    });
  });
}

const monthlyIncomeApiUrl = 'http://127.0.0.1:5000/api/income/monthly';

async function fetchMonthlyIncome() {
  const response = await fetch(monthlyIncomeApiUrl);
  const incomes = await response.json();
  let totalIncome = 0;
  incomes.forEach(income => {
    totalIncome += income.amount;
  });
  document.getElementById('monthlyIncome').innerText = `Total Income for the Month: $${totalIncome}`;
}

window.onload = fetchMonthlyIncome;

window.onload = loadIncomes;


  