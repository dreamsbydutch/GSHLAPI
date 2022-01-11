from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2, database

router = APIRouter(
    prefix="/teams",
    tags=['Teams']
)


@router.get("/", response_model=List[schemas.TeamOut])
def get_teams(db: Session = Depends(database.get_db)):
    teams = db.query(models.Team).all()
    return teams


@router.get("/{id}", response_model=schemas.TeamOut)
def get_team(id: int, db: Session = Depends(database.get_db)):

    team = db.query(models.Team).filter(models.Team.id == id).first()

    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"team with id: {id} was not found")

    return team
