-- 수원 공방거리 스탬프 투어 — 데모 모드 관련 Supabase SQL
-- ─────────────────────────────────────────────────────────────
-- 데모 데이터는 별도 테이블이 아니라 stamps 테이블에 user_id 'demo-...' prefix 로 저장된다.
-- (실 사용자 user_id 는 'user-...' / 그 외 prefix)
-- 따라서 데모 모드/리셋을 위해 새 테이블이나 컬럼 추가는 필요 없다.
-- 아래는 (1) 데모 동작 보장 + (2) 운영 중 데모 데이터 유지보수용이다.
-- 사용법: Supabase 대시보드 → SQL Editor 에 필요한 블록만 복사해 RUN.
-- ─────────────────────────────────────────────────────────────


-- ─────────────────────────────────────────────────────────────
-- 1) (보장) RLS 비활성화
--    데모 리셋 = DELETE /api/stamps/{demo-id} 가 anon 키로 동작하려면 필요.
--    supabase_schema.sql 에서 이미 적용했다면 재실행해도 무해(idempotent).
-- ─────────────────────────────────────────────────────────────
alter table users  disable row level security;
alter table stamps disable row level security;


-- ─────────────────────────────────────────────────────────────
-- 2) (보장) user_id 인덱스 — 데모 조회/삭제 성능. 이미 있으면 무시됨.
-- ─────────────────────────────────────────────────────────────
create index if not exists idx_stamps_user_id on stamps (user_id);


-- ─────────────────────────────────────────────────────────────
-- 3) [조회] 데모 데이터 현황
-- ─────────────────────────────────────────────────────────────
-- 데모 사용자 수 / 데모 스탬프 수 한눈에 보기
select
  count(distinct user_id) filter (where user_id like 'demo-%') as demo_users,
  count(*)                filter (where user_id like 'demo-%') as demo_stamps,
  count(distinct user_id) filter (where user_id not like 'demo-%') as real_users,
  count(*)                filter (where user_id not like 'demo-%') as real_stamps
from stamps;

-- 데모 사용자별 스탬프 개수 (필요 시 주석 해제)
-- select user_id, count(*) as stamps, max(collected_at) as last_collected
-- from stamps
-- where user_id like 'demo-%'
-- group by user_id
-- order by last_collected desc;


-- ─────────────────────────────────────────────────────────────
-- 4) [정리] 데모 데이터 purge
--    실 사용자 데이터(user_id NOT LIKE 'demo-%')는 절대 건드리지 않는다.
--    실행하려면 해당 줄의 주석(--)을 풀고 RUN.
-- ─────────────────────────────────────────────────────────────
-- (a) 모든 데모 스탬프 삭제
-- delete from stamps where user_id like 'demo-%';

-- (b) 모든 데모 사용자 레코드까지 삭제
-- delete from users where user_id like 'demo-%';

-- (c) 오래된 데모 데이터만 삭제 (예: 7일 경과분)
-- delete from stamps
-- where user_id like 'demo-%'
--   and collected_at < now() - interval '7 days';
