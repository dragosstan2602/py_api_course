from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, database, schemas, utils


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/{id}", response_model=schemas.UserOutput)
def get_posts(id: int, 
              db: Session = Depends(database.get_db)):
    
    # query on the DB filtering by the ID -> .first() stops the query after the first match
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} was not found")
    
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate, 
                db: Session = Depends(database.get_db)):
    # Check if user already exists
    user_check = db.query(models.User).filter(models.User.email == user.email).first()
    
    if user_check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'user with email {user.email} already exists')
    # Hash user.password
    user.password = utils.hash_password(user.password)
    
    new_user = models.User(**user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user