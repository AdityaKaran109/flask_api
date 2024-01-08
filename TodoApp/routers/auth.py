from fastapi import APIRouter
from pydantic import BaseModel
from datetime import timedelta, datetime
from typing import Annotated
from models import Users
from starlette import status
from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, Path
from passlib.context import CryptContext
from routers.admin import db_dependency
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

#FOR JWT
SECRET_KEY = "14a5d139cd73e782df211a83598db6c3fe24e15c74ef3e38be1f0f85f67a1c8e"
ALGORITHM = "HS256"

#FOR HASHING PASSWORD
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    role: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

#CREATE ACCESS TOKEN\
def create_access_token(username:str, user_id:int, expires_delta:timedelta):
    encode = {'sub':username, 'id':user_id}
    expires = datetime.utcnow()+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)


# All user
@router.get("/auth/user/", status_code=status.HTTP_200_OK)
def get_users(db: db_dependency):
    return db.query(Users).all()


# Add users
@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.hashed_password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()


# delete user
@router.delete("/auth/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: db_dependency, user_id: int = Path(gt=0)):
    user_model = db.query(Users).filter(user_id == Users.id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(Users).filter(user_id == Users.id).delete()
    db.commit()


# get user by id
@router.get("/auth/{user_id}", status_code=status.HTTP_200_OK)
def get_user(db: db_dependency, user_id: int = Path(gt=0)):
    user_model = db.query(Users).filter(Users.id == user_id).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=404, detail="User not found")


# update user
@router.put("/auth/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(db: db_dependency, user_request: CreateUserRequest, user_id: int = Path(gt=0)):
    user_model = db.query(Users).filter(user_id == Users.id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_model.username = user_request.username
    user_model.email = user_request.email
    user_model.first_name = user_request.first_name
    user_model.last_name = user_request.last_name
    user_model.hashed_password = user_request.hashed_password
    user_model.role = user_request.role
    user_model.is_active = user_request.is_active
    db.add(user_model)
    db.commit()


# auth the user
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        return {"Message":"Failed Auth"}
    token = create_access_token(user.username, user.id, timedelta(minutes=20))


    return {"access_token": token, "token_type": "bearer"}
