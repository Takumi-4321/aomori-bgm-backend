from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

import models
from database import engine, get_db

# データベースのテーブルを自動生成
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aomori BGM API",
    description="データを登録・取得できる、完全な青森BGM API",
    version="1.2.0"
)

# ==========================================
# 1. スキーマ（データ構造）の定義
# ==========================================

# データを新しく登録・更新する時に、フロントエンドから受け取る形
class BGMCreate(BaseModel):
    title: str
    description: str
    location: str
    duration_seconds: int
    category: str

# データを画面に返す（出力する）時の形
class BGMResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    duration_seconds: int
    category: str

    class Config:
        orm_mode = True


# ==========================================
# 2. エンドポイント（API）の実装
# ==========================================

# ① BGM一覧取得API
@app.get("/bgms", response_model=List[BGMResponse], status_code=status.HTTP_200_OK)
def get_all_bgms(db: Session = Depends(get_db)):
    bgms = db.query(models.BGMModel).all()
    return bgms


# ② BGMデータ登録API
@app.post(
    "/bgms", 
    response_model=BGMResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="新しいBGMデータの登録",
    description="青森の新しいBGM情報をデータベースに永続化（保存）します。"
)
def create_bgm(bgm_data: BGMCreate, db: Session = Depends(get_db)):
    new_bgm = models.BGMModel(
        title=bgm_data.title,
        description=bgm_data.description,
        location=bgm_data.location,
        duration_seconds=bgm_data.duration_seconds,
        category=bgm_data.category
    )
    db.add(new_bgm)
    db.commit()
    db.refresh(new_bgm)
    return new_bgm


# ③ BGM詳細取得API
@app.get("/bgms/{bgm_id}", response_model=BGMResponse, status_code=status.HTTP_200_OK)
def get_bgm_by_id(bgm_id: int, db: Session = Depends(get_db)):
    bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    if bgm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"BGM ID {bgm_id} はデータベースに存在しません。"
        )
    return bgm


# ④ BGM更新API（PUT）
@app.put("/bgm/{bgm_id}", response_model=BGMResponse)
def update_bgm(bgm_id: int, updated_bgm: BGMCreate, db: Session = Depends(get_db)):
    db_bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    if db_bgm is None:
        raise HTTPException(status_code=404, detail="BGM not found")
    
    db_bgm.title = updated_bgm.title
    db_bgm.description = updated_bgm.description
    db_bgm.location = updated_bgm.location
    db_bgm.duration_seconds = updated_bgm.duration_seconds
    db_bgm.category = updated_bgm.category
    
    db.commit()
    db.refresh(db_bgm)
    return db_bgm


# ⑤ BGM削除API（DELETE）
@app.delete("/bgm/{bgm_id}")
def delete_bgm(bgm_id: int, db: Session = Depends(get_db)):
    db_bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    if db_bgm is None:
        raise HTTPException(status_code=404, detail="BGM not found")
    
    db.delete(db_bgm)
    db.commit()
    return {"message": f"BGM with id {bgm_id} has been deleted successfully."}
