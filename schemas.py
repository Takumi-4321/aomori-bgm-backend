from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

# 🎵 データを登録するときに必要な項目（入力の形 ＋ 強力な門番付き！）
class BGMCreate(BaseModel):
    # タイトルは最低1文字、最大100文字まで（空っぽを許さない）
    title: str = Field(..., min_length=1, max_length=100, description="BGMのタイトル")
    
    # アーティスト名は省略可能だけど、もし書くなら1文字以上
    artist: Optional[str] = Field(None, min_length=1, max_length=100, description="アーティスト名")
    
    # 以前のstring形式から、本物のURL形式（https://...）しか受け付けないように強化！
    youtube_url: HttpUrl = Field(..., description="YouTubeの音源URL(https://...)")
    
    # その他の項目は以前の使いやすさをそのままキープ
    description: Optional[str] = None
    location: Optional[str] = None
    duration_seconds: Optional[int] = None
    category: Optional[str] = None

# 🎵 画面にデータを返してあげるときの形（IDや登録日時も含む出力の形）
class BGMResponse(BGMCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemyのデータをPydanticに自動変換する設定