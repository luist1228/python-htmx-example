import uuid
from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
  title: str = Field(min_length=1, max_length=255)
  description: str | None = Field(default=None, max_length=255)
  done:bool = False
  
class TodoCreate(TodoBase):
  pass

class Todo(TodoBase, table=True):
  id:uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  title: str = Field(index=True, max_length=255)

class TodoPublic(TodoBase):
  id:uuid.UUID
  title: str
  description: str | None
  done:bool  
  
class TodosPublic(SQLModel):
  data: list[TodoPublic]
  count: int  