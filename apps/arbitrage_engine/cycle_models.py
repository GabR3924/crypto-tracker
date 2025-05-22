from pydantic import BaseModel, Field, computed_field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CycleStatus(str, Enum):
    ACTIVO = "activo"
    COMPLETADO = "completado"

class CreateCycleRequest(BaseModel):
    target_usdt: float = Field(..., gt=0, description="Objetivo de USDT del ciclo")

class CycleResponse(BaseModel):
    id: int
    name: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    target_usdt: float
    purchased_usdt: float = 0.0
    sold_usdt: float = 0.0
    total_invested: float = 0.0
    total_returned: float = 0.0
    total_profit: float = 0.0
    status: CycleStatus = CycleStatus.ACTIVO
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @computed_field
    @property
    def purchase_progress(self) -> float:
        """Progreso de compra como porcentaje"""
        if self.target_usdt == 0:
            return 0.0
        return (self.purchased_usdt / self.target_usdt) * 100
    
    @computed_field
    @property
    def sell_progress(self) -> float:
        """Progreso de venta como porcentaje"""
        if self.purchased_usdt == 0:
            return 0.0
        return (self.sold_usdt / self.purchased_usdt) * 100
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
        use_enum_values = True

class CycleWithTransactionsResponse(CycleResponse):
    transactions: List[dict] = []