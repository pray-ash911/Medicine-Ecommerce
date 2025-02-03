# role_required.py
from functools import wraps
from flask import session, redirect, url_for, flash, jsonify

def role_required(required_role):
    # This function takes the required role as an argument
    def decorator(f):
        # This inner function wraps the original function
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the role from the session
            role = session.get('role')

            # If no role is found in the session, or if it doesn't match the required role, deny access
            if not role or role != required_role:
                # Optionally flash a message or redirect (or return a JSON response as per your needs)
                flash("Access denied! Admins only.", "danger")
                return redirect(url_for('auth.login'))

            # If the role matches, call the original function
            return f(*args, **kwargs)

        return decorated_function  # Return the wrapped function

    return decorator  # Return the decorator function
