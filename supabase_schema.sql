-- 수원 공방거리 스탬프 투어 — Supabase 스키마
-- 데모 전용: RLS / JWT / OAuth 없음.
-- 사용법: Supabase 대시보드 → SQL Editor 에 이 파일 전체를 붙여넣고 RUN.

-- 1) 사용자 (브라우저 localStorage UUID를 그대로 PK로 사용)
create table if not exists users (
  user_id    text primary key,
  created_at timestamptz not null default now()
);

-- 2) 스탬프 (user_id + shop_id 조합은 유일 → 중복 수집 방지)
create table if not exists stamps (
  id           uuid primary key default gen_random_uuid(),
  user_id      text not null,
  shop_id      text not null,
  collected_at timestamptz not null default now(),
  unique (user_id, shop_id)
);

create index if not exists idx_stamps_user_id on stamps (user_id);

-- 3) RLS 비활성화 (데모용 — anon 키로 직접 읽기/쓰기 허용)
--    운영 전환 시: RLS 활성화 후 사용자별 정책을 추가해야 함.
alter table users  disable row level security;
alter table stamps disable row level security;
