from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import schemas
from services import get_users, get_user
from dependencies import get_db, get_current_active_user
from models import User

from gensim.models import Word2Vec
from gensim.models import KeyedVectors

loaded_model = KeyedVectors.load_word2vec_format("wtov/eng_w2v") # 모델 로드


router = APIRouter()


@router.post("/word", name = '연관 단어', tags=['연관 단어'],
            description='접근 토큰의 사용자 정보 반환')
async def read_users_me(item: schemas.Word):
    model_result = loaded_model.most_similar(item.word)
    ret = []
    for word, _ in model_result:
        ret.append(word)
    return ret