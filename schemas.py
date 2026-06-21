from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List
from datetime import datetime

# ==========================================
# 👤 ユーザー認証関連のスキーマ（新設！）
# ==========================================

# 👤 1. アカウントを作るとき（ユーザー登録）に画面から受け取る形
class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50, description="ユーザー名（2文字以上）")
    # EmailStrを使うことで、門番が「正しいメールのアドレス形式か」を自動チェックしてくれる！
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=6, description="パスワード（6文字以上）")

# 👤 2. 画面に「登録できたよ」とユーザー情報を返してあげるときの形
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# 🎵 BGM関連のスキーマ（ログイン機能と連動！）
# ==========================================

# 🎵 3. BGMを新しく登録するときの形
class BGMCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="BGMのタイトル")
    artist: Optional[str] = Field(None, min_length=1, max_length=100, description="アーティスト名")
    youtube_url: HttpUrl = Field(..., description="YouTubeの音源URL(https://...)")
    description: Optional[str] = None
    location: Optional[str] = None
    duration_seconds: Optional[int] = None
    category: Optional[str] = None

# 🎵 4. 画面にBGMデータを返してあげるときの形（誰が投稿したかも一緒に返すように強化！）
class BGMResponse(BGMCreate):
    id: int
    created_at: datetime
    owner_id: int # 👈「この曲はどのユーザーが作ったか」のIDを含める

    class Config:
        from_attributes = True