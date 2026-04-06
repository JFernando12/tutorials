from fastapi import APIRouter, HTTPException

from app.database import SessionDep
from app.models import NoteCreate, NotePublic
from app.services import note_service

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NotePublic, status_code=201)
def create_note(payload: NoteCreate, session: SessionDep):
    return note_service.create_note(payload, session)


@router.get("", response_model=list[NotePublic])
def list_notes(session: SessionDep):
    return note_service.list_notes(session)


@router.get("/{note_id}", response_model=NotePublic)
def get_note(note_id: int, session: SessionDep):
    note = note_service.get_note(note_id, session)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
