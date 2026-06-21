from passlib.context import CryptContext

# 🔒 パスワードを暗号化（ハッシュ化）するための設定（bcryptという強力なアルゴリズムを使用）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. ユーザーが入力した生のパスワードを、暗号化された文字に変える関数
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 2. ログイン時に、入力されたパスワードと、データベース内の暗号化パスワードが一致するか確かめる関数
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)