"""
Punto de entrada principal para el módulo de Binance
"""
from .handler import BinanceHandler

def main(asset: str, fiat: str, cantidad_minima: float | None = None):
    binance_handler = BinanceHandler()

    buy_prices, _ = binance_handler.fetch_advertisements("BUY", asset, fiat, cantidad_minima)
    sell_prices, _ = binance_handler.fetch_advertisements("SELL", asset, fiat, cantidad_minima)

    if buy_prices:
        compra = min(buy_prices)
    else:
        compra = None

    if sell_prices:
        venta = max(sell_prices)
    else:
        venta = None

    if compra is not None and venta is not None:
        ganancia = ((venta - compra) / compra) * 100
        binance_handler.enviar_datos(compra, venta, ganancia)
    else:
        print("No se pudo calcular la ganancia debido a la ausencia de datos adecuados para compra o venta.")

if __name__ == "__main__":
    main()