from datetime import datetime, timedelta
from jose import jwt  
from passlib.context import CryptContext
from config import settings  # 👈 新しく作ったconfigから設定を読み込む！

# 🔒 パスワードのハッシュ化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 1. パスワードハッシュ化
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# 2. パスワード検証
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 🎫 デジタル会員証（JWT アクセストークン）を発行する関数
def create_access_token(data: dict):
    to_encode = data.copy()
    
    # 💡 有効期限を config.py（.env）の設定値から動的に取得！
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # 💡 SECRET_KEY と ALGORITHM も config.py から安全に取得！
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt