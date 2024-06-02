import hashlib
from datetime import datetime, timedelta

from fastapi.security import HTTPBasicCredentials, HTTPBasic

import CRUD
from config import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Header, HTTPException
from schemas import UserSchema
from typing import List
import generate_users
import jwt

# , RequestUser, Request, Response

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_user_token(auth: str = Header(...)):
    print(f'auth: {auth}')
    print(f'auth: {auth}')
    print(f'auth: {auth}')
    print(f'auth: {auth}')
    print(f'auth: {auth}')
    print(f'auth: {auth}')
    print(f'auth: {auth}')
    print(f'auth: {auth}')
    print(f'test split: {auth.split(".")}')
    payload = jwt.decode(auth, "Well_Done", algorithms=["HS256"])
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=402, detail="Invalid authentication credentials")

    return user_id


@router.post("/add")
async def create_user(request: UserSchema, db: Session = Depends(get_db)):
    CRUD.add_new_user(db, user=request)

    return {
        "message": f"user {request.login} successfully added",
        "user": request,
        "status_code": "200"
    }


@router.get("/get_by_first_name")
async def get_user_by_first_name(request: str, db: Session = Depends(get_db)):
    _user = CRUD.get_user_by_first_name(db, first_name=request)

    return {
        "message": f"user '{_user.first_name}' found",
        "user": _user,
        "status_code": "200"
    }


@router.get("/get_by_second_name")
async def get_by_second_name(request: str, db: Session = Depends(get_db)):
    _user = CRUD.get_user_by_second_name(db, second_name=request)

    return {
        "message": f"user '{_user.second_name}' found",
        "user": _user,
        "status_code": "200"
    }


@router.get("/get_all")
async def get_all(start: int, end: int, db: Session = Depends(get_db)):
    _users = CRUD.get_user(db, skip=start, limit=end)

    return {
        "message": f"users found",
        "users": _users,
        "status_code": "200"
    }


@router.post("/post_random_users")
async def post_random_users(db: Session = Depends(get_db)):
    users = generate_users.generate_users()
    for i in users:
        CRUD.add_new_user(db, i)

    return {"message": f"100000 users generate"}


@router.get("/get_user_bu_id")
async def get_all(user_id: int, db: Session = Depends(get_db)):
    _user = CRUD.get_user_by_id(db, user_id)

    return _user


@router.patch("/update")
async def update_user(user_id: int, new_first_name: str, new_second_name: str,
                      new_password: str, new_login: str, db: Session = Depends(get_db), token_id = Depends(check_user_token)):
    if user_id != token_id:
        raise HTTPException(status_code=402, detail='Bad token')

    _user = CRUD.update_user(db, user_id=user_id, first_name=new_first_name, second_name=new_second_name,
                     password=new_password, login=new_login)
    return {
        "message": f"user {user_id} update",
        "users": _user,
        "status_code": "200"
    }


@router.delete("/delete")
async def delete_user(user_id: int, db: Session = Depends(get_db), token_id = Depends(check_user_token)):
    if user_id != token_id:
        raise HTTPException(status_code=402, detail='Bad token')

    _user = CRUD.remove_user(db, user_id=user_id)

    return {
        "message": f"user {user_id} removed",
        "status_code": "200"
    }


@router.post("/login")
async def login(creds: HTTPBasicCredentials=Depends(HTTPBasic()), db: Session = Depends(get_db)):
    _user = CRUD.get_user_by_login(db, creds.username)
    #raise HTTPException(status_code=402, detail='Bad token')

    if _user is None:
        raise HTTPException(status_code=401, detail="user not found")


    if _user.login != creds.username:
        raise HTTPException(status_code=401, detail="wrong login")
    print(_user.login)

    # print(f'going to use password to hash: {}')
    hash_password = hashlib.sha256(creds.password.encode()).hexdigest()
    print(hash_password)
    if hash_password != _user.password:
        raise HTTPException(status_code=401, detail="wrong password")

    exp_date = datetime.now() + timedelta(minutes=15)


    token_data = {"sub": _user.id, "exp": exp_date}
    token = jwt.encode(token_data, "Well_Done", algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

