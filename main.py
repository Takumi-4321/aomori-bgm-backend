from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import security # 👈 暗号化ファイル
from database import engine, get_db

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

# 📥 BGM登録（ACID特性・トランザクション設計版！）
@app.post("/bgms", response_model=schemas.BGMResponse, status_code=status.HTTP_201_CREATED)
def create_bgm(bgm: schemas.BGMCreate, db: Session = Depends(get_db)):
    
    # 💡 ここから厳密なトランザクションを開始（一蓮托生のスタート）
    with db.begin():
        try:
            # 1. BGMデータを生成して仮追加（ステージング）
            db_bgm = models.BGMModel(**bgm.model_dump(mode="json"), owner_id=1)
            db.add(db_bgm)
            
            # 💡 一度データベースに仮反映して、自動生成される「BGMのID」を取得
            db.flush() 

            # 2. 同時に「ログテーブル」にも操作履歴を生成して仮追加
            db_log = models.BGMLogModel(
                bgm_id=db_bgm.id,
                action="CREATE"
            )
            db.add(db_log)
            
            # 💡 withブロックを正常に抜ければ、自動で一括コミットされ両方同時に確定します！
            
        except Exception as e:
            # 💡 どちらか片方でもエラーが起きたら自動でロールバックされ、すべて白紙に戻します！
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"データベースエラーにより処理を巻き戻しました: {str(e)}"
            )

    # 確定したデータをリフレッシュしてクライアントに返却
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