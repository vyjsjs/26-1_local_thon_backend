from typing import Optional

TOTAL_SHOPS = 14
VALID_SHOP_IDS = {f"shop-{i}" for i in range(1, TOTAL_SHOPS + 1)}


def nfc_to_shop_id(nfc_id: str) -> Optional[str]:
    """NFC ID 를 가게 ID 로 변환. 'nfc-shop-1' -> 'shop-1'.

    입구 토템('nfc-entrance')이나 알 수 없는 값은 None 을 반환한다.
    """
    prefix = "nfc-"
    if not nfc_id.startswith(prefix):
        return None
    shop_id = nfc_id[len(prefix):]  # 'nfc-shop-1' -> 'shop-1'
    return shop_id if shop_id in VALID_SHOP_IDS else None
