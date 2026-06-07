from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.groups.schemas import (
    AddMemberRequest,
    CreateGroupRequest,
    GroupMemberResponse,
    GroupResponse,
)
from app.modules.groups.service import GroupService


router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)

@router.post("/", response_model=GroupResponse)
def create_group(
    payload: CreateGroupRequest,
    db: Session = Depends(get_db)
):
    return GroupService.create_group(
        payload,
        db
    )


@router.get("/", response_model=list[GroupResponse])
def get_all_groups(
    db: Session = Depends(get_db)
):
    return GroupService.get_all_groups(db)


@router.get("/{group_id}", response_model=GroupResponse)
def get_group_by_id(
    group_id: str,
    db: Session = Depends(get_db)
):
    return GroupService.get_group_by_id(group_id, db)


@router.post("/{group_id}/members", response_model=list[GroupMemberResponse])
def add_member(
    group_id: str,
    payload: AddMemberRequest,
    db: Session = Depends(get_db)
):
    return GroupService.add_member(
        group_id,
        payload,
        db
    )


@router.get("/{group_id}/members", response_model=list[GroupMemberResponse])
def get_members(
    group_id: str,
    db: Session = Depends(get_db)
):
    return GroupService.get_members(group_id, db)
