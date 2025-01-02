


from fastapi import HTTPException
from sqlmodel import Session, desc, select, func
from sqlalchemy.orm.attributes import flag_modified

from src.models import Message, Todo, TodoCreate, TodoUpdate, TodosPosition

TODO_POSITION_ID= "default"


def create_todo(session: Session, todo_in: TodoCreate)-> Todo:
  # Add postion as last 
  todo = Todo.model_validate(todo_in)  
  session.add(todo)
  add_to_position(session, todo.id)
  session.commit()
  session.refresh(todo)
  return todo 

def get_todo(session:Session, id:str)-> Todo:
  todo= session.get(Todo, id)
  if not todo:
    raise HTTPException(status_code=404, detail="Todo not found")
  return todo
  
def get_todos(session:Session, limit:int=20, offset:int=0)-> tuple[list[Todo], int]:
  count_q= select(func.count()).select_from(Todo)
  count = session.exec(count_q).one()
  q = select(Todo).offset(offset).limit(limit)
  
  todos = session.exec(q).all()  
  order = get_positions(session)
  
  if not order :
    return todos, count
  
  # initialize list for sorted todos
  ordered_todos = []
  # order todos based on array of id's 
  for id in order:
    for todo in todos:
      if str(todo.id) == id:
        ordered_todos.append(todo)
  
  return ordered_todos, count

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
  
  delete_position(session, todo_id)
  session.delete(todo)
  session.commit()
    
  return Message(message="Todo deleted successfully")
  
  
def add_to_position(session:Session, todo_id:str):
  todos_position = session.get(TodosPosition, TODO_POSITION_ID)
  
  if todos_position :
    # add new id to postion array
    newData = dict(todos_position.data)
    newData["order"]= [*newData["order"], str(todo_id)]
    todos_position.data= newData
    
    session.add(todos_position)
    return
  
  raise HTTPException(status_code=404, detail="Todo order not found")
  
def delete_position(session:Session, todo_id:str):
  todos_position = session.get(TodosPosition, TODO_POSITION_ID)
  
  if todos_position :
    newData = dict(todos_position.data)
    
    newOrder = list(newData["order"])
    newOrder.remove(str(todo_id))
    
    newData["order"]= newOrder
    
    todos_position.data = newData
    flag_modified(todos_position, "data")
    
    
    session.add(todos_position)    
    return 
    
  raise HTTPException(status_code=404, detail="Todo order not found")
  
  
def sort_todos(session:Session, newOrder:list[str]):
  todos_position = session.get(TodosPosition, TODO_POSITION_ID)
  if todos_position :
    
    newData = dict(todos_position.data)
    newData["order"] = newOrder
    
    todos_position.data = newData
    flag_modified(todos_position, "data")
    
    session.add(todos_position)   
    session.commit()
    return 
  
  raise HTTPException(status_code=404, detail="Todo order not found")
  
def get_positions(session:Session)-> list[str]:
  todos_position = session.get(TodosPosition, TODO_POSITION_ID)
  if not todos_position: 
    return None 
  return (dict(todos_position.data))["order"]