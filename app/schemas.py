from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    user_id: str


class UserRegisterResponse(BaseModel):
    success: bool
    user_id: str


class StampCollectRequest(BaseModel):
    user_id: str
    nfc_id: str


class StampCollectResponse(BaseModel):
    success: bool
    shop_id: str
    already_collected: bool


class StampItem(BaseModel):
    shop_id: str
    collected_at: Optional[datetime] = None


class StampListResponse(BaseModel):
    user_id: str
    stamps: List[StampItem]
    collected_count: int
    total_count: int


class StampResetResponse(BaseModel):
    success: bool
    user_id: str
    deleted_count: int
