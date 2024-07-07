# app/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema
from starlette.responses import JSONResponse

from .models import User, UpdateUser, EmailSchema
from typing import List
from .email_utils import send_invitation_email

app = FastAPI()

# Assuming a simple in-memory store for demonstration. Replace with actual database operations.
users_db = {}

@app.post("/add_users", response_model=User)
async def create_user(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[user.email] = user
    return user

@app.get("/get_users/{email}", response_model=User)
async def get_user(email: str):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[email]

@app.patch("/update_users/{email}", response_model=User)
async def update_user(email: str, user_update: UpdateUser):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    stored_user_data = users_db[email]
    updated_user = stored_user_data.copy(update=user_update.dict(exclude_unset=True))
    users_db[email] = updated_user
    return updated_user

@app.delete("/delete_users/{email}", response_model=dict)
async def delete_user(email: str):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[email]
    return {"ok": True}


@app.post("/send_invite")
async def send_invite(email: EmailSchema):
    try:
        await send_invitation_email(email.dict().get("email"))
        return {"message": "Invitation email has been sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while sending the email")



