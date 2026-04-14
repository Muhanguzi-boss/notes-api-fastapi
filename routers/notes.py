from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import date
from schemas.note import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter()

notes = []
current_id = 1

#create
@router.post("/notes", response_model=NoteResponse, status_code=201)
def create_note(note: NoteCreate):
    global current_id

    new_note = {
        "id": current_id,
        "title": note.title,
        "content": note.content,
        "created_at": date.today()
    }

    notes.append(new_note)
    current_id += 1
    return new_note

#get all
@router.get("/notes", response_model=List[NoteResponse])
def get_notes(limit: int = Query(10), title: str = Query(None)):
    result = notes

    if title:
        result = [n for n in notes if title.lower() in n["title"].lower()]

    return result[:limit]

# get one
@router.get("/notes/{id}", response_model=NoteResponse)
def get_note(id: int):
    for note in notes:
        if note["id"] == id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

# Update
@router.put("/notes/{id}", response_model=NoteResponse)
def update_note(id: int, updated_note: NoteUpdate):
    for note in notes:
        if note["id"] == id:
            if updated_note.title is not None:
                note["title"] = updated_note.title
            if updated_note.content is not None:
                note["content"] = updated_note.content
            return note

    raise HTTPException(status_code=404, detail="Note not found")

# Delete
@router.delete("/notes/{id}", status_code=204)
def delete_note(id: int):
    for i, note in enumerate(notes):
        if note["id"] == id:
            notes.pop(i)
            return

    raise HTTPException(status_code=404, detail="Note not found")