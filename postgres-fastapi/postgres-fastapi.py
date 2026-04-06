# Step 1: Import dependencies
from contextlib import asynccontextmanager
from typing import Annotated
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

load_dotenv()

# Step 2: Configure database connection
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Step 3: Define the Note model and schemas
class NoteBase(SQLModel):
    title: str
    content: str | None = None

class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class NoteCreate(NoteBase):
    pass

class NotePublic(NoteBase):
    id: int

# Step 4: Create the FastAPI app with lifespan (creates tables on startup)
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

# Step 5: POST /notes — create a note
@app.post("/notes", response_model=NotePublic, status_code=201)
def create_note(payload: NoteCreate, session: SessionDep):
    note = Note.model_validate(payload)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

# Step 6: GET /notes — list all notes
@app.get("/notes", response_model=list[NotePublic])
def list_notes(session: SessionDep):
    return session.exec(select(Note)).all()

# Step 7: GET /notes/{id} — get a single note
@app.get("/notes/{note_id}", response_model=NotePublic)
def get_note(note_id: int, session: SessionDep):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
