-- ============================================================================
-- BLAST RADIUS: what in the DATABASE references bookings.has_pets?
-- Read-only. Run in the SQL Editor (as postgres). One result set.
-- Pair it with a repo search:  git grep -n -i -E "has_?pets|haspets"
-- ============================================================================

-- views that use the column (tracked by Postgres)
select 'view' as kind, view_schema::text as schema, view_name::text as name
from information_schema.view_column_usage
where table_schema = 'public' and table_name = 'bookings' and column_name = 'has_pets'

union all

-- functions whose body mentions it (bodies are NOT dependency-tracked, so search the text)
select 'function', n.nspname::text, p.proname::text
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where p.prosrc ilike '%has_pets%'
  and n.nspname not in ('pg_catalog', 'information_schema')

union all

-- RLS policies whose expressions mention it
select 'policy', schemaname::text, (tablename || '.' || policyname)::text
from pg_policies
where qual ilike '%has_pets%' or with_check ilike '%has_pets%'

union all

-- every user trigger on the table (check what each function does)
select 'trigger on bookings', 'public', (t.tgname || ' -> ' || t.tgfoid::regproc::text)
from pg_trigger t
where t.tgrelid = 'public.bookings'::regclass and not t.tgisinternal

order by 1, 3;

-- Also check by hand: has_pets values now in the table (look for a new null group)
-- select has_pets, count(*) from public.bookings group by 1 order by 1;
