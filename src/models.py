from typing import Dict, List
import uuid
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, JSON, Column

from sqlalchemy.ext.mutable import MutableDict

class TodoBase(SQLModel):
  title:str = Field(min_length=1, max_length=255)
  description: str | None = Field(default=None)
  done:bool = False
  
class TodoCreate(TodoBase):
  pass

class Todo(TodoBase, table=True):
  id:uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class TodoUpdate(TodoBase):
  title:str = Field(min_length=1, max_length=255)
  description: str | None = Field(default=None)
  done:bool
  

class TodoPublic(TodoBase):
  id:uuid.UUID
  description: str | None
  done:bool  
  
class TodosPublic(SQLModel):
  data: list[TodoPublic]
  count: int  
  
class Message(SQLModel):
  message: str
  
  
class SortList(BaseModel):
  id: List[uuid.UUID]
  
  
class TodosPosition(SQLModel, table=True):
  id:str = Field(primary_key=True)
  data: Dict = Field(default = {"order":[]} , sa_column=Column(MutableDict.as_mutable(JSON)))

  

from sqlalchemy.ext.mutable import MutableDict