from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from typing import List

app = FastAPI()

# Notre modèle de données
class User(BaseModel):
    id: UUID | None = None
    username: str
    email: EmailStr
    is_active: bool = True

# Simulation de base de données (en mémoire)
db: List[User] = []


@app.get("/")
def root():
    return {
        "message": "User Management API",
        "endpoints": {
            "docs": "/docs",
            "create_user": "POST /users/",
            "list_users": "GET /users/",
            "get_user": "GET /users/{user_id}",
            "update_user": "PUT /users/{user_id}",
            "delete_user": "DELETE /users/{user_id}"
        }
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
            # On garde l'ID original mais on met à jour le reste
            updated_data.id = user_id 
            db[index] = updated_data
            return updated_data
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")