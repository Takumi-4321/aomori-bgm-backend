from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base # 👈 あなたの環境に合わせて .database から database に修正しました！

# 👤 ① ユーザー情報のテーブル（新しく追加！）
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False) # メール重複はNG
    hashed_password = Column(String, nullable=False) # パスワードは暗号化して保存
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 BGMテーブルとの繋がり（1人のユーザーは複数のBGMを持てる）
    bgms = relationship("BGMModel", back_populates="owner")


# 🎵 ② BGM情報のテーブル（ログイン機能と合体させてパワーアップ！）
class BGMModel(Base): # 👈 あなたのクラス名「BGMModel」に合わせました！
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

    # 🔗 👈【超重要】誰が投稿したBGMなのかを紐付けるための鍵（外部キー）
    owner_id = Column(Integer, ForeignKey("users.id"))
    # 🔗 ユーザーテーブルとの繋がり（このBGMは特定のユーザーのもの）
    owner = relationship("User", back_populates="bgms")