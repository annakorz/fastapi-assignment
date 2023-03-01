from sqlalchemy.orm import Session
from models import User



def get_user_by_email(db: Session, user: User):
    return db.query(User).filter(User.email == user.email).one_or_none()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).one_or_none()



