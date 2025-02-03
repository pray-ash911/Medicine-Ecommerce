# user_routes.py
from flask import render_template, Blueprint, session, request, redirect, flash, url_for
from models.user_model import User
from models.medicine_model import Medicine  # Import Medicine model to access medicine data
from utils.role_required import role_required  # Import role-based access decorator
from models.order_model import Order  # Import Order model to fetch order history
from app import db

user_blueprints = Blueprint('user', __name__, template_folder='../templates')


@user_blueprints.route('/login')
def login():
    return render_template('user_login.html')


@user_blueprints.route('/dashboard')
@role_required('Customer')  # Restrict access to customers only
def dashboard():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('user.login'))

    orders = Order.query.filter_by(user_id=user.id).all()
    return render_template('customer_dashboard.html', username=username, orders=orders)


@user_blueprints.route('/profile', methods=['GET', 'POST'])
@role_required('Customer')
def profile():
    user = User.query.filter_by(username=session.get('username')).first()
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        flash("Profile updated successfully", "success")
        return redirect(url_for('user.profile'))
    return render_template('customer_profile.html', user=user)


# Route for the homepage displaying all medicines
@user_blueprints.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    medicines = Medicine.query.paginate(page=page, per_page=per_page)
    return render_template('customer_homepage.html', medicines=medicines)

# Route for viewing individual medicine details
@user_blueprints.route('/medicine/<int:medicine_id>')
def medicine_detail(medicine_id):
    # Fetch the medicine by ID
    medicine = Medicine.query.get(medicine_id)
    if not medicine:
        flash("Medicine not found", "error")
        return redirect(url_for('user.home'))

    # Calculate the discounted price (if there's a discount)
    discounted_price = medicine.get_discounted_price() if medicine.discount else medicine.price

    return render_template('medicine_detail.html', medicine=medicine, discounted_price=discounted_price)

# user_routes.py

@user_blueprints.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        flash("Please enter a search term.", "warning")
        return redirect(url_for('user.home'))

    # Perform the search
    medicines = Medicine.query.filter(
        (Medicine.name.ilike(f"%{query}%")) | (Medicine.description.ilike(f"%{query}%"))
    ).all()

    # Render customer homepage with search results
    return render_template('customer_homepage.html', medicines=medicines, query=query)


# user_routes.py
@user_blueprints.route('/logout')
def logout():
    # Clear session data or perform logout logic
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('user.login'))
