from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db # さっき完璧に入っているのを確認した関数です！

app = FastAPI(title="Aomori BGM API")

# 📥 ① BGMデータを新しく登録するAPI (POST method)
@app.post("/bgms", response_model=schemas.BGMResponse)
def create_bgm(bgm: schemas.BGMCreate, db: Session = Depends(get_db)):
    # models.py の形に変換してDBに突っ込む準備
    db_bgm = models.BGMModel(**bgm.model_dump())
    db.add(db_bgm)      # データを追加
    db.commit()         # 変更を確定
    db.refresh(db_bgm)  # DB側の最新状態（自動生成されたIDなど）を反映
    return db_bgm

# 📤 ② 登録されたBGMデータの一覧を全件取得するAPI (GET method)
@app.get("/bgms", response_model=List[schemas.BGMResponse])
def read_bgms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bgms = db.query(models.BGMModel).offset(skip).limit(limit).all()
    return bgms