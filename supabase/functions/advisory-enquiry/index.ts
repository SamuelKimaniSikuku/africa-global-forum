// AGF public intake. JWT gateway validation stays enabled; all writes use a server-only key.
const allowedOrigins = new Set(['https://africaglobalforum.com', 'https://www.africaglobalforum.com']);
const interests = new Set(['market-entry','customer-acquisition','community','partnerships','research','sponsorship','other']);
Deno.serve(async (req: Request) => {
  const origin = req.headers.get('origin') || '';
  const headers = { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': allowedOrigins.has(origin) ? origin : 'https://africaglobalforum.com', 'Access-Control-Allow-Headers': 'authorization, apikey, content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Vary': 'Origin', 'Cache-Control': 'no-store' };
  const reply = (data: unknown, status = 200) => new Response(JSON.stringify(data), {status, headers});
  if (!allowedOrigins.has(origin)) return reply({error: 'origin_not_allowed'}, 403);
  if (req.method === 'OPTIONS') return new Response(null, {status: 204, headers});
  if (req.method !== 'POST') return reply({error:'method_not_allowed'},405);
  if (!req.headers.get('content-type')?.toLowerCase().startsWith('application/json')) return reply({error:'invalid_content_type'},415);
  // Bound the body while streaming; a missing Content-Length cannot bypass the limit.
  const reader = req.body?.getReader();
  if (!reader) return reply({error:'invalid_request'},400);
  let body = ''; let size = 0; const decoder = new TextDecoder();
  try {
    while (true) { const {value, done} = await reader.read(); if (done) break; size += value.byteLength; if (size > 24000) { await reader.cancel(); return reply({error:'request_too_large'},413); } body += decoder.decode(value, {stream:true}); }
    body += decoder.decode();
  } catch { return reply({error:'invalid_request'},400); }
  let raw: Record<string, unknown>;
  try { raw = JSON.parse(body); if (!raw || typeof raw !== 'object' || Array.isArray(raw)) throw new Error(); } catch { return reply({error:'invalid_request'},400); }
  const field = (name: string) => typeof raw[name] === 'string' ? (raw[name] as string).trim() : '';
  const payload = {request_id:field('request_id'),name:field('name'),email:field('email').toLowerCase(),company:field('company'),website:field('website'),interest:field('interest'),markets:field('markets'),brief:field('brief')};
  const valid = (value: string, min: number, max: number) => value.length >= min && value.length <= max && !/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(value);
  if (field('fax') || !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(payload.request_id) || !valid(payload.name,1,120) || !valid(payload.email,3,254) || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.email) || !valid(payload.company,1,160) || !valid(payload.website,0,300) || !interests.has(payload.interest) || !valid(payload.markets,1,300) || !valid(payload.brief,20,4000)) return reply({error:'invalid_fields'},400);
  if (payload.website) { try { if (!['https:','http:'].includes(new URL(payload.website).protocol)) throw new Error(); } catch { return reply({error:'invalid_website'},400); } }
  const base = Deno.env.get('SUPABASE_URL'); const key = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
  if (!base || !key) return reply({error:'temporarily_unavailable'},503);
  try {
    // Only a keyed, irreversible identifier is stored, never the raw network address.
    const address = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() || 'unknown';
    const hmacKey = await crypto.subtle.importKey('raw',new TextEncoder().encode(key),{name:'HMAC',hash:'SHA-256'},false,['sign']);
    const digest = await crypto.subtle.sign('HMAC',hmacKey,new TextEncoder().encode(address));
    const client_hash = Array.from(new Uint8Array(digest),x=>x.toString(16).padStart(2,'0')).join('');
    const response = await fetch(base + '/rest/v1/rpc/submit_advisory_enquiry', {method:'POST',headers:{apikey:key,Authorization:'Bearer '+key,'Content-Type':'application/json'},body:JSON.stringify({payload,client_hash}),signal:AbortSignal.timeout(10000)});
    const result = await response.json();
    if (!response.ok) { if (result?.message === 'rate_limit') return reply({error:'rate_limit'},429); console.error('Enquiry storage failed', response.status, result?.code); return reply({error:'temporarily_unavailable'},503); }
    if (result !== payload.request_id) return reply({error:'temporarily_unavailable'},503);
    return reply({ok:true,reference:result});
  } catch { console.error('Enquiry intake unavailable'); return reply({error:'temporarily_unavailable'},503); }
});
