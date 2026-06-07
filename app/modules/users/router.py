from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from .schemas import CreateUserRequest, UserResponse
from .service import UserService

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/")
def create_user(payload:CreateUserRequest,db:Session=Depends(get_db)):
       return UserService.create_user(payload,db)

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db)
):
    return UserService.get_all_users(db)

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db)
):
    return UserService.get_user_by_id(user_id, db)