# groups/schemas.py

from datetime import datetime

from pydantic import BaseModel, Field


class CreateGroupRequest(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )


class AddMemberRequest(BaseModel):
    user_ids: list[str]


class GroupResponse(BaseModel):
    group_id: str
    name: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class GroupMemberResponse(BaseModel):
    id: int
    group_id: str
    user_id: str
    joined_at: datetime

    model_config = {
        "from_attributes": True
    }