-- Private intake for AGF Advisory, Insights commissions and Media sponsorship.
create table public.advisory_enquiries (
 id uuid primary key,
 created_at timestamptz not null default now(),
 name text not null check (char_length(name) between 1 and 120),
 email text not null check (char_length(email) between 3 and 254),
 company text not null check (char_length(company) between 1 and 160),
 website text not null default '' check (char_length(website) <= 300),
 interest text not null check (interest in ('market-entry','customer-acquisition','community','partnerships','research','sponsorship','other')),
 markets text not null check (char_length(markets) between 1 and 300),
 brief text not null check (char_length(brief) between 20 and 4000),
 network_hash text not null check (char_length(network_hash) = 64),
 status text not null default 'new' check (status in ('new','in-review','closed'))
);
alter table public.advisory_enquiries enable row level security;
revoke all on public.advisory_enquiries from public, anon, authenticated;
grant select, insert, update, delete on public.advisory_enquiries to service_role;
create index advisory_enquiries_created on public.advisory_enquiries (created_at desc);
create index advisory_enquiries_email on public.advisory_enquiries (email,created_at desc);
create index advisory_enquiries_network on public.advisory_enquiries (network_hash,created_at desc);
comment on table public.advisory_enquiries is 'Private business enquiries. Review in Supabase; no public read or write access. No automatic email notifications.';
-- Invoker privileges: only the server service role may call this atomic intake.
create function public.submit_advisory_enquiry(payload jsonb, client_hash text)
returns uuid language plpgsql security invoker set search_path = '' as $$
declare request_id uuid := (payload->>'request_id')::uuid; result_id uuid;
begin
 perform pg_advisory_xact_lock(713849201);
 select id into result_id from public.advisory_enquiries where id = request_id and email = payload->>'email';
 if result_id is not null then return result_id; end if;
 if (select count(*) from public.advisory_enquiries where created_at > now()-interval '1 hour' and (email = payload->>'email' or network_hash = client_hash)) >= 5
 or (select count(*) from public.advisory_enquiries where created_at > now()-interval '1 day') >= 200 then
  raise exception 'rate_limit' using errcode = 'P0001';
 end if;
 insert into public.advisory_enquiries (id,name,email,company,website,interest,markets,brief,network_hash)
 values(request_id,payload->>'name',payload->>'email',payload->>'company',coalesce(payload->>'website',''),payload->>'interest',payload->>'markets',payload->>'brief',client_hash)
 returning id into result_id;
 return result_id;
end; $$;
revoke all on function public.submit_advisory_enquiry(jsonb,text) from public,anon,authenticated;
grant execute on function public.submit_advisory_enquiry(jsonb,text) to service_role;
