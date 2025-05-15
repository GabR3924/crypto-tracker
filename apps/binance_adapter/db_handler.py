"""
Módulo para manejar interacciones con la base de datos
"""
import time
from datetime import datetime

def save_data(compra, venta, ganancia):
    """
    Guarda los datos de compra, venta y ganancia en la base de datos
    
    Args:
        compra (float): Precio promedio de compra
        venta (float): Precio promedio de venta
        ganancia (float): Porcentaje de ganancia
    
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    timestamp = int(time.mktime(datetime.now().timetuple()))
    
    # Aquí iría la lógica para guardar en la base de datos
    # Por ejemplo, usando SQLAlchemy, MongoDB, etc.
    
    # Simulación de guardado exitoso
    print(f"Datos guardados en DB: Compra={round(compra, 2)}, Venta={round(venta, 2)}, "
          f"Ganancia={round(ganancia, 2)}, Fecha={timestamp}")
    
    return True