from sqlalchemy import exc
from fastapi import APIRouter, Query

from src.core import crud
from src.models.user import User, UserBase, UserPublic, UserUpdate
from src.db import SessionDep
from src.utils import response

from typing import Annotated, List


router = APIRouter(prefix="/users")


# If user: User, i need the email check
# if user: UserBase, i don't need it
@router.post("", response_model=UserPublic)
def create_user(user: UserBase, session: SessionDep):
    try:
        user_db = crud.create_user(session, user)
        return response.created(user_db)

    except exc.IntegrityError as e:
        return response.bad_request({"message": "Email already exist"})
    except:
        return response.bad_request({})  # TODO


@router.get("", response_model=List[UserPublic])
def read_user(
    session: SessionDep,
    name: str = None,
    age: Annotated[int, Query(le=100)] = None,
    age_min: Annotated[int, Query(le=100)] = None,
    age_max: Annotated[int, Query(le=100)] = None,
):
    x = crud.format_query(name, age, age_min, age_max)
    users = session.exec(x).all()
    return users


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(user_id: int, session: SessionDep) -> User:
    return crud.get_user_by_id(user_id, session)


@router.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = crud.get_user_by_id(user_id, session)
    session.delete(user)
    session.commit()
    return response.OK()


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user_update: UserUpdate, session: SessionDep):
    try:
        user_db = crud.get_user_by_id(user_id, session)
        user_db = crud.update_user(session, user_db, user_update)
        return user_db

    except:
        return response.bad_request({})
