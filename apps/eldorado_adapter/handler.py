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
    'sortAsc': str(sort_asc).lower(),
    'cryptoCurrencyId': crypto_currency_id,
    'fiatCurrencyId': fiat_currency_id,
    'paymentMethods': payment_methods,
    'showUserOffers': str(show_user_offers).lower(),
    'showFavoriteMMOnly': str(show_favorite_mm_only).lower(),
    'userId': '',
    'lastKey': ''
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

def display_selected_data(offers):
    if offers and 'data' in offers:
        for offer in offers['data']:
            offer_id = offer.get('offerId')
            user_id = offer['user'].get('id') if 'user' in offer else None
            username = offer['user'].get('username') if 'user' in offer else None
            offer_status = offer.get('offerStatus')
            offer_type = offer.get('offerType')

            crypto_currency_id = offer.get('cryptoCurrencyId')
            chain = offer.get('chain')
            fiat_currency_id = offer.get('fiatCurrencyId')
            max_limit = offer.get('maxLimit')
            min_limit = offer.get('minLimit')
            fiat_crypto_exchange = offer.get('fiatToCryptoExchangeRate')
            payment_methods = offer.get('paymentMethods')

            print(f"Offer ID: {offer_id}")
            print(f"User ID: {user_id}")
            print(f"Username: {username}")
            print(f"Offer Status: {offer_status}")
            print(f"Offer Type: {offer_type}")
            print(f"Crypto Currency ID: {crypto_currency_id}")
            print(f"Chain: {chain}")
            print(f"Fiat Currency ID: {fiat_currency_id}")
            print(f"Max Limit: {max_limit}")
            print(f"Min Limit: {min_limit}")
            print(f"fiat_crypto_exchange: {fiat_crypto_exchange}")
            print(f"Payment Methods: {', '.join(payment_methods) if payment_methods else 'N/A'}")
            print("-" * 30)
    else:
        print("No se encontraron datos relevantes.")

# Ejemplo de uso con los parámetros
type_id = 0
limit = 10
amount = ''
amount_currency_id = 'USD'
crypto_currency_id = 'TATUM-TRON-USDT'
fiat_currency_id = 'USD'
payment_methods = ''
show_user_offers = True
show_favorite_mm_only = False
sort_asc = False

offers = get_offers_with_headers(type_id, limit, amount, amount_currency_id, crypto_currency_id, fiat_currency_id, payment_methods, show_user_offers, show_favorite_mm_only, sort_asc)

display_selected_data(offers)