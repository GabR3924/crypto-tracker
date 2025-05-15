import requests
import logging
from config import BACKEND_URL

logger = logging.getLogger(__name__)

class BackendClient:
    def __init__(self):
        self.url = BACKEND_URL
    
    def send_data(self, buy_avg, sell_avg, profit_percentage, timestamp):
        """Envía los datos calculados al backend."""
        payload = {
            "compraPromedio": round(buy_avg, 2),
            "ventaPromedio": round(sell_avg, 2),
            "ganancia": round(profit_percentage, 2),
            "fecha": timestamp
        }
        
        try:
            response = requests.post(self.url, json=payload)
            if response.status_code == 200:
                logger.info("✅ Datos enviados correctamente.")
                return True
            else:
                logger.error(f"❌ Error al enviar datos: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Excepción al enviar datos: {e}")
            return False