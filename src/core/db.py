from sqlmodel import SQLModel, Session, create_engine

from src.model.todos_model import get_todos
from src.models import TodosPosition

sqlite_file_name = "todo_db.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables(session:Session):
  SQLModel.metadata.create_all(engine)
  #Get todos positions
  todos_positions = session.get(TodosPosition, "default")
  if not todos_positions:
    todos, count = get_todos(session=session)
    order = []
    if todos :
      for todo in todos:
        order.append(str(todo.id))  
    todos_positions= TodosPosition(id="default", data={"order":order})
    session.add(todos_positions)
    session.commit()          
    
  
