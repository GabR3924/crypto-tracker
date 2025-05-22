from fastapi import APIRouter, HTTPException, Depends
from typing import List
from apps.arbitrage_engine.cycle_handler import CycleHandler
from apps.arbitrage_engine.transaction_handler import TransactionHandler
from apps.arbitrage_engine.cycle_models import (
    CycleResponse, 
    CreateCycleRequest, 
    CycleWithTransactionsResponse
)
from apps.arbitrage_engine.transaction_models import (
    CreateBuyTransactionRequest,
    CreateSellTransactionRequest,
    BuyTransactionResponse,
    SellTransactionResponse,
    PendingBuysResponse
)
from apps.arbitrage_engine.database import get_database

router = APIRouter(prefix="/api/cycles", tags=["cycles", "transactions"])

def get_cycle_handler(db=Depends(get_database)):
    return CycleHandler(db)

def get_transaction_handler(db=Depends(get_database)):
    return TransactionHandler(db)

# ============= RUTAS DE CICLOS =============

@router.get("/", response_model=List[CycleResponse])
async def get_all_cycles(handler: CycleHandler = Depends(get_cycle_handler)):
    """Obtener todos los ciclos"""
    return await handler.get_all_cycles()

@router.get("/active", response_model=List[CycleResponse])
async def get_active_cycles(handler: CycleHandler = Depends(get_cycle_handler)):
    """Obtener solo ciclos activos"""
    return await handler.get_active_cycles()

@router.get("/{cycle_id}", response_model=CycleWithTransactionsResponse)
async def get_cycle_by_id(
    cycle_id: int, 
    handler: CycleHandler = Depends(get_cycle_handler)
):
    """Obtener un ciclo específico con sus transacciones"""
    return await handler.get_cycle_by_id(cycle_id)

@router.post("/", response_model=CycleResponse, status_code=201)
async def create_cycle(
    cycle_data: CreateCycleRequest,
    handler: CycleHandler = Depends(get_cycle_handler)
):
    """Crear un nuevo ciclo"""
    return await handler.create_cycle(cycle_data.target_usdt)

@router.put("/{cycle_id}/finish", response_model=CycleResponse)
async def finish_cycle(
    cycle_id: int,
    handler: CycleHandler = Depends(get_cycle_handler)
):
    """Finalizar un ciclo"""
    return await handler.finish_cycle(cycle_id)

@router.delete("/{cycle_id}")
async def delete_cycle(
    cycle_id: int,
    handler: CycleHandler = Depends(get_cycle_handler)
):
    """Eliminar un ciclo"""
    await handler.delete_cycle(cycle_id)
    return {"success": True, "message": "Ciclo eliminado exitosamente"}

# ============= RUTAS DE TRANSACCIONES =============

@router.post("/{cycle_id}/transactions/buy", response_model=BuyTransactionResponse, status_code=201)
async def create_buy_transaction(
    cycle_id: int,
    transaction_data: CreateBuyTransactionRequest,
    handler: TransactionHandler = Depends(get_transaction_handler)
):
    """Registrar una compra"""
    return await handler.create_buy_transaction(cycle_id, transaction_data)

@router.post("/{cycle_id}/transactions/sell", response_model=SellTransactionResponse, status_code=201)
async def create_sell_transaction(
    cycle_id: int,
    transaction_data: CreateSellTransactionRequest,
    handler: TransactionHandler = Depends(get_transaction_handler)
):
    """Registrar una venta"""
    return await handler.create_sell_transaction(cycle_id, transaction_data)

@router.get("/{cycle_id}/pending-buys", response_model=PendingBuysResponse)
async def get_pending_buys(
    cycle_id: int,
    handler: TransactionHandler = Depends(get_transaction_handler)
):
    """Obtener compras pendientes de un ciclo"""
    return await handler.get_pending_buys(cycle_id)