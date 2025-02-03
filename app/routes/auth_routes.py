# Import necessary libraries and modules
import bcrypt  # Library for hashing passwords
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
# Blueprint: used to organize routes, templates, etc.
# render_template: renders HTML templates
# request: handles form data in HTTP requests
# flash: displays messages to users
# redirect, url_for: redirects users to other routes
# session: used to store user data for the session

from utils.role_required import role_required  # Custom decorator to restrict access based on user role
from models.user_model import User  # User model to interact with user data in the database
from app import db  # Database object to manage data operations
from utils.jwt_token import create_jwt_token, verify_jwt_token  # Utilities for generating/verifying JWT tokens

# Set up Blueprint for auth routes
auth_blueprint = Blueprint('auth', __name__, template_folder='../templates')

# Route for user registration
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # If form is submitted with POST request
        # Collect user input data from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Hash the password for secure storage
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create new user with the collected data
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)  # Store the hashed password

        # Add the new user to the database and save changes
        db.session.add(new_user)
        db.session.commit()

        # Show success message and redirect to the login page
        flash("Registration successful!", "success")
        return redirect(url_for('auth.login'))

    # If it's a GET request, show the registration form
    return render_template('user_registration.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Look for a user with the submitted email
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found', 'danger')
            return render_template("user_login.html")

        # Verify password and debug the check
        if user.check_password(password):
            # Store session data
            session['username'] = user.username
            session['role'] = user.role
            token = create_jwt_token(user.username, user.role)
            session['token'] = token

            flash("Logged in successfully", "success")
            if user.role == 'Admin':
                return redirect(url_for('medicine.view_medicines'))
            return redirect(url_for('user.home'))
        else:
            flash('Invalid password', 'danger')

    return render_template("user_login.html")

