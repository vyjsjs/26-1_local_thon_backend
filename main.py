from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. 허락할 프론트엔드 주소 목록 (나중에 Vercel 주소를 여기에 추가합니다)
origins = [
    "http://localhost:3000",  # Next.js 로컬 개발
    "http://localhost:5173",  # Vite 로컬 개발 (레거시)
]

# 2. CORS 미들웨어 추가 (보안 통과 설정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # GET, POST 등 모든 방식 허용
    allow_headers=["*"], # 모든 헤더 허용
)

# 3. 테스트용 API 만들기
@app.get("/api/test")
def test_api():
    return {"message": "백엔드와 성공적으로 연결되었습니다!"}