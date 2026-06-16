import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# 環境変数からPostgreSQLの接続URLを取得。なければデフォルト値（Docker環境用）を使用
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://db_user:db_password@localhost:5432/aomori_bgm_db")

# PostgreSQL用のEngineを作成（SQLiteの時の 'check_same_thread' は不要になるため削除）
engine = create_engine(DATABASE_URL)

# 各APIリクエストごとにデータベースのセッション（接続インスタンス）を作るための設定
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# テーブルのモデルを作るためのベースクラス
Base = declarative_base()

# APIがデータベースを利用する際に呼び出す関数（依存性注入用）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # 処理が終わったら必ず接続を閉じてメモリを解放する（実務で超重要）