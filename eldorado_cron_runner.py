import logging
from apps.eldorado_adapter.main import main as eldorado_main

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Puedes definir diferentes combinaciones de parámetros a probar
markets = [
    {
        "limit": 10,
        "amount": '',
        "amount_currency_id": "USD",
        "crypto_currency_id": "TATUM-TRON-USDT",
        "fiat_currency_id": "USD",
        "payment_methods": 'app_zinli_us',
        "show_user_offers": True,
        "show_favorite_mm_only": False
    },
     {
        "limit": 10,
        "amount": '',
        "amount_currency_id": "TATUM-TRON-USDT",
        "crypto_currency_id": "TATUM-TRON-USDT",
        "fiat_currency_id": "VES",
        "payment_methods": 'bank_banesco',
        "show_user_offers": True,
        "show_favorite_mm_only": False
    },
    # Puedes agregar más configuraciones si quieres comparar mercados
]

for market in markets:
    logging.info("⏳ Ejecutando consulta para ElDorado")
    eldorado_main(
        limit=market["limit"],
        amount=market["amount"],
        amount_currency_id=market["amount_currency_id"],
        crypto_currency_id=market["crypto_currency_id"],
        fiat_currency_id=market["fiat_currency_id"],
        payment_methods=market["payment_methods"],
        show_user_offers=market["show_user_offers"],
        show_favorite_mm_only=market["show_favorite_mm_only"]
    )
