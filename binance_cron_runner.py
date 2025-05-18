import logging
from apps.binance_adapter.main import main as binance_main

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

markets = [
    {"asset": "USDT", "fiat": "VES", "cantidad_minima": 320},
    # {"asset": "BTC", "fiat": "VES", "cantidad_minima": 0.001},
    # {"asset": "USDT", "fiat": "ARS", "cantidad_minima": 320},
]

for market in markets:
    logging.info(f"⏳ Ejecutando para {market['asset']}/{market['fiat']}")
    binance_main(market["asset"], market["fiat"], cantidad_minima=market["cantidad_minima"])
