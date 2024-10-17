


from fastapi import HTTPException
from sqlmodel import Session, select, func

from src.models import Message, Todo, TodoCreate, TodoUpdate


def create_todo(session: Session, todo_in: TodoCreate)-> Todo:
  todo = Todo.model_validate(todo_in)
  session.add(todo)
  session.commit()
  session.refresh(todo)
  return todo
  
def get_todos(session:Session, limit:int, offset:int)-> tuple[list[Todo], int]:
  count_q= select(func.count()).select_from(Todo)
  count = session.exec(count_q).one()
  q = select(Todo).offset(offset).limit(limit)
  todos = session.exec(q).all()
  return todos, count

def update_todo(session:Session, todo_id:str, todo_in:TodoUpdate)-> Todo:
  todo = session.get(Todo, todo_id)
  if not todo:
    raise HTTPException(status_code=404, detail="Todo not found")
  update_dict = todo_in.model_dump(exclude_unset=True)
  todo.sqlmodel_update(update_dict)
  session.add(todo)
  session.commit()
  session.refresh(todo)
  return todo

def delete_todo(session:Session, todo_id:str)->Message:
  todo = session.get(Todo, todo_id)
  if not todo:
    raise HTTPException(status_code=404, detail="Todo not found")
  session.delete(todo)
  session.commit()
  return Message(message="Todo deleted successfully")
  
  