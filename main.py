from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Aomori BGM API",
    description="青森の情景を音で届けるバックエンドサービス",
    version="1.0.0"
)

# ==========================================
# 1. スキーマ（データ構造）の定義
# ==========================================
class BGMResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    duration_seconds: int
    category: str  # 例: "festival", "nature", "traditional"

# ==========================================
# 2. 模擬データ（データベースの代わり）
# ==========================================
MOCK_BGM_DATABASE = [
    {
        "id": 1,
        "title": "青森ねぶた祭り - 運行の熱気",
        "description": "じゃわめぐ（ぞくぞくする）大迫力の囃子と跳人の声。",
        "location": "青森市",
        "duration_seconds": 180,
        "category": "festival"
    },
    {
        "id": 2,
        "title": "奥入瀬渓流 - 清流のせせらぎ",
        "description": "新緑の奥入瀬、阿修羅の流れ周辺で録音した天然のホワイトノイズ。",
        "location": "十和田市",
        "duration_seconds": 300,
        "category": "nature"
    },
    {
        "id": 3,
        "title": "津軽三味線 - 即興の響き",
        "description": "叩き奏法による、力強くも哀愁を帯びた伝統の音色。",
        "location": "弘前市",
        "duration_seconds": 240,
        "category": "traditional"
    }
]

# ==========================================
# 3. エンドポイント（APIのURL）の実装
# ==========================================

# ① BGM一覧取得API
@app.get(
    "/bgms", 
    response_model=List[BGMResponse], 
    status_code=status.HTTP_200_OK,
    summary="BGM一覧の取得",
    description="登録されているすべての青森のBGMデータを返します。"
)
def get_all_bgms():
    return MOCK_BGM_DATABASE


# ② BGM詳細取得API
@app.get(
    "/bgms/{bgm_id}", 
    response_model=BGMResponse, 
    status_code=status.HTTP_200_OK,
    summary="BGM詳細の取得",
    description="指定されたIDのBGM詳細データを返します。存在しない場合は404を返します。"
)
def get_bgm_by_id(bgm_id: int):
    # データベース（リスト）から該当するIDを探索
    for bgm in MOCK_BGM_DATABASE:
        if bgm["id"] == bgm_id:
            return bgm
    
    # 見つからなかった場合は、適切なHTTPステータスコード（404）を返却
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"BGM ID {bgm_id} は見つかりませんでした。"
    )