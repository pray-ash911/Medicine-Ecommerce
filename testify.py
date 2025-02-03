from flask import Flask, jsonify, request  # Import necessary modules from Flask
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # Import JWT-related functions

app = Flask(__name__)  # Initialize the Flask app

# Set up a secret key to sign the JWT. This ensures the tokens are secure.
# Always keep this key secret in a real application!
app.config['JWT_SECRET_KEY'] = '13743e21e08a9b689a82ebe14a2173faad19309fb1672122b6edb0fe32117b65'

# Initialize JWT manager with the Flask app
jwt = JWTManager(app)

# A simple mock user database (this is just for testing; in a real app, this would be from an actual database)
users = {
    'user1': {'password': 'abc123'},
    'user2': {'password': 'password'}
}

# Route for user login
@app.route('/login', methods=['POST'])  # Define a POST endpoint for login
def login():
    # Get the username and password from the request (JSON data sent by the client)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the provided credentials match any user in our mock database
    if username in users and users[username]['password'] == password:
        # If credentials are valid, create a JWT token for this user
        access_token = create_access_token(identity=username)
        # Return the generated token in JSON format
        return jsonify(access_token=access_token), 200  # Status 200 means OK
    else:
        # If credentials are invalid, return an error message
        return jsonify(message="Invalid credentials"), 401  # Status 401 means Unauthorized

# Route for accessing a protected resource (requires a valid JWT token)
@app.route('/protected', methods=['GET'])
@jwt_required()  # This decorator ensures that the routes can only be accessed with a valid JWT token
def protected():
    # Get the identity of the current user (extracted from the JWT token)
    current_user = get_jwt_identity()
    # Return a message showing which user is logged in (based on the token)
    return jsonify(logged_in_as=current_user), 200  # Status 200 means OK

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode (useful during development)
