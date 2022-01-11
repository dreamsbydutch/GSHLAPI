from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import conint


# -------------- Auth Schemas ---------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# -------------- User Schemas ---------------------------------

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class OwnerOut(BaseModel):
    id: int
    first_name: str
    last_name: str


# -------------- Team Schemas ---------------------------------

class TeamCreate(BaseModel):
    team_name: str

    class Config:
        orm_mode = True


class TeamOut(TeamCreate):
    id: int
    team_logo: str
    owner_id: int
    owner: OwnerOut


class PlayerPosition(BaseModel):
    player_id: int
    position_id: int
    dir: conint(le=1)
