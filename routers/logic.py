from typing import List

from fastapi import Depends, HTTPException, APIRouter, WebSocket
from sqlalchemy.orm import Session

import schemas

from gensim.models import KeyedVectors

loaded_model = KeyedVectors.load_word2vec_format("wtov/eng_w2v") # 모델 로드


router = APIRouter()


@router.post("/word", name = '연관 단어', tags=['연관 단어'],
            description='한 단어의 유사한 단어를 반환')
async def read_users_me(item: schemas.Word):
    try:
        model_result = loaded_model.most_similar(item.word)
    except:
        return []
    ret = []
    for word, _ in model_result:
        ret.append(word)
    return ret