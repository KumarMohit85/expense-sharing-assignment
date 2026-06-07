from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.settlements.schemas import SettlementResponse
from app.modules.settlements.service import SettlementService


router = APIRouter(tags=["Settlements"])

@router.get("/groups/{group_id}/settlements", response_model=list[SettlementResponse])
def get_settlement_suggestions(
    group_id: str,
    db: Session = Depends(get_db)
):
    return SettlementService.get_settlement_suggestions(group_id, db)
