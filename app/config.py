import os

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# CORS 허용 출처. 배포 후 Vercel URL 은 FRONTEND_ORIGIN 환경변수로 추가.
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Next.js 로컬 개발
    "http://localhost:5173",  # Vite 로컬 개발 (레거시)
]

_frontend_origin = os.environ.get("FRONTEND_ORIGIN")
if _frontend_origin:
    ALLOWED_ORIGINS.append(_frontend_origin)
