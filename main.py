from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select


# Build Models

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    is_done: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)


class NoteCreate(SQLModel):
    title: str
    content: str


class NotesUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_done: Optional[bool] = None


# Building API stuff

engine = create_engine('sqlite:///notes.db', echo=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown: Close engine (optional for cleanup)
    engine.dispose()


app = FastAPI(title="CRUD app", lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


# Building CRUD Routes

@app.post("/notes", response_model=Note)
def create_note(payload: NoteCreate, session: Session = Depends(get_session)):
    note = Note.model_validate(payload)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@app.get("/notes", response_model=List[Note])
def list_notes(is_done: Optional[bool] = None, session: Session = Depends(get_session)):
    note = select(Note)

    if is_done is not None:
        note = note.where(Note.is_done == is_done)

    note = note.order_by(Note.created_at.desc())
    return session.exec(note).all()


@app.get('/notes/{note_id}', response_model=Note)
def get_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found!")
    return note


@app.patch("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, payload: NotesUpdate, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found!")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(note, key, value)

    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found!")
    session.delete(note)
    session.commit()
    return {'ok': True}