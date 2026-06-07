# expenses/schemas.py

from datetime import datetime

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    user_id: str
    name: str


class CreateExpenseRequest(BaseModel):
    group_id: str
    paid_by: str
    amount: float = Field(gt=0)
    description: str = Field(
        min_length=1,
        max_length=255
    )


class ExpenseResponse(BaseModel):
    expense_id: str
    group_id: str
    paid_by: UserInfo
    amount: float
    description: str
    created_at: datetime


class ExpenseShareResponse(BaseModel):
    id: int
    expense_id: str
    user_id: str
    share_amount: float

    model_config = {
        "from_attributes": True
    }
