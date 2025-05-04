from typing import Annotated

import models
from database import SessionLocal, engine
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from routers import auth
from sqlalchemy.orm import Session

router = APIRouter(prefix="/todos", tags=["todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=10, max_length=100)
    priority: int = Field(gt=0, le=5)
    complete: bool = Field(default=False)

    class Config:
        from_attributes = True


@router.get("/")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Todo).all()


@router.get("/todo/{todo_id}")
async def read_todo(
    todo_id: Annotated[int, Path(..., gt=0)], db: Annotated[Session, Depends(get_db)]
):
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, db: Annotated[Session, Depends(get_db)]):
    todo_model = models.Todo(**todo_request.model_dump(), owner_id=1)
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return {"todo_model": todo_model}


@router.put("/todo/{todo_id}", status_code=status.HTTP_202_ACCEPTED, response_model=TodoRequest)
async def update_todo(
    todo_id: Annotated[int, Path(..., gt=0)],
    todo_request: Annotated[TodoRequest, Body(...)],
    db: Annotated[Session, Depends(get_db)],
):
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model


@router.delete("/todo/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_todo(
    todo_id: Annotated[int, Path(..., gt=0)],
    db: Annotated[Session, Depends(get_db)],
):
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()

    return {"message": "Todo deleted successfully"}
