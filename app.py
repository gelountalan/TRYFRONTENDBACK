from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Database connection parameters
DB_CONFIG = {
    "host": "localhost",
    "database": "my_project",
    "user": "postgres",
    "password": "admin"
}

# Function to connect to the database
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# Serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Middleware to add CORS headers manually
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"  # Allow all origins
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json  # Get JSON data from frontend

        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validate input (basic validation)
        if not all([firstname, lastname, username, email, password]):
            return jsonify({"error": "All fields are required"}), 400

        # Hash password for security
        hashed_password = generate_password_hash(password)

        # Connect to the database
        conn = connect_db()
        cursor = conn.cursor()

        # Insert user into the database
        cursor.execute(sql.SQL("""
            INSERT INTO users (firstname, lastname, username, email, password)
            VALUES (%s, %s, %s, %s, %s)
        """), (firstname, lastname, username, email, hashed_password))

        # Commit and close connection
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
