from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get MongoDB URL from environment variable
mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
client = MongoClient(mongodb_url)
db = client.budget_tracker

@app.route('/')
def index():
    expenses = list(db.expenses.find())
    total_income = sum(float(expense.get('amount', 0)) for expense in expenses if expense.get('type') == 'income')
    total_expenses = sum(float(expense.get('amount', 0)) for expense in expenses if expense.get('type') == 'expense')
    balance = total_income - total_expenses
    return render_template('index.html', expenses=expenses, balance=balance)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']
        category = request.form['category']
        date = request.form['date']
        trans_type = request.form['type']

        db.expenses.insert_one({
            'amount': amount,
            'description': description,
            'category': category,
            'date': date,
            'type': trans_type
        })

        return redirect(url_for('index'))

    return render_template('add_expense.html')

@app.route('/view')
def view_expenses():
    expenses = db.expenses.find()
    return render_template('view_expenses.html', expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)