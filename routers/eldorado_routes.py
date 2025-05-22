from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from apps.eldorado_adapter.schemas import OfferFilter, Offer
from apps.eldorado_adapter.handler import get_buy_and_sell_offers
from typing import List, Dict, Any

router = APIRouter(prefix="/eldorado", tags=["eldorado"])

def format_offers(offers: List[Offer]) -> List[Dict[str, Any]]:
    """Convierte la lista de objetos Offer a formato JSON para la respuesta"""
    result = []
    for offer in offers:
        # Convertir el modelo Pydantic a diccionario, respetando los valores opcionales
        offer_dict = offer.dict()
        # Asegurar que payment_methods sea una lista vacía si es None
        if offer_dict["payment_methods"] is None:
            offer_dict["payment_methods"] = []
        result.append(offer_dict)
    return result

@router.get("/run")
def run_eldorado_handler(
    limit: int = Query(10, description="Límite de ofertas"),
    amount: str = Query('', description="Cantidad específica"),
    amount_currency_id: str = Query('USD', description="ID de moneda de cantidad"),
    crypto_currency_id: str = Query('TATUM-TRON-USDT', description="ID de criptomoneda"),
    fiat_currency_id: str = Query('USD', description="ID de moneda fiat"),
    payment_methods: str = Query('', description="Métodos de pago"),
    show_user_offers: bool = Query(True, description="Mostrar ofertas del usuario"),
    show_favorite_mm_only: bool = Query(False, description="Mostrar solo ofertas de MM favoritos"),
):
    """Obtener ofertas de compra y venta de Eldorado"""
    try:
        # Creamos el filtro base con los parámetros comunes
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
        
        # Obtenemos tanto ofertas de compra como de venta
        buy_offers, sell_offers = get_buy_and_sell_offers(filter_params)
        
        # Formateamos los resultados para JSON
        formatted_buy_offers = format_offers(buy_offers)
        formatted_sell_offers = format_offers(sell_offers)
        
        # Construimos la respuesta
        result = {
            "status": "success",
            "buy_offers": {
                "count": len(formatted_buy_offers),
                "data": formatted_buy_offers
            },
            "sell_offers": {
                "count": len(formatted_sell_offers),
                "data": formatted_sell_offers
            },
            "filters_applied": filter_params.dict()
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )