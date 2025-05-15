"""
Definición de modelos de datos y estructuras para la aplicación
"""
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Advertisement:
    """Clase para representar un anuncio P2P"""
    price: float
    min_amount: float
    max_amount: float
    adv_no: str
    seller_nickname: str
    has_banesco: bool
    user_grade: int
    
@dataclass
class MarketData:
    """Clase para representar datos del mercado"""
    buy_average: float
    sell_average: float
    profit_percentage: float
    timestamp: int
    min_transaction: Optional[float] = None
    max_transaction: Optional[float] = None
    
    @classmethod
    def create(cls, buy_prices: List[float], sell_prices: List[float], 
               min_transaction: float, max_transaction: float) -> 'MarketData':
        """
        Crea una instancia de MarketData a partir de listas de precios
        
        Args:
            buy_prices: Lista de precios de compra
            sell_prices: Lista de precios de venta
            min_transaction: Valor mínimo de transacción encontrado
            max_transaction: Valor máximo de transacción encontrado
            
        Returns:
            MarketData: Instancia con los datos procesados
        """
        timestamp = int(datetime.now().timestamp())
        
        buy_average = sum(buy_prices) / len(buy_prices) if buy_prices else 0
        sell_average = sum(sell_prices) / len(sell_prices) if sell_prices else 0
        
        profit_percentage = 0
        if buy_average > 0 and sell_average > 0:
            profit_percentage = ((sell_average - buy_average) / buy_average) * 100
            
        return cls(
            buy_average=buy_average,
            sell_average=sell_average,
            profit_percentage=profit_percentage,
            timestamp=timestamp,
            min_transaction=min_transaction,
            max_transaction=max_transaction
        )