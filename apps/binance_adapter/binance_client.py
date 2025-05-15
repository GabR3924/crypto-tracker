import requests
import logging
from datetime import datetime
import time
from .config import API_URL, ASSET, FIAT, MIN_TRANSACTION_THRESHOLD, REQUIRED_PAYMENT_METHOD, MAX_USER_GRADE, ROWS_PER_PAGE



logger = logging.getLogger(__name__)

class BinanceP2PClient:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}
        self.timestamp = int(time.mktime(datetime.now().timetuple()))
    
    def fetch_advertisements(self, trade_type):
        """Obtiene anuncios P2P filtrados según criterios específicos."""
        filtered_prices = []
        page = 1
        total_pages = 0
        min_transaction = float('inf')
        max_transaction = float('-inf')
        
        while True:
            payload = {
                "asset": ASSET,
                "fiat": FIAT,
                "tradeType": trade_type,
                "page": page,
                "rows": ROWS_PER_PAGE,
            }
            
            try:
                response = requests.post(API_URL, json=payload, headers=self.headers, verify=False)
                
                if response.status_code != 200:
                    logger.error(f"Error {response.status_code}: {response.text}")
                    break
                
                data = response.json()
                advertisements = data.get("data", [])
                print(advertisements)
                
                if not advertisements:
                    logger.info(f"No se encontraron más anuncios para {trade_type}.")
                    break
                
                for adv in advertisements:
                    price, min_t, max_t = self._process_advertisement(adv, min_transaction, max_transaction)
                    if price:
                        filtered_prices.append(price)
                    
                    # Actualiza los valores mínimos y máximos
                    if min_t < min_transaction:
                        min_transaction = min_t
                    if max_t > max_transaction:
                        max_transaction = max_t
                
                if filtered_prices:
                    logger.info(f"Se encontraron anuncios válidos en la página {page}.")
                    break
                else:
                    logger.info(f"No se encontraron anuncios válidos en la página {page}. Buscando en la siguiente página...")
                    page += 1
                    total_pages += 1
                
            except Exception as e:
                logger.error(f"Error al hacer la solicitud: {e}")
                break
        
        self._log_search_summary(total_pages, min_transaction, max_transaction)
        return filtered_prices
    
    def _process_advertisement(self, adv, min_transaction, max_transaction):
        """Procesa un anuncio individual y verifica si cumple los criterios."""
        advert_info = adv.get("adv", {})
        advertiser_info = adv.get("advertiser", {})
        
        price = float(advert_info.get("price", 0))
        min_amount = float(advert_info.get("minSingleTransAmount", 0))
        max_amount = float(advert_info.get("maxSingleTransAmount", 0))
        
        adv_id = advert_info.get('advNo')
        logger.info(f"Procesando anuncio: {adv_id} - Mínimo: {min_amount} - Máximo: {max_amount}")
        
        # Verifica criterios de filtrado
        has_required_payment = any(
            trade_method.get('payType') == REQUIRED_PAYMENT_METHOD 
            for trade_method in advert_info.get("tradeMethods", [])
        )
        
        is_not_verified = advertiser_info.get("userGrade", 0) <= MAX_USER_GRADE
        is_valid_amount = min_amount >= MIN_TRANSACTION_THRESHOLD and max_amount > 0
        
        if has_required_payment and is_not_verified and is_valid_amount:
            logger.info(f"Anuncio {adv_id} - Precio: {price} VES - Vendedor: {advertiser_info.get('nickName')}")
            return price, min_amount, max_amount
        
        return None, min_amount, max_amount
    
    def _log_search_summary(self, total_pages, min_transaction, max_transaction):
        """Registra el resumen de la búsqueda en los logs."""
        logger.info(f"\nTotal de páginas revisadas: {total_pages + 1}")
        if min_transaction != float('inf'):
            logger.info(f"Valor mínimo de transacción encontrado: {min_transaction:.2f} VES")
        if max_transaction != float('-inf'):
            logger.info(f"Valor máximo de transacción encontrado: {max_transaction:.2f} VES")