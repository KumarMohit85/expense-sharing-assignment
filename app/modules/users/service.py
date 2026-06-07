from fastapi import HTTPException

from .repository import UserRepository

class UserService:
    @staticmethod
    def create_user(payload,db):
           return UserRepository.create_user(db=db,name=payload.name)

    @staticmethod
    def get_all_users(db):
        return UserRepository.get_all_users(db)

    @staticmethod
    def get_user_by_id(user_id, db):
        user = UserRepository.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user