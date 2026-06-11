from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

# 自分で作ったファイルから設定を読み込む
import models
from database import engine, get_db

# アプリ起動時に、上で定義したテーブルを実際のSQLiteに自動作成する
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aomori BGM API",
    description="SQLiteデータベースと連携した、本物の青森BGM API",
    version="1.1.0"
)

# Pydanticモデル（データの出口の形）
class BGMResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    duration_seconds: int
    category: str

    class Config:
        # SQLAlchemyのオブジェクト（辞書型じゃないデータ）も自動でPydanticに変換する魔法の設定
        orm_mode = True


# ① 【DB版】BGM一覧取得API
@app.get("/bgms", response_model=List[BGMResponse], status_code=status.HTTP_200_OK)
def get_all_bgms(db: Session = Depends(get_db)):
    # データベースからbgmsテーブルのデータを全件取得する（SQLが自動発行される）
    bgms = db.query(models.BGMModel).all()
    return bgms


# ② 【DB版】BGM詳細取得API
@app.get("/bgms/{bgm_id}", response_model=BGMResponse, status_code=status.HTTP_200_OK)
def get_bgm_by_id(bgm_id: int, db: Session = Depends(get_db)):
    # データベースから指定されたIDのデータを1件だけ探索
    bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    
    if bgm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"BGM ID {bgm_id} はデータベースに存在しません。"
        )
    return bgm