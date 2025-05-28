import requests
from .schemas import OfferFilter, Offer
from .db_handlers import save_data
from typing import List
from decimal import Decimal, ROUND_DOWN


def get_offers_with_headers(filter_params: OfferFilter) -> List[Offer]:
    url = "https://74j6q7lg6a.execute-api.eu-west-1.amazonaws.com/stage/orderbook/public/offers/active"

    params = {
        'type': filter_params.type_id,
        'limit': filter_params.limit,
        'amount': filter_params.amount,
        'amountCurrencyId': filter_params.amount_currency_id,
        'sortAsc': str(filter_params.sort_asc).lower(),
        'cryptoCurrencyId': filter_params.crypto_currency_id,
        'fiatCurrencyId': filter_params.fiat_currency_id,
        'paymentMethods': filter_params.payment_methods,
        'showUserOffers': str(filter_params.show_user_offers).lower(),
        'showFavoriteMMOnly': str(filter_params.show_favorite_mm_only).lower(),
        'userId': '',
        'lastKey': ''
    }

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

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        response_data = response.json()
        offers_data = response_data.get('data', [])
        offers = []
        
        for offer_data in offers_data:
            # Extraer datos del usuario si existe
            user_data = offer_data.get('user', {})
            user_id = user_data.get('id') if user_data else None
            username = user_data.get('username') if user_data else None
            
            # Extraer métodos de pago (convertir a lista si es necesario)
            payment_methods = offer_data.get('paymentMethods', [])
            if isinstance(payment_methods, str):
                payment_methods = [payment_methods]
            
            # Crear objeto Offer con los campos mapeados correctamente
            offer = Offer(
                offer_id=offer_data.get('offerId'),
                user_id=user_id,
                username=username,
                offer_status=offer_data.get('offerStatus'),
                offer_type=offer_data.get('offerType'),
                crypto_currency_id=offer_data.get('cryptoCurrencyId'),
                chain=offer_data.get('chain'),
                fiat_currency_id=offer_data.get('fiatCurrencyId'),
                max_limit=offer_data.get('maxLimit'),
                min_limit=offer_data.get('minLimit'),
                fiat_crypto_exchange=offer_data.get('fiatToCryptoExchangeRate'),
                payment_methods=payment_methods
            )
            offers.append(offer)
            
        return offers
    else:
        print(f"Error: {response.status_code}")
        print(f"Respuesta: {response.text}")
        return []

def display_selected_data(offers: List[Offer]):
    if not offers:
        print("No se encontraron ofertas.")
        return
        
    for offer in offers:
        print(f"Offer ID: {offer.offer_id}")
        print(f"User ID: {offer.user_id}")
        print(f"Username: {offer.username}")
        print(f"Offer Status: {offer.offer_status}")
        print(f"Offer Type: {offer.offer_type}")
        print(f"Crypto Currency ID: {offer.crypto_currency_id}")
        print(f"Chain: {offer.chain}")
        print(f"Fiat Currency ID: {offer.fiat_currency_id}")
        print(f"Max Limit: {offer.max_limit}")
        print(f"Min Limit: {offer.min_limit}")
        print(f"Fiat Crypto Exchange: {offer.fiat_crypto_exchange}")
        
        if offer.payment_methods:
            methods_str = ', '.join(offer.payment_methods)
            print(f"Payment Methods: {methods_str}")
        else:
            print("Payment Methods: None")
            
        print("-" * 30)
    

def get_buy_and_sell_offers(filter_params: OfferFilter = None):
    """
    Obtiene tanto ofertas de compra como de venta utilizando los mismos parámetros base.
    Solo cambia type_id (1 para compra, 0 para venta) y sort_asc (True para compra, False para venta).

    Args:
        filter_params: Parámetros de filtro base. Si es None, se usarán valores predeterminados.

    Returns:
        tuple: (ofertas_compra, ofertas_venta)
    """
    # Si no se proporcionan parámetros, usar valores predeterminados
    if filter_params is None:
        filter_params = OfferFilter(
            limit=10,
            amount='5',
            amount_currency_id='USD',
            crypto_currency_id='TATUM-TRON-USDT',
            fiat_currency_id='USD',
            payment_methods='app_zinli_us',
            show_user_offers=True,
            show_favorite_mm_only=False
        )
    
    # Configurar y ejecutar para Compra (type_id=1, sort_asc=True)
    buy_filter_params = filter_params.copy(update={"type_id": 1, "sort_asc": True})
    print("\n=== OFERTAS DE COMPRA ===")
    buy_offers = get_offers_with_headers(buy_filter_params)
    
    # Configurar y ejecutar para Venta (type_id=0, sort_asc=False)
    sell_filter_params = filter_params.copy(update={"type_id": 0, "sort_asc": False})
    print("\n=== OFERTAS DE VENTA ===")
    sell_offers = get_offers_with_headers(sell_filter_params)

    # Si hay ofertas de compra y venta, calculamos el porcentaje de ganancia
    if buy_offers and sell_offers:

        buy_price = Decimal(str(buy_offers[0].fiat_crypto_exchange)).quantize(Decimal("0.001"), rounding=ROUND_DOWN)
        sell_price = Decimal(str(sell_offers[0].fiat_crypto_exchange)).quantize(Decimal("0.001"), rounding=ROUND_DOWN)
        
        # Obtener el payment method de los parámetros de filtro
        payment_method = filter_params.payment_methods
            
        # Calculamos el porcentaje de ganancia
        profit_percentage = (( sell_price - buy_price) / buy_price * 100).quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        # Imprimir los datos antes de guardarlos
        print(f"Datos a guardar -> Precio de compra: {buy_price}, Precio de venta: {sell_price}, Porcentaje de ganancia: {profit_percentage}%, Payment Method: {payment_method}")

        # Guardamos datos en la base de datos incluyendo el payment method
        save_data(buy_price, sell_price, profit_percentage, payment_method, origen='eldorado')
    else:
        print("No hay suficientes ofertas para calcular la ganancia.")
    
    return buy_offers, sell_offers
def main():
    # Obtener ofertas de compra y venta
    buy_offers, sell_offers = get_buy_and_sell_offers()
    
    # Mostrar resultados de compra
    print(f"\nResultados de compra: {len(buy_offers)} ofertas encontradas")
    display_selected_data(buy_offers)
    
    # Mostrar resultados de venta
    print(f"\nResultados de venta: {len(sell_offers)} ofertas encontradas")
    display_selected_data(sell_offers)


if __name__ == "__main__":
    main()