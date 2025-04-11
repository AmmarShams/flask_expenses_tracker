from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable = False)
    category = db.Column(db.String(100), nullable = False)
    notes = db.Column(db.String(300), nullable = True)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return 'Expense %r' % self.id


@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        notes = request.form['notes']
        new_expense = Expenses(amount=amount,category=category,notes=notes)

        try:
            db.session.add(new_expense)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem adding this expense '
    else:
        categories = db.session.query(Expenses.category).distinct().all()
        expenses = Expenses.query.order_by(Expenses.date_created).all()
        return render_template('index.html', expenses = expenses, categories= categories)


@app.route('/delete/<int:id>')
def delete(id):
    expense_to_be_deleted = Expenses.query.get_or_404(id)

    try:
        db.session.delete(expense_to_be_deleted)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem removing this expense'


@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    expense_to_be_updated = Expenses.query.get_or_404(id)
    if request.method == 'POST':
        
        expense_to_be_updated.amount = request.form['amount']
        expense_to_be_updated.category = request.form['category']
        expense_to_be_updated.notes = request.form['notes']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating this expense'
    else:
        return render_template('update.html', expense = expense_to_be_updated)   
    


@app.route('/filter', methods = ['GET'])
def filter():
    selected_category = request.args.get('categorySelect')
    print("Selected category:", selected_category)

    categories = db.session.query(Expenses.category).distinct().all()
    filtered_expenses = Expenses.query.filter(Expenses.category == selected_category).all()
    print(f"Filtered expenses count: {len(filtered_expenses)}")

    return render_template('filter.html', filtered_expenses=filtered_expenses, categories=categories)
        





if __name__ == '__main__':
    app.run(debug=True)