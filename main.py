from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aomori BGM API",
    description="データを登録・取得できる、完全な青森BGM API",
    version="1.2.0"
)

# ==========================================
# 1. スキーマ（データ構造）の定義
# ==========================================

# 【追加】データを新しく登録する時に、フロントエンドから受け取る形
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

# ① 【昨日作った】BGM一覧取得API
@app.get("/bgms", response_model=List[BGMResponse], status_code=status.HTTP_200_OK)
def get_all_bgms(db: Session = Depends(get_db)):
    bgms = db.query(models.BGMModel).all()
    return bgms


# ② 【新設！】BGMデータ登録API
@app.post(
    "/bgms", 
    response_model=BGMResponse, 
    status_code=status.HTTP_201_CREATED, # 201 Created を返すのがプロのルール
    summary="新しいBGMデータの登録",
    description="青森の新しいBGM情報をデータベースに永続化（保存）します。"
)
def create_bgm(bgm_data: BGMCreate, db: Session = Depends(get_db)):
    # フロントエンドから届いたデータを、データベース用のモデルに変換
    new_bgm = models.BGMModel(
        title=bgm_data.title,
        description=bgm_data.description,
        location=bgm_data.location,
        duration_seconds=bgm_data.duration_seconds,
        category=bgm_data.category
    )
    
    # データベースにデータを「追加」して「確定（コミット）」させる
    db.add(new_bgm)
    db.commit()
    
    # データベース側で自動で発番された「ID」などを確定させて読み込む
    db.refresh(new_bgm)
    
    # 登録されたばかりの最新データを返却する
    return new_bgm


# ③ 【昨日作った】BGM詳細取得API
@app.get("/bgms/{bgm_id}", response_model=BGMResponse, status_code=status.HTTP_200_OK)
def get_bgm_by_id(bgm_id: int, db: Session = Depends(get_db)):
    bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    if bgm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"BGM ID {bgm_id} はデータベースに存在しません。"
        )
    return bgm

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# ※既存の models, schemas, database のインポート文はそのまま残してください

app = FastAPI()

# --- 既存のPOSTやGETの処理がここにある想定です ---

@app.put("/bgm/{bgm_id}", response_model=schemas.BGM)
def update_bgm(bgm_id: int, updated_bgm: schemas.BGMCreate, db: Session = Depends(get_db)):
    
    # 【コメント入れ所①：指定されたIDのデータがDBに存在するか探す処理】
    db_bgm = db.query(models.BGM).filter(models.BGM.id == bgm_id).first()
    
    # 【コメント入れ所②：データが見つからなかった場合にエラー(404)を返す処理】
    if db_bgm is None:
        raise HTTPException(status_code=404, detail="BGM not found")
    
    # 【コメント入れ所③：既存のデータ（db_bgm）の各カラムを、受け取った新しいデータ（updated_bgm）で上書きする処理】
    db_bgm.title = updated_bgm.title
    db_bgm.description = updated_bgm.description
    # ※他にも音声ファイルのパスなどがあれば、ここに同様の上書き処理を追加します
    
    # 【コメント入れ所④：DBの変更内容を確定（コミット）させる処理】
    db.commit()
    
    # 【コメント入れ所⑤：確定した最新のデータをDBから再読み込みする処理】
    db.refresh(db_bgm)
    
    # 更新したデータをクライアントに返却
    return db_bgm

@app.delete("/bgm/{bgm_id}")
def delete_bgm(bgm_id: int, db: Session = Depends(get_db)):
    
    # 【コメント入れ所①：削除したいIDのデータが、本当にDBにあるか確認する処理】
    db_bgm = db.query(models.BGM).filter(models.BGM.id == bgm_id).first()
    
    # 【コメント入れ所②：データが存在しなかったら、更新時と同様に404エラーを出す処理】
    if db_bgm is None:
        raise HTTPException(status_code=404, detail="BGM not found")
    
    # 【コメント入れ所③：見つかったデータを、データベースのゴミ箱（削除対象）に入れる処理】
    db.delete(db_bgm)
    
    # 【コメント入れ所④：削除を確定させ、データベースから完全に消去する処理】
    db.commit()
    
    # 正常に消去されたことを示すメッセージを返却
    return {"message": f"BGM with id {bgm_id} has been deleted successfully."}