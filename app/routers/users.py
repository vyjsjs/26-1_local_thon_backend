from fastapi import APIRouter, Depends
from supabase import Client

from app.database import get_supabase
from app.schemas import UserRegisterRequest, UserRegisterResponse

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=UserRegisterResponse)
def register_user(
    body: UserRegisterRequest,
    supabase: Client = Depends(get_supabase),
):
    # user_id 가 PK 이므로 upsert 는 멱등 (이미 있으면 그대로 둠)
    supabase.table("users").upsert({"user_id": body.user_id}).execute()
    return UserRegisterResponse(success=True, user_id=body.user_id)
