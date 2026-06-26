from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# 👤 ① ユーザー情報のテーブル
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 BGMテーブルとの繋がり
    bgms = relationship("BGMModel", back_populates="owner")


# 🎵 ② BGM情報のテーブル
class BGMModel(Base):
    __tablename__ = "bgms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True) 
    artist = Column(String, nullable=True)             
    youtube_url = Column(String, nullable=False)       
    description = Column(String, nullable=True)        
    location = Column(String, nullable=True)           
    duration_seconds = Column(Integer, nullable=True)  
    category = Column(String, nullable=True)           
    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 誰が投稿したBGMなのかを紐付けるための鍵（外部キー）
    owner_id = Column(Integer, ForeignKey("users.id"))
    # 🔗 ユーザーテーブルとの繋がり
    owner = relationship("User", back_populates="bgms")


# 📜 ③ BGMの操作履歴を記録するテーブル（トランザクション検証用！）
class BGMLogModel(Base):
    __tablename__ = "bgm_logs"

    id = Column(Integer, primary_key=True, index=True)
    bgm_id = Column(Integer, nullable=True)               # 操作されたBGMのID
    action = Column(String, nullable=False)                # "CREATE", "UPDATE", "DELETE"
    created_at = Column(DateTime, default=datetime.utcnow) # 操作された日時