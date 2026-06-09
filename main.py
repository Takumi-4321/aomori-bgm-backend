from fastapi import FastAPI

# FastAPIのインスタンス（本体）を作成
app = FastAPI()

# ルートURL（ / ）にGETリクエストが来たら、以下の関数を実行する
@app.get("/")
def read_root():
    return {"message": "Hello World from Aomori BGM!"}