from pydantic import BaseModel
from typing import Optional, List

class Offer(BaseModel):
    offer_id: Optional[str]
    user_id: Optional[str]
    username: Optional[str]
    offer_status: Optional[int]
    offer_type: Optional[int]
    crypto_currency_id: Optional[str]
    chain: Optional[str]
    fiat_currency_id: Optional[str]
    max_limit: Optional[float]
    min_limit: Optional[float]
    fiat_crypto_exchange: Optional[float]
    payment_methods: Optional[List[str]]

class OfferFilter(BaseModel):
    type_id: int = 0
    limit: int = 10
    amount: str = ''
    amount_currency_id: str = 'USD'
    crypto_currency_id: str = 'TATUM-TRON-USDT'
    fiat_currency_id: str = 'USD'
    payment_methods: str = ''
    show_user_offers: bool = True
    show_favorite_mm_only: bool = False
    sort_asc: bool = False