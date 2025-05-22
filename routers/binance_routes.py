from fastapi import APIRouter, Query
from apps.binance_adapter.main import main as binance_main
from apps.binance_adapter.db_handler import get_all_data

router = APIRouter(prefix="/binance", tags=["binance"])

@router.get("/run")
def run_binance_handler(
    asset: str = Query(..., description="Activo, por ejemplo USDT"),
    fiat: str = Query(..., description="Moneda fiat, por ejemplo VES"),
    cantidad_minima: float | None = Query(None, description="Cantidad mínima opcional")
):
    """Ejecutar el handler de Binance para obtener precios de arbitraje"""
    try:
        binance_main(asset, fiat, cantidad_minima)
        return {
            "status": "success", 
            "message": "Binance handler ejecutado correctamente",
            "params": {
                "asset": asset,
                "fiat": fiat,
                "cantidad_minima": cantidad_minima
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/data")
def get_binance_data():
    """Obtener todos los datos históricos de Binance"""
    try:
        data = get_all_data()
        return {
            "status": "success", 
            "data": data,
            "count": len(data) if data else 0
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}