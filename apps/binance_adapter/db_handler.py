import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()
# print("DEBUG ENV:", os.getenv("ENDPOINT"), os.getenv("MASTERPASSWORD"), os.getenv("PORT"))

# Configuración de la base de datos en RDS
DB_CONFIG = {
    "host": os.getenv("ENDPOINT"),
    "user": "admin",  # Reemplázalo con tu usuario de RDS
    "password": os.getenv("MASTERPASSWORD"),
    "database": "crypto",  # Reemplázalo con el nombre de tu DB en RDS
    "port": int(os.getenv("PORT", 3306))  # Usa 3306 por defecto si no se encuentra
}

# Crear conexión
def create_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Crear tabla si no existe
def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS crypto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME,
                avg_buy DECIMAL(10, 3),
                avg_sell DECIMAL(10, 3),
                profit_percentage DECIMAL(10, 3),
                origen VARCHAR(255)
        )
    ''')
    conn.commit()
    conn.close()

# Guardar datos en la DB
def save_data(compra, venta, ganancia, origen):
    conn = create_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = '''
        INSERT INTO crypto (timestamp, avg_buy, avg_sell, profit_percentage, origen)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (timestamp, venta,compra, ganancia, origen))
    
    conn.commit()
    conn.close()
    print(f'✅ Datos guardados en la base de datos: {timestamp}')
    
def get_all_data():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    
      # Usar id DESC para obtener el registro más reciente basado en la inserción
    cursor.execute("SELECT * FROM crypto ORDER BY id DESC")
    results = cursor.fetchall()
    
    conn.close()
    return results

# Inicializar la base de datos
init_db()