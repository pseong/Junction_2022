from datetime import timedelta

from fastapi import Depends, HTTPException, Request, status, APIRouter
from sqlalchemy.orm import Session

import schemas
from dependencies import get_db
from services import user_get_or_create, create_access_token
from SETTING import ACCESS_TOKEN_EXPIRE_MINUTES

import requests

router = APIRouter()

@router.post("/google", name = '구글 로그인', tags=['로그인'],
            description='API 인증을 위한 접근 토큰 반환<br>인증이 필요한 API 호출 시<br>'
                        '헤더에 Authorization 에다가 토큰 전송<br>'
                        '헤더에 "Authorization: Bearer 접근토큰" 형식으로 다른 API 호출 시 인증',
            response_description='access_token: 접근 토큰<br>'
                                 'state: 유효한 계정 정보', response_model=schemas.Token)
def login_for_access_token(request: Request, db: Session = Depends(get_db)):
    if "Authorization" in request.headers:
        token = request.headers["Authorization"]
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not found Authorization in header")
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="failed to asign")

    user_json = response.json()
    item = schemas.UserCreate
    item.sub = user_json['sub']
    item.email = user_json['email']
    item.name = user_json['name']

    user = user_get_or_create(db, item)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/test", name = '테스트 로그인', tags=['로그인'],
            description='직접 sub, emali, name을 전송해주면 접근 토큰 반환',
            response_description='access_token: 접근 토큰<br>'
                                 'state: 유효한 계정 정보', response_model=schemas.Token)
def login_for_access_token_test(item: schemas.UserCreate, db: Session = Depends(get_db)):

    user = user_get_or_create(db, item)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}