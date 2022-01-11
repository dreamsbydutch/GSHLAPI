from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2, database

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/", response_model=schemas.UserOut)
def get_user(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(
        models.User.id == current_user.id).first()

    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(role="User", **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.delete("/")
def delete_user(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id == current_user.id)
    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/", response_model=schemas.UserOut)
def update_user(updated_user: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    user_query = db.query(models.User).filter(
        models.User.id == current_user.id)
    hashed_pwd = utils.hash(updated_user.password)
    updated_user.password = hashed_pwd
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()
