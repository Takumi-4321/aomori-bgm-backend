import os
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# 🔒 パスバー設定（すでに書いてあるもの）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 【新】 .envファイルから安全に秘密鍵と設定を読み込む
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")

# 1. パスワードハッシュ化（すでに書いてあるもの）
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 2. パスワード検証（すでに書いてあるもの）
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 🎫 【新】 デジタル会員証（JWT アクセストークン）を発行する関数
def create_access_token(data: dict):
    to_encode = data.copy()
    
    # 有効期限を30分に設定
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    # .envから読み込んだSECRET_KEYで暗号化署名する
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt