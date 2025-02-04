from flask import Flask, render_template, request, redirect, url_for, session
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class ATM:
    """A simple ATM machine simulation"""

    def __init__(self, initial_balance=5000, pin='1234'):
        self.balance = initial_balance
        self.pin = pin
        self.transaction_history = []

    def check_pin(self, entered_pin):
        if entered_pin == self.pin:
            return True
        return False

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"{datetime.datetime.now()}: Deposited ${amount:.2f}")
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"{datetime.datetime.now()}: Withdrew ${amount:.2f}")
            return True
        return False

    def change_pin(self, new_pin):
        if len(new_pin) == 4 and new_pin.isdigit():
            self.pin = new_pin
            self.transaction_history.append(f"{datetime.datetime.now()}: PIN changed.")
            return True
        return False

    def show_transaction_history(self):
        return self.transaction_history

atm = ATM()  # Initializing the ATM object with default balance and PIN

@app.route('/')
def index():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', balance=atm.balance)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_pin = request.form['pin']
        if atm.check_pin(entered_pin):
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Incorrect PIN. Please try again.")
    return render_template('login.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        if atm.deposit(amount):
            return redirect(url_for('index'))
        else:
            return render_template('deposit.html', error="Invalid deposit amount. Please enter a positive amount.")
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        if atm.withdraw(amount):
            return redirect(url_for('index'))
        else:
            return render_template('withdraw.html', error="Invalid withdrawal amount or insufficient balance.")
    return render_template('withdraw.html')

@app.route('/change_pin', methods=['GET', 'POST'])
def change_pin():
    if request.method == 'POST':
        new_pin = request.form['new_pin']
        if atm.change_pin(new_pin):
            return redirect(url_for('index'))
        else:
            return render_template('change_pin.html', error="Invalid PIN format. PIN must be 4 digits.")
    return render_template('change_pin.html')

@app.route('/transaction_history')
def transaction_history():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    history = atm.show_transaction_history()
    return render_template('transaction_history.html', history=history)

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
