from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  # 👈 鍵マークを出すために追加！
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import security  # 👈 暗号化ファイル
from database import engine, get_db
from security import create_access_token

app = FastAPI(title="Aomori BGM API")

# 🔑 【新設】画面に「Authorize」ボタンと「鍵マーク」を出現させるための設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ==========================================
# 👤 ① ユーザー認証関連のAPI
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
# 🎵 ② BGM関連のAPI
# ==========================================

# 📥 BGM登録（ログインユーザーのIDを自動紐付けする版！）
@app.post("/bgms", response_model=schemas.BGMResponse, status_code=status.HTTP_201_CREATED)
def create_bgm(
    bgm: schemas.BGMCreate, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)  # 👈 鍵チェック門番
):
    # 👤 【新設】トークン（会員証）から、今ログインしているユーザーを特定する
    # ※ `create_access_token(data={"sub": user.email})` で作ったので、tokenの中にはemailが入っています
    current_user = db.query(models.User).filter(models.User.email == token).first()
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="有効なユーザーが見つかりません。"
        )

    # 💡 ここから厳密なトランザクションを開始
    with db.begin():
        try:
            # 1. BGMデータを生成して仮追加（owner_idにログイン中のユーザーIDを自動セット！）
            db_bgm = models.BGMModel(**bgm.model_dump(mode="json"), owner_id=current_user.id)
            db.add(db_bgm)
            
            # 💡 一度データベースに仮反映して、自動生成される「BGMのID」を取得
            db.flush() 

            # 2. 同時に「ログテーブル」にも操作履歴を生成して仮追加
            db_log = models.BGMLogModel(
                bgm_id=db_bgm.id,
                action="CREATE"
            )
            db.add(db_log)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"データベースエラーにより処理を巻き戻しました: {str(e)}"
            )

    # 確定したデータをリフレッシュしてクライアントに返却
    db.refresh(db_bgm)
    return db_bgm

# 📤 BGM全件取得
@app.get("/bgms", response_model=List[schemas.BGMResponse])
def read_bgms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.BGMModel).offset(skip).limit(limit).all()

# 🔄 BGM更新
@app.put("/bgms/{bgm_id}", response_model=schemas.BGMResponse)
def update_bgm(bgm_id: int, updated_bgm: schemas.BGMCreate, db: Session = Depends(get_db)):
    db_bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    if db_bgm is None:
        raise HTTPException(status_code=404, detail="指定されたBGMが見つかりません")
    
    for key, value in updated_bgm.model_dump(mode="json").items():
        setattr(db_bgm, key, value)
       
    db.commit()
    db.refresh(db_bgm)
    return db_bgm

# 🗑️ BGM削除
@app.delete("/bgms/{bgm_id}")
def delete_bgm(bgm_id: int, db: Session = Depends(get_db)):
    db_bgm = db.query(models.BGMModel).filter(models.BGMModel.id == bgm_id).first()
    if db_bgm is None:
        raise HTTPException(status_code=404, detail="指定されたBGMが見つかりません")
    
    db.delete(db_bgm)
    db.commit()
    return {"message": f"ID {bgm_id} のBGMを削除しました"}


# ==========================================
# 🎫 ③ ログイン認証関連のAPI
# ==========================================

@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 1. データベースからユーザーをメールアドレスで探す
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # 2. ユーザーが存在しない、またはパスワードが間違っていたらエラー
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスかパスワードが間違っています",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. 検証OKなら、本物の会員証（JWTアクセストークン）を発行！
    access_token = create_access_token(data={"sub": user.email})
    
    # 4. フロントエンド（ブラウザ）に鍵を返す
    return {"access_token": access_token, "token_type": "bearer"}