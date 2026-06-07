from fastapi import HTTPException

from app.modules.groups.repository import GroupRepository
from app.modules.users.repository import UserRepository

from .models import Group, GroupMember


class GroupService:
    @staticmethod
    def create_group(payload, db):

        group = Group(
            name=payload.name
        )

        return GroupRepository.create_group(db, group)

    @staticmethod
    def get_all_groups(db):
        return GroupRepository.get_all_groups(db)

    @staticmethod
    def get_group_by_id(group_id, db):
        group = GroupRepository.get_group_by_id(db, group_id)

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        return group

    @staticmethod
    def get_members(group_id, db):
        group = GroupRepository.get_group_by_id(db, group_id)

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        return GroupRepository.get_members(db, group_id)

    @staticmethod
    def add_member(group_id: str, payload, db):
        group = GroupRepository.get_group_by_id(
            db,
            group_id
        )

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )

        if not payload.user_ids:
            raise HTTPException(
                status_code=400,
                detail="user_ids must contain at least one user"
            )

        created_members = []
        for user_id in payload.user_ids:
            user = UserRepository.get_user_by_id(db, user_id)

            if not user:
                raise HTTPException(
                    status_code=404,
                    detail=f"User not found: {user_id}"
                )

            existing_member = GroupRepository.is_member(
                db,
                group_id,
                user_id
            )

            if existing_member:
                raise HTTPException(
                    status_code=409,
                    detail=f"User already belongs to this group: {user_id}"
                )

            member = GroupMember(
                group_id=group_id,
                user_id=user_id
            )
            created_members.append(member)

        db.add_all(created_members)
        db.commit()
        for member in created_members:
            db.refresh(member)

        return created_members