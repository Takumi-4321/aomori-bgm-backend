from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. データベースの保存先を指定（同じフォルダ内に「aomori_bgm.db」というファイルができる）
SQLALCHEMY_DATABASE_URL = "sqlite:///./aomori_bgm.db"

# 2. データベースを操作する「エンジン」を作成
engine = create_engine(
    # SQLite限定の設定：複数のスレッドからアクセスできるようにする
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. データベースとやり取りをする「セッション（窓口）」の工場を作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 後でテーブルの形（モデル）を作る時に使うベースクラス
Base = declarative_base()

# 5. APIが実行される時に、DB接続を開いて、終わったら自動で閉じるための便利な仕組み
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()