import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity,
    get_jwt
)
import bcrypt
from datetime import timedelta

# --- Initialize Flask app ---
app = Flask(__name__)

# --- Configuration ---
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # token valid for 1 hour

jwt = JWTManager(app)

# --- In‑memory "database" ---
# Each user: {"username": str, "password_hash": bytes, "role": str}
users = []

# --- Helper functions ---
def find_user(username):
    """Find a user by username."""
    for user in users:
        if user['username'] == username:
            return user
    return None

# --- Registration endpoint ---
@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Expected JSON: {"username": "alice", "password": "secret", "role": "user"}
    Role is optional; default is "user".
    """
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data['username']
    password = data['password']
    role = data.get('role', 'user')  # default role

    # Check if user already exists
    if find_user(username):
        return jsonify({"error": "User already exists"}), 409

    # Hash the password using bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Store the user
    users.append({
        'username': username,
        'password_hash': hashed,
        'role': role
    })

    return jsonify({"message": f"User '{username}' registered successfully"}), 201

# --- Login endpoint ---
@app.route('/login', methods=['POST'])
def login():
    """
    Login and receive a JWT token.
    Expected JSON: {"username": "alice", "password": "secret"}
    """
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data['username']
    password = data['password']

    user = find_user(username)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token with identity (username) and additional claims (role)
    additional_claims = {"role": user['role']}
    access_token = create_access_token(
        identity=username,
        additional_claims=additional_claims
    )

    return jsonify({
        "access_token": access_token,
        "username": username,
        "role": user['role']
    }), 200

# --- Protected route: profile (requires authentication) ---
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Get the profile of the authenticated user."""
    current_user = get_jwt_identity()
    user = find_user(current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user['username'],
        "role": user['role']
    }), 200

# --- Admin-only route (requires role=admin) ---
@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_dashboard():
    """Admin dashboard – only accessible by users with admin role."""
    claims = get_jwt()  # get the token claims
    role = claims.get('role', 'user')

    if role != 'admin':
        return jsonify({"error": "Admin access required"}), 403

    return jsonify({"message": "Welcome, Admin!"}), 200

# --- Owner-only route (requires role=owner) ---
@app.route('/owner', methods=['GET'])
@jwt_required()
def owner_dashboard():
    """Owner dashboard – only accessible by users with owner role."""
    claims = get_jwt()
    role = claims.get('role', 'user')

    if role != 'owner':
        return jsonify({"error": "Owner access required"}), 403

    return jsonify({"message": "Welcome, Owner!"}), 200

# --- Generic role-based decorator (optional, more flexible) ---
def role_required(allowed_roles):
    """Decorator factory to restrict access to specific roles."""
    def decorator(fn):
        from functools import wraps
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get('role', 'user')
            if role not in allowed_roles:
                return jsonify({"error": f"Access denied. Required roles: {allowed_roles}"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Example of using the generic decorator
@app.route('/secure-data', methods=['GET'])
@jwt_required()
@role_required(['admin', 'owner'])  # Only admin or owner can access
def secure_data():
    """Example of role-based access using a reusable decorator."""
    return jsonify({"data": "This is sensitive data for admins and owners."}), 200

# --- Error handlers ---
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Missing or invalid token"}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "You don't have permission to access this resource"}), 403

# --- Start the app ---
if __name__ == '__main__':
    # Run on 0.0.0.0 to make it accessible from other devices (optional)
    app.run(host='0.0.0.0', port=5000, debug=True)
