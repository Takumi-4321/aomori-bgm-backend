# 1. ベースとなるPythonの軽量イメージを指定
FROM python:3.11-slim

# 2. コンテナ内の作業ディレクトリを設定
WORKDIR /app

# 3. 環境変数の設定（Pythonがpycファイルを作成するのを防ぎ、ログをリアルタイムで出力する）
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. 依存関係の定義ファイルを先にコピー（キャッシュを利かせてビルドを高速化するため）
COPY requirements.txt .

# 5. ライブラリのインストール
RUN pip install --no-cache-dir -r requirements.txt

# 6. ローカルのソースコードをすべてコンテナ内にコピー
COPY . .

# 7. FastAPIを起動するコマンド（コンテナ起動時に実行される）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]