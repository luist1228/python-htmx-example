

import json
from typing import Annotated, Any
import uuid
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
import markdown

from src.model import todos_model
from src.models import SortList, TodoCreate, TodoUpdate
from ..deps import ClientDep
from src.core.deps import SessionDep


router=APIRouter(
  prefix ="/todos", 
  tags=["todos"],
  dependencies=[]
)

@router.get("/", response_class=HTMLResponse)
def todos_main_page(session: SessionDep, request: Request, clientDep:ClientDep):
  todos, count = todos_model.get_todos(session=session)
  
  return clientDep.htmx_template_response(
        request=request, 
        name="pages/todos_page.html",
        context= {
            "title" : "Todos",
            "todos" : todos
        }
    )


@router.post("/", response_class=HTMLResponse)
def create_todo(
  request: Request, 
  session:SessionDep, 
  clientDep:ClientDep,
  todo_in: Annotated[TodoCreate, Form()],
) -> Any:
  todo=todos_model.create_todo(session=session, todo_in=todo_in)
  html_md=""
  if todo.description:
    html_md = markdown.markdown(
      todo.description,
      extensions=['tables','fenced_code'],
      tab_length=2
    )
  return clientDep.htmx_template_response(
        request=request, 
        name="pages/edit_todo_page.html",
        headers={
            "HX-Replace-Url":"/todos/"+str(todo.id)
        },
        context= {
            "todo" : todo,
            "md":html_md
        }
    )
  
@router.get("/{id}", response_class=HTMLResponse)
def get_todo(
  request: Request, 
  session:SessionDep, 
  clientDep:ClientDep,
  id:uuid.UUID
) -> Any:
  todo=todos_model.get_todo(session=session, id=id)
  html_md=""
  if todo.description:
    html_md = markdown.markdown(
      todo.description,
      extensions=['tables','fenced_code','markdown_checklist.extension'],
      tab_length=4
    )
  return clientDep.htmx_template_response(
        request=request, 
        name="pages/todo_page.html",
        headers={
            "HX-Replace-Url":"/todos/"+str(todo.id)
        },
        context= {
            "todo" : todo,
            "md":html_md
        }
    )

@router.patch("/{id}", response_class=HTMLResponse)
def update_todo(
  request: Request, 
  session:SessionDep, 
  clientDep:ClientDep, 
  id:uuid.UUID,
  todo_in: Annotated[TodoUpdate, Form()]
)-> Any:
  todo = todos_model.update_todo(session=session, todo_id=id, todo_in=todo_in)
  return clientDep.htmx_template_response(
        request=request, 
        name="partials/todo.html",
        context= {
          "todo":todo
        }
    )
  
  
@router.delete("/{id}", response_class=HTMLResponse)
def delete_todo(
  clientDep:ClientDep, 
  request: Request, 
  session:SessionDep, 
  
  id:uuid.UUID, 
)-> Any:
  todos_model.delete_todo(session, id)
  todos, _ = todos_model.get_todos(session=session)
  return clientDep.htmx_template_response(
        request=request, 
        name="partials/todos_list.html",
        context= {
            "todos" : todos
        }
    )
  
@router.post("/delete/{id}",response_class=HTMLResponse)
def delete_todo(
  clientDep:ClientDep, 
  request: Request, 
  session:SessionDep, 
  id:uuid.UUID, 
)-> Any:
  todos_model.delete_todo(session, id)
  todos, _ = todos_model.get_todos(session=session)
  return clientDep.htmx_template_response(
      request=request, 
      name="pages/todos_page.html",
      context= {
          "todos" : todos
      }
  )

@router.get("/edit/{id}", response_class=HTMLResponse)
def edit_todo_page(
  clientDep:ClientDep, 
  request:Request, 
  session:SessionDep, 
  id:uuid.UUID
)-> Any:
  todo = todos_model.get_todo(session=session, id=id)
  html_md=""
  if todo.description:
    html_md = markdown.markdown(
      todo.description,
      extensions=['tables','fenced_code'],
      tab_length=2
    )
  return clientDep.htmx_template_response(
        request=request, 
        name="pages/edit_todo_page.html",
        context= {
            "title" : "Todos",
            "todo" : todo,
            "md":html_md
        }
    )
  
@router.put("/edit/{id}", response_class=HTMLResponse)
def edit_todo(
  clientDep:ClientDep, 
  request:Request, 
  session:SessionDep, 
  id:uuid.UUID,
  todo_in: Annotated[TodoUpdate, Form()]
)->Any:
  todo = todos_model.update_todo(session=session, todo_id=id, todo_in=todo_in)
  hx_location = {"path":"/todos/"+str(todo.id), "target":"#app-content", "swap":"innerHTML"}
  json_header = json.dumps(hx_location)
  return clientDep.htmx_template_response(
        request=request, 
        name="pages/todo_page.html",
        headers={
            "HX-Location":str(json_header)
        },
        context= {
            "title" : "Todos",
            "todo" : todo
        }
    )
  
@router.post("/edit/{id}", response_class=HTMLResponse)
def edit_todo(
  clientDep:ClientDep, 
  request:Request, 
  session:SessionDep, 
  id:uuid.UUID,
  todo_in: Annotated[TodoUpdate, Form()]
)->Any:
  todo = todos_model.update_todo(session=session, todo_id=id, todo_in=todo_in)
  return clientDep.htmx_template_response(
        request=request, 
        name="pages/todo_page.html",
        context= {
            "title" : "Todos",
            "todo" : todo
        }
    )
  
@router.post("/toggle/{id}", response_class=HTMLResponse)
def toggle_todo(
  clientDep:ClientDep, 
  request:Request, 
  session:SessionDep, 
  id:uuid.UUID,
  todo_in: Annotated[TodoUpdate, Form()]
)->Any:
  todos_model.update_todo(session=session, todo_id=id, todo_in=todo_in)
  todos, _ = todos_model.get_todos(session=session)
 
  return clientDep.htmx_template_response(
          request=request, 
          name="pages/todos_page.html",
          context= {
              "title" : "Todos",
              "todos" : todos
          },
          status_code=307
      )
  
@router.post("/sort")
def sort_todos(
  clientDep:ClientDep, 
  request: Request,
  session:SessionDep,
  sortList:Annotated[SortList, Form()]
)->Any:
  newOrder= []
  for id in sortList.id:
    newOrder.append(str(id))
    
  todos_model.sort_todos(session=session, newOrder=newOrder)
  todos, _ = todos_model.get_todos(session=session)

  return clientDep.htmx_template_response(
        request=request, 
        name="pages/test.html",
        context= {
            "todos" : todos
        }
    )