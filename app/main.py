from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from typing import List
import os
from dotenv import load_dotenv

from .models import User as UserModel, UpdateUser, UserCreate, UserRead, EmailSchema
from .email_utils import send_invitation_email

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

app = FastAPI()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.post("/add_users", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(UserModel).where(UserModel.email == user.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = UserModel(**user.dict())
        db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserRead.from_orm(new_user)

@app.get("/get_users/{email}", response_model=UserRead)
async def get_user(email: str, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(UserModel).where(UserModel.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.from_orm(user)

@app.patch("/update_users/{email}", response_model=UserRead)
async def update_user(email: str, user_update: UpdateUser, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(UserModel).where(UserModel.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
    return UserRead.from_orm(user)

@app.delete("/delete_users/{email}", response_model=dict)
async def delete_user(email: str, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(UserModel).where(UserModel.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await db.delete(user)
        await db.commit()
    return {"ok": True}

@app.post("/send_invite")
async def send_invite(email: EmailSchema):
    try:
        await send_invitation_email(email.dict().get("email"))
        return {"message": "Invitation email has been sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred while sending the email: {e}")
