from typing import Optional

from fastapi import HTTPException

from sqlmodel import Session, select
from src.models.user import User, UserBase


def format_query(name, age, age_min, age_max):
    x = select(User)
    if name:
        # https://github.com/fastapi/sqlmodel/issues/153#issuecomment-964994946
        x = x.where(User.name.like(name + "%"))
    if age:
        x = x.where(User.age == age)
    elif age_min and age_max:
        x = x.where(User.age >= age_min, User.age <= age_max)
    elif age_min:
        x = x.where(User.age >= age_min)
    elif age_max:
        x = x.where(User.age <= age_max)
    return x


def create_user(session: Session, user_create: UserBase) -> User:
    db_user = User.model_validate(user_create)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, user_db: User, user_update: UserBase) -> User:
    user_data = user_update.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


def get_user_by_id(user_id: int, session: Session) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
