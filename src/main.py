from contextlib import asynccontextmanager
from typing import Annotated, Any, Union
from fastapi import FastAPI, Query
from sqlmodel import  select, func

from src.core.db import create_db_and_tables
from src.core.deps import SessionDep

from src.models import Todo, TodoCreate, TodoPublic, TodosPublic

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    

app = FastAPI(lifespan=lifespan)

@app.get("/todos", response_model= TodosPublic)
def read_todos(
  session: SessionDep, 
  limit: Annotated[int, Query(le=20)]=20,
  offset: Annotated[int, Query(ge=0)]=0
)-> list[Todo]:
  count_q= select(func.count()).select_from(Todo)
  count = session.exec(count_q).one()
  q = select(Todo).offset(offset).limit(limit)
  todos = session.exec(q).all()
  return TodosPublic(data= todos, count=count)


@app.post("/todos", response_model=TodoPublic)
def create_todo(
  session: SessionDep,
  todo_in: TodoCreate
) -> Any:
  todo = Todo.model_validate(todo_in)
  session.add(todo)
  session.commit()
  session.refresh(todo)
  return todo
