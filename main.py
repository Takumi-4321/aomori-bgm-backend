from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import security # 👈 暗号化ファイル
from database import engine, get_db

# データベースのテーブルを自動作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aomori BGM API")


# ==========================================
# 👤 ① ユーザー認証関連のAPI（新設！）
# ==========================================

@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. すでに同じメールアドレスが登録されていないかチェック
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="このメールアドレスは既に登録されています。"
        )
    
    # 2. パスワードをハッシュ化（暗号化）
    hashed_pass = security.get_password_hash(user.password)
    
    # 3. データベースに保存
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pass
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ==========================================
# 🎵 ② BGM関連のAPI（あなたのコードをベースに強化！）
# ==========================================

# 📥 BGM登録（仮のowner_id=1をセットするように強化）
@app.post("/bgms", response_model=schemas.BGMResponse, status_code=status.HTTP_201_CREATED)
def create_bgm(bgm: schemas.BGMCreate, db: Session = Depends(get_db)):
    # mode="json" を追加するだけで、URL型が安全な文字列に変換されます！
    db_bgm = models.BGMModel(**bgm.model_dump(mode="json"), owner_id=1)
    db.add(db_bgm)
    db.commit()
    db.refresh(db_bgm)
    return db_bgm

# 📤 BGM全件取得（そのままキープ！）
@app.get("/bgms", response_model=List[schemas.BGMResponse])
def read_bgms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.BGMModel).offset(skip).limit(limit).all()

# 🔄 BGM更新（そのままキープ！）
@app.put("/bgms/{bgm_id}", response_model=schemas.BGMResponse)
def update_bgm(bgm_id: int, updated_bgm: schemas.BGMCreate, db: Session = Depends(get_db)):
    db_bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    if db_bgm is None:
        raise HTTPException(status_code=404, detail="指定されたBGMが見つかりません")
    
    # mode="json" を追加することで、URLをPostgreSQLが喜ぶ普通の文字列に変換して上書きします！
    for key, value in updated_bgm.model_dump(mode="json").items():
        setattr(db_bgm, key, value)
       
    db.commit()
    db.refresh(db_bgm)
    return db_bgm

# 🗑️ BGM削除（そのままキープ！）
@app.delete("/bgms/{bgm_id}")
def delete_bgm(bgm_id: int, db: Session = Depends(get_db)):
    db_bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    if db_bgm is None:
        raise HTTPException(status_code=404, detail="指定されたBGMが見つかりません")
    
    db.delete(db_bgm)
    db.commit()
    return {"message": f"ID {bgm_id} のBGMを削除しました"}