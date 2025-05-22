from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class CreateBuyTransactionRequest(BaseModel):
    usdt_desired: float = Field(..., gt=0, description="USDT deseados para comprar")
    commission_rate: float = Field(..., ge=0, description="Tasa de comisión")
    purchase_price: float = Field(..., gt=0, description="Precio de compra")
    usdt_to_pay: float = Field(..., gt=0, description="USDT a pagar")
    total_investment_bs: float = Field(..., gt=0, description="Inversión total en Bs")
    real_purchase_price: float = Field(..., gt=0, description="Precio real de compra")

class CreateSellTransactionRequest(BaseModel):
    market_best_price: float = Field(..., gt=0, description="Mejor precio del mercado")
    competitive_adjustment: Optional[float] = Field(None, description="Ajuste competitivo")
    sale_price: float = Field(..., gt=0, description="Precio de venta")
    usdt_sold: float = Field(..., gt=0, description="USDT vendidos")
    profit_bs: Optional[float] = Field(None, description="Ganancia en Bs")
    profit_percentage: Optional[float] = Field(None, description="Porcentaje de ganancia")

class LinkedBuy(BaseModel):
    buy_id: int
    amount: float
    buy_price: float

class BuyTransactionResponse(BaseModel):
    id: int
    cycle_id: int
    transaction_type: str
    usdt_desired: float
    commission_rate: float
    purchase_price: float
    usdt_to_pay: float
    total_investment_bs: float
    real_purchase_price: float
    buy_status: str
    transaction_date: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SellTransactionResponse(BaseModel):
    id: int
    cycle_id: int
    transaction_type: str
    market_best_price: float
    competitive_adjustment: Optional[float]
    sale_price: float
    usdt_sold: float
    profit_bs: Optional[float]
    profit_percentage: Optional[float]
    transaction_date: datetime
    linked_buys: List[LinkedBuy]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PendingBuysResponse(BaseModel):
    pending_buys: List[BuyTransactionResponse]
    total_available_usdt: float