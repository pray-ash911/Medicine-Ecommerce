'''Creating a JWT Token (create_jwt_token):
Takes username and role as parameters.
Constructs a payload with the username, role, and expiration time (set to 30 minutes from current time).
Signs the token with the app's SECRET_KEY using the HS256 algorithm.
Returns the generated JWT token.
Verifying a JWT Token (verify_jwt_token):

Takes the JWT token as input.
Attempts to decode the token using the app's SECRET_KEY and checks if it is valid.
If valid, returns a dictionary with the user and role from the token payload.
If the token has expired or is invalid, it returns None.

'''


import jwt  # Import the JWT library for encoding and decoding JSON Web Tokens
import datetime  # Import datetime to handle token expiration times
from flask import current_app as app  # Import Flask's current app to access app config (like SECRET_KEY)


# Function to create a JWT token with username and role
def create_jwt_token(username, role):
    """
    Create a JWT token that includes the username and role.
    """
    token = jwt.encode({
        'user': username,  # Add the username to the token payload
        'role': role,  # Add the user's role to the token payload
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        # Set token expiration time to 30 minutes from now
    }, app.config['SECRET_KEY'], algorithm="HS256")  # Use the app's SECRET_KEY to sign the token with HS256 algorithm
    return token  # Return the generated token


# Function to verify and decode a JWT token
def verify_jwt_token(token):
    """
    Verify a JWT token and return the decoded user information if valid.
    """
    try:
        # Decode the token using the app's SECRET_KEY and the HS256 algorithm
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

        # Return a dictionary with the username and role from the token if valid
        return {'user': decoded['user'], 'role': decoded['role']}

    # Handle case when the token has expired
    except jwt.ExpiredSignatureError:
        return None  # Return None if the token has expired

    # Handle case when the token is invalid for other reasons
    except jwt.InvalidTokenError:
        return None  # Return None if the token is invalid
