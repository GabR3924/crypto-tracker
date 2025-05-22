from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import binance_routes, eldorado_routes, user_routes, cycle_routes

app = FastAPI(
    title="Crypto Arbitrage API",
    description="API para arbitraje de criptomonedas con Binance y Eldorado",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios específicos
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de salud básica
@app.get("/")
def read_root():
    return {
        "message": "Crypto Arbitrage API está funcionando correctamente",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "crypto-arbitrage-api"}

# Registrar todos los routers
app.include_router(binance_routes.router)
app.include_router(eldorado_routes.router)
app.include_router(user_routes.router)
app.include_router(cycle_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)