from collections.abc import Sequence
from sqlmodel import Session, select
from app.models import Note, NoteCreate

def create_note(payload: NoteCreate, session: Session) -> Note:
    note = Note.model_validate(payload)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

def list_notes(session: Session) -> Sequence[Note]:
    return session.exec(select(Note)).all()

def get_note(note_id: int, session: Session) -> Note | None:
    return session.get(Note, note_id)
