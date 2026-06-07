# balances/schemas.py

from typing import Dict

from pydantic import BaseModel


class BalanceResponse(BaseModel):
    user_id: str
    name: str
    balance: float



