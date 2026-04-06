from sqlmodel import Field, SQLModel

class NoteBase(SQLModel):
    title: str
    content: str | None = None

class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class NoteCreate(NoteBase):
    pass

class NotePublic(NoteBase):
    id: int
