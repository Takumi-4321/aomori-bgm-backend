from sqlalchemy import Column, Integer, String
from database import Base

# データベース上の「bgms」というテーブルの構造を定義
class BGMModel(Base):
    __tablename__ = "bgms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    location = Column(String)
    duration_seconds = Column(Integer)
    category = Column(String)