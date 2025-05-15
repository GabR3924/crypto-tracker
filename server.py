from fastapi import FastAPI, Query
from apps.binance_adapter.main import main
from apps.binance_adapter.db_handler import get_all_data  # <-- IMPORTANTE

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI está funcionando correctamente"}

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
