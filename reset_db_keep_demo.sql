-- 데모용 유저와 스탬프를 제외한 전체 DB 초기화
-- 보존 대상 user_id: user-1780122403573-ty8n30jk9
-- 실행: Supabase 대시보드 → SQL Editor 에 붙여넣고 RUN

begin;

-- 1) 데모 유저 외 스탬프 삭제
delete from stamps
where user_id <> 'user-1780122403573-ty8n30jk9';

-- 2) 데모 유저 외 사용자 삭제
delete from users
where user_id <> 'user-1780122403573-ty8n30jk9';

commit;

-- 결과 확인
select 'users'  as "table", count(*) as remaining from users
union all
select 'stamps' as "table", count(*) as remaining from stamps;
