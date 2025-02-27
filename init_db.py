import psycopg2
from flask import Flask, request, jsonify



# Database connection settings
DB_CONFIG = {
    "dbname": "my_project",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    
}

# Function to connect to PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connected to the database successfully!")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

# Function to create a table
def create_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    firstname VARCHAR(50) NOT NULL,
                    lastname VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password TEXT NOT NULL
                );
            """)
            conn.commit()
            print("Table 'users' created successfully!")
    except psycopg2.Error as e:
        print("Error creating table:", e)

# Function to insert a user
def insert_user(conn, username, firstname, lastname, email, password):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (username, firstname, lastname, email, password)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """, (username, firstname, lastname, email, password))
            conn.commit()
            print("User inserted successfully!")
    except psycopg2.Error as e:
        print("Error inserting user:", e)

# Function to fetch all users
def fetch_users(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users;")
            users = cur.fetchall()
            for user in users:
                print(user)
    except psycopg2.Error as e:
        print("Error fetching users:", e)

# Main function
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_table(conn)  # Create table if not exists
        insert_user(conn, "johndoe", "John", "Doe", "john.doe@example.com", "securepassword123")
        fetch_users(conn)  # Retrieve and display users
        conn.close()
