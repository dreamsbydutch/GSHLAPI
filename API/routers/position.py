from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2, database

router = APIRouter(
    prefix="/position_change",
    tags=['PositionChange']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def position_change(position_change: schemas.PlayerPosition, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    player = db.query(models.Player).filter(
        models.Player.id == position_change.player_id).first()
    position = db.query(models.Position).filter(
        models.Position.id == position_change.position_id).first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Player with id {position_change.player_id} does not exist")
    if not position:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Position with id {position_change.position_id} does not exist")

    position_change_query = db.query(models.PlayerPosition).filter(models.PlayerPosition.player_id ==
                                                                   position_change.player_id, models.PlayerPosition.position_id == position_change.position_id)
    found_player_position = position_change_query.first()

    if (position_change.dir == 1):
        if found_player_position:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"player {position_change.player_id} already has eligibility for position {position_change.position_id}")
        new_position_change = models.PlayerPosition(player_id=position_change.player_id,
                                                    position_id=position_change.position_id)
        db.add(new_position_change)
        db.commit()
        return {"message": "Succesfully added new player position"}

    else:
        if not found_player_position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Player position does not exist")

        position_change_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Succesfully deleted player position"}
