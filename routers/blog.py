from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .oauth2 import get_current_user
from .. import schema, database, models

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"],
    responses={
            404: {"user": "User is not authenticated"}
        }
)


@router.get("/", response_model=List[schema.ShowBlog])
def get_all_post(db: Session = Depends(database.get_db), current_user: schema.User = Depends(get_current_user)):
    return db.query(models.Blog).all()



@router.get("/{id}", response_model=schema.ShowBlog)
def get_blog_by_id(id: int, db: Session = Depends(database.get_db)):
    blog_model = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"not found a blog with {id}"})
    return blog_model


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(blog: schema.BlogSchema, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db)):
    blog_model = db.query(models.Blog).filter(models.Blog.id == id)
    if blog_model.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Resource with id {id} not found")
    blog_model.delete(synchronize_session=False)
    db.commit()
    return {"Message": f"Item with id {id} has been deleted"}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schema.BlogSchema, db: Session = Depends(database.get_db)):
    blog_model = db.query(models.Blog).filter(models.Blog.id == id)
    if blog_model.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Resource with id {id} not found")
    blog_model.update(request.dict(), synchronize_session=False)
    db.commit()
    return {"Message": f"Item with id {id} has been updated"}