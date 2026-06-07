from app.modules.groups.models import Group, GroupMember


class GroupRepository:

    @staticmethod
    def create_group(db, group):
        db.add(group)
        db.commit()
        db.refresh(group)
        return group

    @staticmethod
    def get_all_groups(db):
        return db.query(Group).all()

    @staticmethod
    def get_group_by_id(db, group_id):
        return (
            db.query(Group)
            .filter(Group.group_id == group_id)
            .first()
        )

    @staticmethod
    def get_members(db, group_id):
        return (
            db.query(GroupMember)
            .filter(GroupMember.group_id == group_id)
            .all()
        )

    @staticmethod
    def add_member(db, member):
        db.add(member)
        db.commit()
        db.refresh(member)
        return member
    
    @staticmethod
    def is_member(
        db,
        group_id: str,
        user_id: str
    ):
        return (
            db.query(GroupMember)
            .filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            )
            .first()
        )

