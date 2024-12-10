from flask import Flask, url_for
from flask import render_template, redirect, flash
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import AddTransaction, CreateSavingJar, AddRefund
from app.forms import LoginForm, RegisterForm
from app.models import User, SavingJar, Transactions, Refund, RefundStatus, IncomeOutcome

"""Initialisation page set up"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'My$ecur3Key@2024!'
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite://app.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route("/")
def index():
    return render_template("index.html")

"""Create route if user wants to register"""
"""Get=show form and post=process form data"""
@app.route('/register', methods = ['GET', 'POST']) 
def register():
    """Check if the user is already logged in, if they are, they are redirected to the dashboard """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    """POST request + validate input data by checking input data is valid"""
    if form.validate_on_submit():
        """Hash user password for security reasons"""
        hashed_password = generate_password_hash(form.password.data)
        """Create a new user object using the data that have been input in the form and commit changes """
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password.data)
        db.session.add(user)
        db.session.commit()
        """Send a temporary/flash message to confirm registration success"""
        flash('Registration successful! Please log in.', 'success')
        """Redirects user to the login page, after they registered"""
        return redirect(url_for('login'))
    """Renders the html template and passes the form to it"""
    return render_template('register.html', form=form)

"""Create route if user wants to login"""
@app.route('/login', methods= ['GET', 'POST'])
def login():
    """Check if user is already logged in, if they are, redirect to dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    """Displays the login form"""
    form = LoginForm()
    """Make sure the data input is valid and checks if there is another email that matches the input, in the database, verification that the user exists with queries"""
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        """Check if the user has input correct details"""
        if user and check_password_hash(user.password_hash, form.password.data):
            """If data input is correct, user if logged in and redirected to dashboard"""
            login_user(user)
            return redirect(url_for('dashboard'))
        """If data is not correct, user is not allowed login and error message is displayed"""
        flash('Invalid email or password', 'danger')
    """Renders the html template and passes the form to it"""
    return render_template('login.html', form=form)

"""Create route if user wants to logout"""
@app.route('/logout')
def logout():
    logout_user()
    """After logout user is redirected to login page"""
    return redirect(url_for('login'))

"""Create route for dashboard"""
@app.route('/dashboard')
def dashboard():
    """Fetch all transactions and saving jars of the user"""
    transactions = Transactions.query.filter_by(user_id = current_user.id).all()
    refunds = Refund.query.filter_by(user_id = current_user.id).all()
    saving_jars = SavingJar.query.filter_by(user_id = current_user.id).all()
    """Pass to the template for the dashboard transactions and saving jars"""
    return render_template('dashboard.html', transactions = transactions, refunds = refunds, saving_jars = saving_jars)

"""Create route for displaying singular transactions"""
@app.route('/transactions/<int:transaction_id>', methods=['GET'])
def view_transaction(transaction_id):
    transaction = Transactions.query.filter_by(id = transaction_id, user_id = current_user.id).first_or_404()
    return render_template('transactions.html', transaction = transaction)


"""Create route to display singular refund"""
@app.route('/refunds/<int:refund_id>', methods=['GET'])
def view_refund(refund_id):
    refund = Refund.query.filter_by(id = refund_id, user_id = current_user.id).first_of_404()
    return render_template('refunds.html', refunds = refund)

"""Create route for displaying singular saving jar"""
@app.route('/refunds/<int:jar_id>', method=['GET'])
def saving_jar(jar_id):
    jar = SavingJar.query.filter_by(id = jar_id, user_id = current_user.id).first_of_404()
    return render_template('saving_jars.html', jar = jar )

"""Create route for adding a refund"""
@app.route('/add_refunds', methods=['GET', 'POST'])
def add_refunds():
    form = AddRefund()
    if form.validate_on_submit():
        """Use form data to create new refund"""
        refund = Refund (user_id = current_user, datetime = form.datetime.data, amount = form.amount.data, status = RefundStatus[form.status.data])
        """Add to database"""
        db.session.add(refund)
        db.session.commit()
        flash('Refund has been added to the tracker!', 'success')
        return redirect(url_for('refunds'))
    """Redirect to refund page if form isnt submitted"""
    return render_template('refunds.html', form = form)



"""Create route for adding transactions"""
@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = AddTransaction()
    if form.validate_on_submit():
        """Using form data, create a new trasnaction"""
        transaction = Transactions (user_id = current_user.id, amount = form.amount.data, category = form.category.data, date = form.datetime.data, kind = IncomeOutcome[form.kind.data])
        """Add Transaction to database"""
        db.session.add(transaction)
        db.session.commit()
        """Display message to user to confirm transaction added"""
        flash('Transaction has been added !', 'success')
        """Now redirect user to dashboard"""
        return redirect(url_for('dashboard'))
    """If form hasnt been submitted, redirect user to the form"""
    return render_template('add_transaction.html', form = form)


"""Create route for creating new saving jars"""
@app.route('/add_saving_jar', methods=['GET', 'POST'])
@login_required
def saving_jar():
    form = CreateSavingJar()
    if form.validate_on_submit():
        """Create new jar using data from the form"""
        jar = SavingJar (user_id = current_user.id, name = form.name.data, goal = form.goal.data)
        """Add jar to db"""
        db.session.add(jar)
        db.session.commit()
        """Display message to confirm jar creation"""
        flash('Jar has been created successfully', 'success')
        """Redirect user to dashboard"""
        return redirect(url_for('dashboard'))
    """If form hasnt been submitted, redirect user to it"""
    return render_template('add_saving_jar.html', form = form)






if __name__ == "__main__":
    app.run(debug=True)