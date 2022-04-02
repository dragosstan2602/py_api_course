from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from .. import models, database, schemas, utils, oauth2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 100, skip: int = 0,
              search: Optional[str] = ""):

    posts = db.query(models.Post, 
                       func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                            models.Vote.post_id == models.Post.id, 
                                                                            isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,
             db: Session = Depends(database.get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    
    # query on the DB filtering by the ID -> .first() stops the query after the first match
    post = db.query(models.Post, 
                    func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                         models.Vote.post_id == models.Post.id, 
                                                                         isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(database.get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # To authenticate with the token just do a post request with the following header
    # key: Authorization
    # value: Bearer token_value (Bearer is a string and the space after it is important)
    # Or in Authorization tab just select type Bearer and paste in the token
    
    # **post.dict() unpacks the post variable so you don't have to do
    # title=post.title, content=post.content etc etc
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    
    # print(current_user.id)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
    #                (str(id)))
    # deleted_post = cursor.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
        
    post_query.delete(synchronize_session=False)
    
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, 
                post: schemas.PostCreate, 
                db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    
    my_post = post_query.first()
    
    if my_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} was not found')
        
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
        
    post_query.update(post.dict(), synchronize_session=False) 
       
    db.commit()  
       
    return post_query.first()