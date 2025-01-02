from typing import Annotated, Any
import uuid
from fastapi import APIRouter, Query
from sqlmodel import select, func
from src.core.deps import SessionDep
from src.models import Todo, TodoCreate, TodoPublic, TodoUpdate, TodosPublic
from src.model import todos_model

router=APIRouter(
  prefix ="/todos", 
  tags=["todos"],
  dependencies=[]
)

@router.get("/", response_model= TodosPublic)
def read_todos(
  session: SessionDep, 
  limit: Annotated[int, Query(le=20)]=20,
  offset: Annotated[int, Query(ge=0)]=0
)-> list[Todo]:
  todos, count = todos_model.get_todos(session, limit, offset)
  return TodosPublic(data= todos, count=count)


@router.post("/", response_model=TodoPublic)
def create_todo(
  session: SessionDep,
  todo_in: TodoCreate
) -> Any:
  return todos_model.create_todo(session, todo_in)


@router.put("/{id}", response_model=TodoPublic)
def update_todo(
  session:SessionDep, 
  id:uuid.UUID,
  todo_in: TodoUpdate
)-> Any:
  todo = todos_model.update_todo(
    session=session, todo_id=id, todo_in=todo_in)
  return todo
  

@router.delete("/{id}")
def delete_todo(
  session:SessionDep, 
  id:uuid.UUID,
) -> Any:
  message = todos_model.delete_todo(session=session, todo_id=id)
  return message