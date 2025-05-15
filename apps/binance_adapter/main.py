"""
Punto de entrada principal para el módulo de Binance
"""
from .handler import BinanceHandler

def main():
    # Crear instancia del manejador de Binance
    binance_handler = BinanceHandler()

    # Configurar parámetros dinámicos
    asset = "USDT"
    fiat = "VES"
    cantidad_min_deseada = 320

    # Obtener anuncios de compra y venta usando parámetros dinámicos
    buy_prices, _ = binance_handler.fetch_advertisements("BUY", asset, fiat, cantidad_min_deseada)
    sell_prices, _ = binance_handler.fetch_advertisements("SELL", asset, fiat, cantidad_min_deseada)

    # Encontrar el precio de compra más bajo y el precio de venta más alto
    if buy_prices:
        compra = min(buy_prices)
    else:
        compra = None

    if sell_prices:
        venta = max(sell_prices)
    else:
        venta = None

    # Calcular el porcentaje de ganancia
    if compra is not None and venta is not None:
        ganancia = ((venta - compra) / compra) * 100
        # Enviar los datos calculados a la base de datos
        binance_handler.enviar_datos(compra, venta, ganancia)
    else:
        print("No se pudo calcular la ganancia debido a la ausencia de datos adecuados para compra o venta.")

if __name__ == "__main__":
    main()