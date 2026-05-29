from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.database import get_supabase
from app.schemas import (
    StampCollectRequest,
    StampCollectResponse,
    StampItem,
    StampListResponse,
)
from app.shops import TOTAL_SHOPS, nfc_to_shop_id

router = APIRouter(prefix="/api/stamps", tags=["stamps"])


@router.post("/collect", response_model=StampCollectResponse)
def collect_stamp(
    body: StampCollectRequest,
    supabase: Client = Depends(get_supabase),
):
    shop_id = nfc_to_shop_id(body.nfc_id)
    if shop_id is None:
        raise HTTPException(
            status_code=400,
            detail=f"유효하지 않은 NFC ID 입니다: {body.nfc_id}",
        )

    # 사용자 보장 (register 를 거치지 않았어도 동작하도록 upsert)
    supabase.table("users").upsert({"user_id": body.user_id}).execute()

    # 이미 수집했는지 확인
    existing = (
        supabase.table("stamps")
        .select("id")
        .eq("user_id", body.user_id)
        .eq("shop_id", shop_id)
        .execute()
    )
    if existing.data:
        return StampCollectResponse(
            success=False, shop_id=shop_id, already_collected=True
        )

    # 신규 수집
    try:
        supabase.table("stamps").insert(
            {"user_id": body.user_id, "shop_id": shop_id}
        ).execute()
    except Exception:
        # 동시 요청으로 UNIQUE(user_id, shop_id) 제약에 걸린 경우 → 이미 수집으로 재확인
        again = (
            supabase.table("stamps")
            .select("id")
            .eq("user_id", body.user_id)
            .eq("shop_id", shop_id)
            .execute()
        )
        if again.data:
            return StampCollectResponse(
                success=False, shop_id=shop_id, already_collected=True
            )
        raise HTTPException(status_code=500, detail="스탬프 저장에 실패했습니다.")

    return StampCollectResponse(
        success=True, shop_id=shop_id, already_collected=False
    )


@router.get("/{user_id}", response_model=StampListResponse)
def get_user_stamps(
    user_id: str,
    supabase: Client = Depends(get_supabase),
):
    res = (
        supabase.table("stamps")
        .select("shop_id, collected_at")
        .eq("user_id", user_id)
        .order("collected_at")
        .execute()
    )
    rows = res.data or []
    stamps = [
        StampItem(shop_id=row["shop_id"], collected_at=row.get("collected_at"))
        for row in rows
    ]
    return StampListResponse(
        user_id=user_id,
        stamps=stamps,
        collected_count=len(stamps),
        total_count=TOTAL_SHOPS,
    )
