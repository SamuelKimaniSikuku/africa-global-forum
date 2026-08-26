-- ============================================================
-- Africa Global Forum — Creator Directory
-- Run this once in your Supabase project:
--   Dashboard → SQL Editor → New query → paste → Run
-- ============================================================

-- ---------- 1. Table ----------
create table if not exists public.creators (
  id                 uuid primary key default gen_random_uuid(),
  created_at         timestamptz not null default now(),

  -- identity
  name               text not null check (char_length(name) between 2 and 80),
  tagline            text check (char_length(tagline) <= 140),

  -- the diaspora data that makes this directory sellable
  country_origin     text not null check (char_length(country_origin) <= 60),
  country_residence  text not null check (char_length(country_residence) <= 60),
  city               text check (char_length(city) <= 60),

  -- what they make
  niches             text[] not null default '{}' check (array_length(niches, 1) is null or array_length(niches, 1) <= 5),
  primary_platform   text check (primary_platform in
                       ('instagram','tiktok','youtube','x','linkedin','podcast','newsletter','other')),
  followers_total    integer check (followers_total >= 0 and followers_total <= 500000000),

  -- links (store handles or full URLs; the page normalises both)
  instagram          text check (char_length(instagram) <= 200),
  tiktok             text check (char_length(tiktok)    <= 200),
  youtube            text check (char_length(youtube)   <= 200),
  x_handle           text check (char_length(x_handle)  <= 200),
  linkedin           text check (char_length(linkedin)  <= 200),
  website            text check (char_length(website)   <= 200),

  -- availability signals (this is what turns the list into deal flow)
  open_to_collabs    boolean not null default true,
  open_to_brand_work boolean not null default true,

  -- private: never exposed to the public page (see column grants below)
  email              text not null check (char_length(email) between 5 and 160),

  -- moderation
  status             text not null default 'pending'
                     check (status in ('pending','approved','rejected'))
);

create index if not exists creators_status_idx  on public.creators (status);
create index if not exists creators_created_idx on public.creators (created_at desc);

-- One submission per email, so nobody can flood the queue with the same profile.
create unique index if not exists creators_email_uniq on public.creators (lower(email));

-- ---------- 2. Privileges (column-level: this is what keeps email private) ----------
revoke all on public.creators from anon, authenticated;

-- Visitors may READ only these columns. `email` and `status` are deliberately absent,
-- so there is no query the public page (or anyone with the anon key) can write to get them.
grant select (
  id, created_at, name, tagline, country_origin, country_residence, city,
  niches, primary_platform, followers_total,
  instagram, tiktok, youtube, x_handle, linkedin, website,
  open_to_collabs, open_to_brand_work
) on public.creators to anon;

-- Visitors may WRITE only these columns. `status` is absent, so a submission
-- always falls back to the 'pending' default — nobody can self-approve.
grant insert (
  name, tagline, country_origin, country_residence, city,
  niches, primary_platform, followers_total,
  instagram, tiktok, youtube, x_handle, linkedin, website,
  open_to_collabs, open_to_brand_work, email
) on public.creators to anon;

-- ---------- 3. Row Level Security ----------
alter table public.creators enable row level security;

-- Read: approved profiles only. Pending and rejected rows are invisible to the public.
drop policy if exists creators_public_read on public.creators;
create policy creators_public_read
  on public.creators for select to anon
  using (status = 'approved');

-- Write: anyone may submit, but only as 'pending'. Belt-and-braces alongside the grant above.
drop policy if exists creators_anon_submit on public.creators;
create policy creators_anon_submit
  on public.creators for insert to anon
  with check (status = 'pending');

-- No update or delete policy exists, so the anon key cannot edit or remove anything.

-- ============================================================
-- Approving people
-- ============================================================
-- Dashboard → Table Editor → creators → set status to 'approved'. Or:
--
--   select id, name, country_origin, country_residence, email, created_at
--   from public.creators where status = 'pending' order by created_at;
--
--   update public.creators set status = 'approved' where id = '<paste-id>';
--
-- ============================================================
