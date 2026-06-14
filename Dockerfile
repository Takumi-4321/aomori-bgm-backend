# 1. ベースとなるPythonの軽量イメージを指定
FROM python:3.11-slim

# 2. コンテナ内の作業ディレクトリを設定
WORKDIR /app

# 3. 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 4. 依存関係の定義ファイルを先にコピー
COPY requirements.txt .

# 5. ライブラリのインストール
RUN pip install --no-cache-dir -r requirements.txt

# 6. ローカルのソースコードをすべてコンテナ内にコピー
COPY . .

# 7. 【実務仕様】セキュリティ対策として一般ユーザーを作成して切り替え
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 8. FastAPIを起動するコマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]