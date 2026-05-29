from functools import lru_cache

from supabase import Client, create_client

from app.config import SUPABASE_KEY, SUPABASE_URL


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    """Supabase 클라이언트 싱글톤. 첫 요청 시 생성(지연 초기화)."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL / SUPABASE_KEY 환경변수가 설정되지 않았습니다. .env 를 확인하세요."
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)
