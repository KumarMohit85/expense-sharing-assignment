from sqlalchemy.orm import Session

from .models import User

class UserRepository:
    @staticmethod
    def create_user(
        db:Session,
        name:str
        )-> User:
             user = User(name=name)
             db.add(user)
             db.commit()
             db.refresh(user)
             return user
    
    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str):
        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )
