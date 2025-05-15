import logging

logger = logging.getLogger(__name__)

class MarketDataAnalyzer:
    @staticmethod
    def calculate_average(prices):
        """Calcula el precio promedio de una lista de precios."""
        return sum(prices) / len(prices) if prices else 0
    
    @staticmethod
    def calculate_profit_percentage(buy_avg, sell_avg):
        """Calcula el porcentaje de ganancia entre precios de compra y venta."""
        if buy_avg > 0 and sell_avg > 0:
            return ((sell_avg - buy_avg) / buy_avg) * 100
        return 0
    
    @staticmethod
    def report_results(buy_avg, sell_avg, profit_percentage):
        """Reporta los resultados del análisis."""
        if buy_avg:
            logger.info(f"\n🔹 Promedio de compra (BUY): {buy_avg:.2f} VES")
        else:
            logger.warning("No hay precios de compra disponibles.")
        
        if sell_avg:
            logger.info(f"🔸 Promedio de venta (SELL): {sell_avg:.2f} VES")
        else:
            logger.warning("No hay precios de venta disponibles.")
        
        if profit_percentage:
            logger.info(f"📈 Porcentaje de ganancia: {profit_percentage:.2f}%")
        else:
            logger.warning("No se puede calcular porcentaje de ganancia.")
        
        return buy_avg and sell_avg and profit_percentage