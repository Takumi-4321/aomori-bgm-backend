from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 🎵 データを登録するときに必要な項目（入力の形）
class BGMCreate(BaseModel):
    title: str
    artist: Optional[str] = None
    youtube_url: str
    description: Optional[str] = None
    location: Optional[str] = None
    duration_seconds: Optional[int] = None
    category: Optional[str] = None

# 🎵 画面にデータを返してあげるときの形（IDや登録日時も含む出力の形）
class BGMResponse(BGMCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # SQLAlchemyのデータをPydanticに自動変換する設定