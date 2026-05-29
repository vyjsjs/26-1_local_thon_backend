from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from app.routers import stamps, users

app = FastAPI(title="수원 공방거리 스탬프 투어 API")

# CORS 미들웨어 (허용 출처는 app/config.py 에서 관리)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 연결 테스트용 (기존)
@app.get("/api/test")
def test_api():
    return {"message": "백엔드와 성공적으로 연결되었습니다!"}


# 라우터 등록
app.include_router(users.router)
app.include_router(stamps.router)
