import requests
import json

def get_offers_with_headers(type_id, limit, amount, amount_currency_id, crypto_currency_id, fiat_currency_id, payment_methods, show_user_offers, show_favorite_mm_only, sort_asc):
    url = "https://74j6q7lg6a.execute-api.eu-west-1.amazonaws.com/stage/orderbook/public/offers/active"

    # Parámeteros de la consulta
    params = {
        'type': type_id,
        'limit': limit,
        'amount': amount,
        'amountCurrencyId': amount_currency_id,
        'sortAsc': sort_asc,
        'cryptoCurrencyId': crypto_currency_id,
        'fiatCurrencyId': fiat_currency_id,
        'paymentMethods': payment_methods,
        'showUserOffers': show_user_offers,
        'showFavoriteMMOnly': show_favorite_mm_only
    }
    
    # Headers
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en',
        'content-type': 'application/json; charset=utf-8',
        'device-id': '0394b5d951ea6e16e3f7a14323aa1e632d4642b03433390574510173a32fa2d3',
        'origin': 'https://app.eldorado.io',
        'referer': 'https://app.eldorado.io/',
        'sec-ch-ua': '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36',
    }

    # Llamada a la API
    response = requests.get(url, headers=headers, params=params)

    # Verificando si la petición fue exitosa
    if response.status_code == 200:
        # Convertir la respuesta en JSON
        offers = response.json()
        return offers
    else:
        print(f"Error: {response.status_code}")
        return None

# Ejemplo de uso con los parámetros de la URL proporcionada
type_id = 0
limit = 3
amount = 5
amount_currency_id = 'TATUM-TRON-USDT'
crypto_currency_id = 'TATUM-TRON-USDT'
fiat_currency_id = 'USD'
payment_methods = 'app_zinli_us'
show_user_offers = True
show_favorite_mm_only = False
sort_asc = False # Cambiar a 'False' según el parámetro sortAsc=false en la URL

offers = get_offers_with_headers(type_id, limit, amount, amount_currency_id, crypto_currency_id, fiat_currency_id, payment_methods, show_user_offers, show_favorite_mm_only, sort_asc)

if offers:
    # Mostrar el resultado con indentación
    print(json.dumps(offers, indent=4))