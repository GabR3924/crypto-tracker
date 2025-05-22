import mysql.connector
from mysql.connector import pooling, Error
import os
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Generator, Dict, Any
import logging

# Cargar variables de entorno
load_dotenv()

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la base de datos
DB_CONFIG = {
    "host": os.getenv("ENDPOINT"),
    "user": "admin",
    "password": os.getenv("MASTERPASSWORD"),
    "database": "crypto",
    "port": int(os.getenv("PORT", 3306)),
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
    "autocommit": False,
    "raise_on_warnings": True,
    "sql_mode": "STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO"
}

# Configuración del pool de conexiones
POOL_CONFIG = {
    **DB_CONFIG,
    "pool_name": "crypto_pool",
    "pool_size": 10,
    "pool_reset_session": True,
    "buffered": True
}

# Pool de conexiones global
connection_pool = None
_initialized = False

def init_connection_pool():
    """Inicializar el pool de conexiones"""
    global connection_pool
    try:
        connection_pool = pooling.MySQLConnectionPool(**POOL_CONFIG)
        logger.info("✅ Pool de conexiones MySQL inicializado correctamente")
        return connection_pool
    except Error as e:
        logger.error(f"❌ Error al crear pool de conexiones: {e}")
        raise

def get_connection():
    """Obtener una conexión del pool"""
    global connection_pool
    if connection_pool is None:
        init_connection_pool()
    
    try:
        connection = connection_pool.get_connection()
        return connection
    except Error as e:
        logger.error(f"❌ Error al obtener conexión: {e}")
        raise

@contextmanager
def get_database_connection():
    """Context manager para manejo seguro de conexiones"""
    connection = None
    try:
        connection = get_connection()
        yield connection
    except Error as e:
        if connection:
            connection.rollback()
        logger.error(f"❌ Error en la base de datos: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()

def get_database() -> Generator[mysql.connector.MySQLConnection, None, None]:
    """Dependency para FastAPI - obtener conexión de base de datos"""
    with get_database_connection() as connection:
        yield connection

class DatabaseManager:
    """Clase para operaciones avanzadas de base de datos"""
    
    @staticmethod
    def execute_query(query: str, params: tuple = None, fetch: bool = False) -> Any:
        """Ejecutar una query con mejor manejo de errores"""
        with get_database_connection() as connection:
            cursor = connection.cursor(dictionary=True, buffered=True)
            try:
                cursor.execute(query, params or ())
                
                if fetch:
                    if "SELECT" in query.upper():
                        result = cursor.fetchall()
                    else:
                        result = cursor.fetchone()
                else:
                    connection.commit()
                    result = cursor.rowcount
                
                return result
            except Error as e:
                connection.rollback()
                # Manejar específicamente el error de tabla existente
                if e.errno == 1050:  # ER_TABLE_EXISTS_ERROR
                    logger.warning(f"⚠️ Tabla ya existe: {e}")
                    return None
                logger.error(f"❌ Error ejecutando query: {e}")
                logger.error(f"Query: {query}")
                logger.error(f"Params: {params}")
                raise
            finally:
                cursor.close()
    
    @staticmethod
    def execute_many(query: str, data: list) -> int:
        """Ejecutar múltiples inserts/updates"""
        with get_database_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.executemany(query, data)
                connection.commit()
                return cursor.rowcount
            except Error as e:
                connection.rollback()
                logger.error(f"❌ Error en execute_many: {e}")
                raise
            finally:
                cursor.close()
    
    @staticmethod
    def get_last_insert_id(connection) -> int:
        """Obtener el último ID insertado"""
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()

def init_database_tables():
    """Crear todas las tablas necesarias con mejor manejo de errores"""
    tables = {
        "cycles": """
        CREATE TABLE IF NOT EXISTS cycles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_date TIMESTAMP NULL,
            target_usdt DECIMAL(15,8) NOT NULL,
            purchased_usdt DECIMAL(15,8) DEFAULT 0,
            sold_usdt DECIMAL(15,8) DEFAULT 0,
            total_invested DECIMAL(15,2) DEFAULT 0,
            total_returned DECIMAL(15,2) DEFAULT 0,
            total_profit DECIMAL(15,2) DEFAULT 0,
            status VARCHAR(20) DEFAULT 'activo' CHECK (status IN ('activo', 'completado')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_status (status),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        "transactions": """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cycle_id INT NOT NULL,
            transaction_type VARCHAR(10) NOT NULL CHECK (transaction_type IN ('compra', 'venta')),
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            -- Campos para compras
            usdt_desired DECIMAL(15,8) NULL,
            commission_rate DECIMAL(5,2) NULL,
            purchase_price DECIMAL(15,4) NULL,
            usdt_to_pay DECIMAL(15,8) NULL,
            total_investment_bs DECIMAL(15,2) NULL,
            real_purchase_price DECIMAL(15,4) NULL,
            buy_status VARCHAR(20) NULL CHECK (buy_status IN ('pendiente', 'completado')),
            
            -- Campos para ventas
            market_best_price DECIMAL(15,4) NULL,
            competitive_adjustment DECIMAL(15,4) NULL,
            sale_price DECIMAL(15,4) NULL,
            usdt_sold DECIMAL(15,8) NULL,
            profit_bs DECIMAL(15,2) NULL,
            profit_percentage DECIMAL(8,4) NULL,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            FOREIGN KEY (cycle_id) REFERENCES cycles(id) ON DELETE CASCADE,
            INDEX idx_cycle_id (cycle_id),
            INDEX idx_transaction_type (transaction_type),
            INDEX idx_buy_status (buy_status),
            INDEX idx_transaction_date (transaction_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        "transaction_links": """
        CREATE TABLE IF NOT EXISTS transaction_links (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sell_transaction_id INT NOT NULL,
            buy_transaction_id INT NOT NULL,
            linked_amount DECIMAL(15,8) NOT NULL,
            buy_price DECIMAL(15,4) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (sell_transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
            FOREIGN KEY (buy_transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
            INDEX idx_sell_transaction (sell_transaction_id),
            INDEX idx_buy_transaction (buy_transaction_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    }
    
    for table_name, table_sql in tables.items():
        try:
            DatabaseManager.execute_query(table_sql)
            logger.info(f"✅ Tabla {table_name} creada/verificada correctamente")
        except Error as e:
            if "already exists" in str(e):
                logger.warning(f"⚠️ La tabla {table_name} ya existe (esto es normal)")
            else:
                logger.error(f"❌ Error creando tabla {table_name}: {e}")
                raise

def test_connection():
    """Probar la conexión a la base de datos"""
    try:
        with get_database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                logger.info("✅ Conexión a la base de datos exitosa")
                return True
            else:
                logger.error("❌ Conexión fallida")
                return False
    except Error as e:
        logger.error(f"❌ Error de conexión: {e}")
        return False

def initialize():
    """Inicialización controlada del módulo"""
    global _initialized
    if not _initialized:
        try:
            init_connection_pool()
            init_database_tables()
            _initialized = True
        except Exception as e:
            logger.error(f"❌ Error en la inicialización: {e}")
            raise

if __name__ == "__main__":
    # Solo para testing
    test_connection()
    initialize()
else:
    # Inicialización diferida - no se ejecuta automáticamente al importar
    pass