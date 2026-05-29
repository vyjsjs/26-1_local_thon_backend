FROM python:3.12-slim

WORKDIR /app

# 의존성 먼저 설치 (레이어 캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 소스 복사
COPY . .

EXPOSE 8000

# 환경변수(SUPABASE_URL, SUPABASE_KEY)는 런타임에 주입:
#   docker run --env-file .env -p 8000:8000 <image>
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
