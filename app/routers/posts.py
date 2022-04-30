from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from ..database import get_db, engine
from .. import models, schemas, oauth2

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


# @router.get('')
@router.get('', response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).all()

    posts = db \
        .query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                      current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content) VALUES(%s, %s) RETURNING *""", (post.title, post.content))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # does RETURNING *
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(post_id),))
    # post = cursor.fetchone()

    print(type(current_user))

    # post = db.query(models.Post)\
    #     .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) \
    #     .group_by(models.Post.id) \
    #     .filter(models.Post.id == post_id).first()

    post = db \
        .query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{post_id} was not found')

    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db), authorized=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id),))
    # post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{post_id} was not found')

    post.delete(synchronize_session=False)
    db.commit()
    return {"message": f"post with id: {post_id} was deleted"}


@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(post_id: int, post: schemas.UpdateCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title =%s, content=%s, published=%s WHERE id = %s RETURNING *""",
    #                (
    #                    post.title, post.content, post.published, str(post_id),
    #                ))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{post_id} was not found')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
