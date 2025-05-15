import logging
from .binance_client import BinanceP2PClient
from .analyzer import MarketDataAnalyzer
from .backend_client import BackendClient

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Función principal que orquesta el flujo del programa."""
    binance_client = BinanceP2PClient()
    analyzer = MarketDataAnalyzer()
    backend_client = BackendClient()
    
    # Obtener datos
    buy_prices = binance_client.fetch_advertisements("BUY")
    sell_prices = binance_client.fetch_advertisements("SELL")
    
    # Analizar datos
    buy_avg = analyzer.calculate_average(buy_prices)
    sell_avg = analyzer.calculate_average(sell_prices)
    profit_percentage = analyzer.calculate_profit_percentage(buy_avg, sell_avg)
    
    # Mostrar resultados
    valid_data = analyzer.report_results(buy_avg, sell_avg, profit_percentage)
    
    # Enviar datos si todos los valores están disponibles
    if valid_data:
        backend_client.send_data(buy_avg, sell_avg, profit_percentage, binance_client.timestamp)
    else:
        logger.warning("⚠️ No se enviaron datos debido a valores inválidos.")

if __name__ == "__main__":
    main()