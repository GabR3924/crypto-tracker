from .handler import BinanceHandler

def main(asset: str, fiat: str, cantidad_minima: float | None = None):
    binance_handler = BinanceHandler()

    # "BUY" en Binance significa que otras personas quieren comprarte a ti
    buy_prices, _ = binance_handler.fetch_advertisements("BUY", asset, fiat, cantidad_minima)

    # "SELL" significa que otras personas quieren venderte a ti
    sell_prices, _ = binance_handler.fetch_advertisements("SELL", asset, fiat, cantidad_minima)

    if sell_prices:
        precio_compra_real = min(sell_prices)  # tú compras a menor precio
    else:
        precio_compra_real = None

    if buy_prices:
        precio_venta_real = max(buy_prices)  # tú vendes al mayor precio posible
    else:
        precio_venta_real = None

    if precio_compra_real is not None and precio_venta_real is not None:
        ganancia = ((precio_venta_real - precio_compra_real) / precio_compra_real) * 100
        binance_handler.enviar_datos(precio_compra_real, precio_venta_real, ganancia)
    else:
        print("No se pudo calcular la ganancia debido a la ausencia de datos adecuados para compra o venta.")

if __name__ == "__main__":
    main()
