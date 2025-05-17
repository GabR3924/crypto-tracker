from fastapi import FastAPI, Query, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from apps.binance_adapter.main import main
from apps.binance_adapter.db_handler import get_all_data  # <-- IMPORTANTE
from apps.eldorado_adapter.main import main
from apps.eldorado_adapter.schemas import OfferFilter, Offer
from apps.eldorado_adapter.handler import get_buy_and_sell_offers, get_offers_with_headers
from typing import List, Dict, Any
from apps.login.schemas import User  # Modelo Pydantic
from apps.login.handler import register_user, init_user_system
from apps.login.db_handler import get_all_users

app = FastAPI()

# Si estás usando el frontend desde otro dominio/puerto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especifica tu dominio frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI está funcionando correctamente"}

@app.post("/user/register")
def register_user_route(user: User = Body(...)):
    try:
        success = register_user(user)
        if success:
            return {"status": "success", "message": "Usuario registrado correctamente"}
        else:
            return {"status": "error", "message": "El correo ya está registrado"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/user/all")
def get_all_users_route():
    try:
        users = get_all_users()
        return {"status": "success", "data": users}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/binance/run")
def run_binance_handler(
    asset: str = Query(..., description="Activo, por ejemplo USDT"),
    fiat: str = Query(..., description="Moneda fiat, por ejemplo VES"),
    cantidad_minima: float | None = Query(None)  # cantidad mínima opcional

    # cantidad_minima: float = Query(..., description="Cantidad mínima deseada")
):
    try:
        main(asset, fiat, cantidad_minima)
        return {"status": "success", "message": "Binance handler ejecutado correctamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/binance/data")
def get_binance_data():
    try:
        data = get_all_data()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


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

@app.get("/eldorado/run")
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
            }
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )