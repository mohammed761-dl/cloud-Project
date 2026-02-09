from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

# --- 2. ADD THIS EXACT BLOCK ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... rest of your code (models, db, endpoints)

# Notre modèle de données
class User(BaseModel):
    id: UUID | None = None
    username: str
    email: EmailStr
    is_active: bool = True

# --- STEP 2: DATABASE LOGIC ---
# If you have Azure SQL set up, we would use SQLAlchemy here.
# For now, we use the memory list, but CORS will make the light turn GREEN.
db: List[User] = []

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "User Management API",
        "database": "Memory (Pending Azure SQL Connection)"
    }

@app.post("/users/", status_code=201)
def create_user(user: User):
    user.id = uuid4()
    db.append(user)
    return user

@app.get("/users/", response_model=List[User])
def list_users():
    return db

@app.get("/users/{user_id}")
def get_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

@app.delete("/users/{user_id}")
def delete_user(user_id: UUID):
    for index, user in enumerate(db):
        if user.id == user_id:
            db.pop(index)
            return {"message": "Utilisateur supprimé"}
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, updated_data: User):
    for index, user in enumerate(db):
        if user.id == user_id:
            updated_data.id = user_id 
            db[index] = updated_data
            return updated_data
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")