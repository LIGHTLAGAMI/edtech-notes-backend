from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define a Note model
class Note(BaseModel):
    id: int
    title: str
    content: str

# In-memory database (just for demo)
notes_db: List[Note] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Notes API!"}

@app.post("/notes/")
def create_note(note: Note):
    for n in notes_db:
        if n.id == note.id:
            raise HTTPException(status_code=400, detail="Note with this ID already exists.")
    notes_db.append(note)
    return {"message": "Note created successfully", "note": note}

@app.get("/notes/", response_model=List[Note])
def get_notes():
    return notes_db

@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    for note in notes_db:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found.")

@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Note):
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db[i] = updated_note
            return {"message": "Note updated successfully", "note": updated_note}
    raise HTTPException(status_code=404, detail="Note not found.")

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for note in notes_db:
        if note.id == note_id:
            notes_db.remove(note)
            return {"message": "Note deleted successfully"}
    raise HTTPException(status_code=404, detail="Note not found.")
