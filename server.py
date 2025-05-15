from fastapi import FastAPI
from apps.binance_adapter.main import main  # importa tu main

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI está funcionando correctamente"}

@app.get("/binance/run")
def run_binance_handler():
    try:
        main()
        return {"status": "success", "message": "Binance handler ejecutado correctamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
