# FastAPI Notes CRUD API

A simple RESTful CRUD API built with **FastAPI** and **SQLModel** that allows users to create, read, update, and delete notes.

## Tech Stack
- Python
- FastAPI
- SQLModel
- SQLite

## Features
- Create notes with title and content
- Retrieve all notes or filter by completion status
- Update notes (partial updates supported)
- Delete notes
- Automatic database creation on startup

## API Endpoints

| Method | Endpoint | Description |
|------|--------|-------------|
| POST | /notes | Create a new note |
| GET | /notes | List all notes |
| GET | /notes/{id} | Get a specific note |
| PATCH | /notes/{id} | Update a note |
| DELETE | /notes/{id} | Delete a note |

## Setup & Run

```bash
git clone https://github.com/yourusername/fastapi-notes-crud.git
cd fastapi-notes-crud
pip install -r requirements.txt
uvicorn main:app --reload
```
API will be available at http://127.0.0.1:8000/docs after running it in the terminal
