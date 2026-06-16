from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class BGMModel(Base):
    __tablename__ = "bgms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True) # 曲名
    artist = Column(String, nullable=True)             # ★追加：アーティスト名
    youtube_url = Column(String, nullable=False)       # ★追加：YouTubeのリンク（画面再生用）
    description = Column(String, nullable=True)        # 説明文
    location = Column(String, nullable=True)           # 青森のどこの場所か
    duration_seconds = Column(Integer, nullable=True)  # 曲の長さ
    category = Column(String, nullable=True)           # カテゴリ（ねぶた、自然音など）
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # ★追加：登録日時