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

# 🔄 ③ 特定のBGMデータを更新するAPI (PUT method)
@app.put("/bgms/{bgm_id}", response_model=schemas.BGMResponse)
def update_bgm(bgm_id: int, updated_bgm: schemas.BGMCreate, db: Session = Depends(get_db)):
    # 指定されたIDのデータがDBにあるか探す
    db_bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    if db_bgm is None:
        raise HTTPException(status_code=404, detail="指定されたBGMが見つかりません")
    
    # データを上書き
    for key, value in updated_bgm.model_dump().items():
        setattr(db_bgm, key, value)
        
    db.commit()
    db.refresh(db_bgm)
    return db_bgm

# 🗑️ ④ 特定のBGMデータを削除するAPI (DELETE method)
@app.delete("/bgms/{bgm_id}")
def delete_bgm(bgm_id: int, db: Session = Depends(get_db)):
    # 指定されたIDのデータがDBにあるか探す
    db_bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    if db_bgm is None:
        raise HTTPException(status_code=404, detail="指定されたBGMが見つかりません")
    
    db.delete(db_bgm) # 削除を実行
    db.commit()       # 確定
    return {"message": f"ID {bgm_id} のBGMを削除しました"}