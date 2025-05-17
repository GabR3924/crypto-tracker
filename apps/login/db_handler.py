import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("ENDPOINT"),
    "user": "admin",
    "password": os.getenv("MASTERPASSWORD"),
    "database": "crypto",
    "port": int(os.getenv("PORT", 3306))
}

def create_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_user_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        telefono VARCHAR(20) NOT NULL,
        correo VARCHAR(255) NOT NULL UNIQUE
    );

    ''')
    conn.commit()
    conn.close()

def insert_user(nombre, apellido, telefono, correo):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO user (nombre, apellido, telefono, correo)
            VALUES (%s, %s, %s, %s)
        ''', (nombre, apellido, telefono, correo))
        conn.commit()
        return True
    except mysql.connector.errors.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_users():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user ORDER BY id DESC")
    results = cursor.fetchall()
    conn.close()
    return results
