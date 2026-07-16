# 🔐 JWT‑Based Authentication & Authorization (Flask)

This is a complete implementation of a **JWT‑based authentication and authorization** system using **Flask**, **Flask‑JWT‑Extended**, and **bcrypt**.  
It includes:

- **User registration** – stores hashed passwords (bcrypt).
- **User login** – returns a JWT access token.
- **Protected routes** – only authenticated users can access.
- **Role‑based access control** – endpoints restricted to specific roles (`admin`, `user`, `owner`).

---

## 📦 Requirements

Install the dependencies with pip:

```bash
pip install flask flask-jwt-extended bcrypt
```

> **Note:** This example uses an **in‑memory store** (a Python list) for users – suitable for development/testing. In production, replace it with a real database.

---

## 🚀 Running the Server

1. Save the code as `JWTapp.py`.
2. Install dependencies: `pip install flask flask-jwt-extended bcrypt`
3. Run: `python JWTapp.py`
4. The server starts at `http://localhost:5000`

---

## 🔍 Endpoints & Testing with `curl`

### 1. Register a new user

```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret", "role": "user"}'
```

Response:
```json
{"message": "User 'alice' registered successfully"}
```

Register an admin:
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "bob", "password": "adminpass", "role": "admin"}'
```

Register an owner:
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "carol", "password": "ownerpass", "role": "owner"}'
```

---

### 2. Login and obtain a JWT token

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "alice",
  "role": "user"
}
```

Save the `access_token` for subsequent requests.

---

### 3. Access protected profile (requires authentication)

```bash
curl -X GET http://localhost:5000/profile \
  -H "Authorization: Bearer <your_access_token>"
```

Response:
```json
{
  "username": "alice",
  "role": "user"
}
```

---

### 4. Admin-only route (fails for non-admin)

```bash
# As Alice (user role)
curl -X GET http://localhost:5000/admin \
  -H "Authorization: Bearer <alice_token>"
```
Response:
```json
{"error": "Admin access required"}
```

```bash
# As Bob (admin role)
curl -X GET http://localhost:5000/admin \
  -H "Authorization: Bearer <bob_token>"
```
Response:
```json
{"message": "Welcome, Admin!"}
```

---

### 5. Owner-only route

```bash
# As Alice (user) – denied
curl -X GET http://localhost:5000/owner \
  -H "Authorization: Bearer <alice_token>"
```

```bash
# As Carol (owner) – granted
curl -X GET http://localhost:5000/owner \
  -H "Authorization: Bearer <carol_token>"
```

---

### 6. Role‑based decorator example

```bash
# Access /secure-data – only admin or owner can see it
# As Bob (admin) – success
curl -X GET http://localhost:5000/secure-data \
  -H "Authorization: Bearer <bob_token>"
# As Alice (user) – denied
```

---

## 🧠 How It Works

| Component                      | Description |
|--------------------------------|-------------|
| **Registration**               | Receives username, password, optional role. Hashes password with bcrypt and stores in memory. |
| **Login**                      | Verifies credentials. On success, creates a JWT token containing the username (identity) and the user's role as an additional claim. |
| **`@jwt_required()`**          | Middleware that validates the token on protected routes. Extracts the identity (username). |
| **Role checks**                | Extract the `role` claim from the token with `get_jwt()`. Compare it to allowed roles. |
| **`role_required` decorator**  | A reusable function that checks if the token's role is in a list of allowed roles. |
| **Error handling**             | Returns `401` for missing/invalid tokens, `403` for insufficient permissions. |

---

## 🔐 Security Notes

- **JWT_SECRET_KEY**: In production, set a strong, random secret via environment variable. Never commit it to version control.
- **bcrypt**: Used with a salt to protect against rainbow tables. The work factor can be adjusted via `bcrypt.gensalt(rounds=12)`.
- **Token expiration**: Set to 1 hour. Use refresh tokens for longer sessions (not implemented here).
- **Transport security**: Always use HTTPS in production to prevent token interception.
- **In‑memory store**: This example uses a list; for persistence, replace with a database (SQLite, PostgreSQL, etc.) and store hashed passwords securely.

---

## 📚 Possible Enhancements

- Add **refresh tokens** to allow sliding expiration.
- Implement **password reset** functionality.
- Add **email verification** during registration.
- Store user data in a real **database** with an ORM like SQLAlchemy.
- Logout support by maintaining a token blacklist.
- More granular permissions (e.g., `read`, `write`) using scopes.

---

**Built with ❤️ for educational purposes.**
