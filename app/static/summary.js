const incomeApiUrl = 'http://127.0.0.1:5000/api/income';
const expensesApiUrl = 'http://127.0.0.1:5000/api/expenses';

function calculateMonthlyIncome(incomes) {
  let totalIncome = 0;
  incomes.forEach(income => {
    const amount = income.amount;
    const frequency = income.frequency;
    switch (frequency) {
      case 'Weekly':
        totalIncome += amount * 4;
        break;
      case 'Biweekly':
        totalIncome += amount * 2;
        break;
      case 'Monthly':
      default:
        totalIncome += amount;
        break;
    }
  });
  return totalIncome;
}

function calculateMonthlyExpenses(expenses) {
  return expenses.reduce((total, expense) => total + expense.amount, 0);
}

async function calculateSummary() {
  const incomeResponse = await fetch(incomeApiUrl);
  const incomes = await incomeResponse.json();
  const expensesResponse = await fetch(expensesApiUrl);
  const expenses = await expensesResponse.json();

  const totalIncome = calculateMonthlyIncome(incomes);
  const totalExpenses = calculateMonthlyExpenses(expenses);

  const monthlyBalance = totalIncome - totalExpenses;

  document.getElementById('totalIncome').textContent = totalIncome.toFixed(2);
  document.getElementById('totalExpenses').textContent = totalExpenses.toFixed(2);
  document.getElementById('monthlyBalance').textContent = monthlyBalance.toFixed(2);
}

window.onload = calculateSummary;
