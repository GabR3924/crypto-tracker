from .handler import get_offers_with_headers, display_selected_data, get_buy_and_sell_offers
from .schemas import OfferFilter

def main(
    limit=10,
    amount='',
    amount_currency_id='USD',
    crypto_currency_id='TATUM-TRON-USDT',
    fiat_currency_id='USD',
    payment_methods='',
    show_user_offers=True,
    show_favorite_mm_only=False
):
    filter_params = OfferFilter(
        limit=limit,
        amount=amount,
        amount_currency_id=amount_currency_id,
        crypto_currency_id=crypto_currency_id,
        fiat_currency_id=fiat_currency_id,
        payment_methods=payment_methods,
        show_user_offers=show_user_offers,
        show_favorite_mm_only=show_favorite_mm_only
    )

    print(f"Buscando ofertas con payment_method: {filter_params.payment_methods}")
    
    buy_offers, sell_offers = get_buy_and_sell_offers(filter_params)
    
    print(f"\nOFERTAS DE COMPRA: {len(buy_offers)} encontradas")
    if buy_offers:
        display_selected_data(buy_offers)
    else:
        print("No se encontraron ofertas de compra con los filtros especificados.")
    
    print(f"\nOFERTAS DE VENTA: {len(sell_offers)} encontradas")
    if sell_offers:
        display_selected_data(sell_offers)
    else:
        print("No se encontraron ofertas de venta con los filtros especificados.")


if __name__ == "__main__":
    main()