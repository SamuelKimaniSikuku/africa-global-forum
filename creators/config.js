/* ============================================================
   Africa Global Forum — Creator Directory config

   Fill these two values in from your Supabase project:
     Dashboard → Project Settings → API
       url     = "Project URL"
       anonKey = "Project API keys → anon / public"

   The anon key is designed to be public — it is safe in this file.
   What actually protects the data is the Row Level Security in
   supabase-schema.sql: it lets visitors read approved profiles only,
   write nothing but a pending submission, and never see anyone's email.
   Run that schema BEFORE putting a key here.
   ============================================================ */

window.AGF_SUPABASE = {
  url: '',
  anonKey: ''
};
