from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.expenses.schemas import CreateExpenseRequest, ExpenseResponse
from app.modules.expenses.service import ExpenseService


router = APIRouter(tags=["Expenses"])

@router.post("/expenses", response_model=ExpenseResponse)
def create_expense(
    payload: CreateExpenseRequest,
    db: Session = Depends(get_db)
):
    return ExpenseService.create_expense(
        payload,
        db
    )


@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense_by_id(
    expense_id: str,
    db: Session = Depends(get_db)
):
    return ExpenseService.get_expense_by_id(expense_id, db)


@router.get("/groups/{group_id}/expenses", response_model=list[ExpenseResponse])
def get_group_expenses(
    group_id: str,
    db: Session = Depends(get_db)
):
    return ExpenseService.get_group_expenses(group_id, db)
