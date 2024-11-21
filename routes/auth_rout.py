import uuid

import bcrypt
import jwt
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from middleware.auth_middleware import getdata
from models.user_model import User
from pydantic_schema.create_user import CreateUser
from pydantic_schema.loged_user import Logeduser

router=APIRouter()
@router.post("/signup",status_code=201)
def signup(user:CreateUser,db: Session=Depends(get_db)):
    user_db= db.query(User).filter(User.email==user.email).first()
    if user_db:
        raise HTTPException(status_code=400,
            detail={"error": "User already exists", "field": "email"})
    hashed_pw=bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    new_user = User(id=str(uuid.uuid4()), email=user.email, password=hashed_pw, name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user": {"name": new_user.name, "email": new_user.email}}

# Create tables in the database

@router.post("/login")
    
def login(user: Logeduser, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(status_code=400, detail={"error": "user doesn't exist"})
    
    is_password = bcrypt.checkpw(user.password.encode(), user_db.password)
    if not is_password:
        raise HTTPException(status_code=400, detail="The password is incorrect")
    token=jwt.encode(payload={"id":user_db.id},key='password_key')
    return {"user":user_db,"token":token}

@router.get("/")
def get_user(db:Session=Depends(get_db),user_id=Depends(getdata)):
    user = db.query(User).filter(User.id == user_id['uid']).options(
 joinedload(User.favorite)
    ).first()

    if not user:
        raise HTTPException(404, 'User not found!')
    
    return user