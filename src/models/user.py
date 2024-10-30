from pydantic import EmailStr
from sqlmodel import Field, SQLModel, AutoString


# Data shared by all user models
class UserBase(SQLModel):
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)
    age: int | None = Field(default=None, index=True)
    active: bool | None = Field(default=True, index=True)


# Database table will have everything from UserBase + User
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


# Data to return in requests
# Lets say there's some more values in User that are not present here, beyond id
class UserPublic(UserBase):
    id: int


# Every value from UserBase is optional, therefore every value from the base class can be updated
class UserUpdate(UserBase):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = None
    active: bool | None = None
