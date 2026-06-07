from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.balances.schemas import BalanceResponse
from app.modules.balances.service import BalanceService


router = APIRouter(tags=["Balances"])

@router.get("/groups/{group_id}/balances", response_model=list[BalanceResponse])
def get_group_balances(
    group_id: str,
    db: Session = Depends(get_db)
):
    return BalanceService.get_group_balances(group_id, db)


@router.get("/groups/{group_id}/balances/pairwise")
def get_pairwise_balances(
    group_id: str,
    db: Session = Depends(get_db)
):

    return BalanceService.get_pairwise_balances(group_id, db)
