from .handler import get_offers_with_headers, display_selected_data, get_buy_and_sell_offers
from .schemas import OfferFilter

def main():
    # Crear objeto de filtro con los parámetros base deseados
    filter_params = OfferFilter(
        # No necesitamos establecer type_id ni sort_asc aquí ya que
        # get_buy_and_sell_offers los configurará automáticamente
        limit=10,
        amount='5',
        amount_currency_id='USD',
        crypto_currency_id='TATUM-TRON-USDT',
        fiat_currency_id='USD',
        payment_methods='app_zinli_us',
        show_user_offers=True,
        show_favorite_mm_only=False
    )
    
    print(f"Buscando ofertas con payment_method: {filter_params.payment_methods}")
    
    # Obtener tanto ofertas de compra como de venta
    buy_offers, sell_offers = get_buy_and_sell_offers(filter_params)
    
    # Mostrar los resultados de las ofertas de compra
    print(f"\nOFERTAS DE COMPRA: {len(buy_offers)} encontradas")
    if buy_offers:
        display_selected_data(buy_offers)
    else:
        print("No se encontraron ofertas de compra con los filtros especificados.")
    
    # Mostrar los resultados de las ofertas de venta
    print(f"\nOFERTAS DE VENTA: {len(sell_offers)} encontradas")
    if sell_offers:
        display_selected_data(sell_offers)
    else:
        print("No se encontraron ofertas de venta con los filtros especificados.")

if __name__ == "__main__":
    main()