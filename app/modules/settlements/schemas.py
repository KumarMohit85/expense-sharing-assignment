# settlements/schemas.py

from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: str
    name: str


class SettlementResponse(BaseModel):
    from_user: UserInfo
    to_user: UserInfo
    amount: float
