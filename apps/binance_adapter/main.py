from .handler import BinanceHandler

def main(asset: str = "USDT", fiat: str = "VES", cantidad_minima: float | None = None):
    binance_handler = BinanceHandler()

    # Obtenemos precios y anuncios completos para BUY y SELL
    buy_prices, buy_ads = binance_handler.fetch_advertisements("BUY", asset, fiat, cantidad_minima)
    sell_prices, sell_ads = binance_handler.fetch_advertisements("SELL", asset, fiat, cantidad_minima)

    # Tomamos el precio del primer anuncio si existe
    precio_venta_real = buy_ads[0]['precio'] if buy_ads else None  # Precio al que vendes USDT (primer anuncio BUY)
    precio_compra_real = sell_ads[0]['precio'] if sell_ads else None  # Precio al que compras USDT (primer anuncio SELL)

    if precio_compra_real is not None and precio_venta_real is not None:
        # Calculamos ganancia: ganancia porcentual con respecto al precio de compra
        ganancia = ((precio_venta_real - precio_compra_real) / precio_compra_real) * 100

        print(f"Guardando datos -> Precio compra: {precio_compra_real}, Precio venta: {precio_venta_real}, Ganancia: {ganancia:.2f}%")

        binance_handler.enviar_datos(precio_compra_real, precio_venta_real, ganancia)
    else:
        print("No se pudo calcular la ganancia debido a la ausencia de datos adecuados para compra o venta.")

if __name__ == "__main__":
    main()
