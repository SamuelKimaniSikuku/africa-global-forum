/* ============================================================
   Africa Global Forum — Creator Directory
   ============================================================ */
(function () {
  'use strict';

  var CFG = window.AGF_SUPABASE || {};
  var LIVE = !!(CFG.url && CFG.anonKey);

  var COLS = [
    'id','created_at','name','tagline','country_origin','country_residence','city',
    'niches','primary_platform','followers_total',
    'instagram','tiktok','youtube','x_handle','linkedin','website',
    'open_to_collabs','open_to_brand_work'
  ].join(',');

  var els = {
    grid:     document.getElementById('cdGrid'),
    count:    document.getElementById('cdCount'),
    search:   document.getElementById('cdSearch'),
    platform: document.getElementById('cdPlatform'),
    origin:   document.getElementById('cdOrigin'),
    based:    document.getElementById('cdBased'),
    niche:    document.getElementById('cdNiche'),
    avail:    document.getElementById('cdAvail'),
    setup:    document.getElementById('cdSetup'),
    form:     document.getElementById('cdForm'),
    submit:   document.getElementById('cdSubmit'),
    msg:      document.getElementById('cdMsg'),
    sCount:   document.getElementById('statCount'),
    sReach:   document.getElementById('statReach'),
    sBased:   document.getElementById('statBased'),
    sOrigin:  document.getElementById('statOrigin')
  };

  var ALL = [];

  /* ---------------- helpers ---------------- */

  function compact(n) {
    if (!n || n < 0) return '—';
    if (n >= 1e9) return (n / 1e9).toFixed(1).replace(/\.0$/, '') + 'B';
    if (n >= 1e6) return (n / 1e6).toFixed(1).replace(/\.0$/, '') + 'M';
    if (n >= 1e3) return (n / 1e3).toFixed(1).replace(/\.0$/, '') + 'K';
    return String(n);
  }

  function initials(name) {
    var parts = String(name || '').trim().split(/\s+/).filter(Boolean);
    if (!parts.length) return '?';
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }

  // Only ever hand an http(s) URL to the DOM. Anything else (javascript:, data:,
  // vbscript:) is dropped rather than rendered — profiles are moderated, but a
  // moderator approving a profile should never be able to approve a script.
  function safeUrl(raw) {
    if (!raw) return null;
    var v = String(raw).trim();
    if (!v) return null;
    if (!/^https?:\/\//i.test(v)) return null;
    try {
      var u = new URL(v);
      if (u.protocol !== 'http:' && u.protocol !== 'https:') return null;
      return u.href;
    } catch (e) { return null; }
  }

  // Accepts either a bare handle ("@amina.eats") or a full URL, returns a safe URL.
  function toUrl(raw, base) {
    if (!raw) return null;
    var v = String(raw).trim();
    if (!v) return null;
    if (/^https?:\/\//i.test(v)) return safeUrl(v);
    if (/^www\./i.test(v)) return safeUrl('https://' + v);
    if (!base) return null;                            // website field: must be a full URL
    // Anything left must look like a real handle. A bare scheme ("javascript:…"),
    // punctuation or spaces means it is not one, so render no link at all rather
    // than a broken one pointing at instagram.com/javascript:alert(1).
    var handle = v.replace(/^@+/, '');
    if (!/^[A-Za-z0-9._-]{1,64}$/.test(handle)) return null;
    return safeUrl(base + handle);
  }

  var ICONS = {
    instagram: 'M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 5 5 .1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.2 3.2-1.7 4.8-5 5-1.2.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.2-4.8-1.7-5-5C2 15.6 2 15.2 2 12s0-3.6.1-4.8c.2-3.3 1.7-4.8 5-5C8.4 2.2 8.8 2.2 12 2.2zm0 6.5c-1.8 0-3.3 1.5-3.3 3.3s1.5 3.3 3.3 3.3 3.3-1.5 3.3-3.3-1.5-3.3-3.3-3.3zm5.6-1.6a1.2 1.2 0 11-2.4 0 1.2 1.2 0 012.4 0zM12 7a5 5 0 100 10 5 5 0 000-10z',
    tiktok:    'M16.6 5.82A4.28 4.28 0 0115.54 3h-3.09v12.4a2.59 2.59 0 01-2.59 2.5 2.59 2.59 0 01-2.59-2.59 2.59 2.59 0 012.59-2.59c.27 0 .53.04.77.12v-3.1a5.7 5.7 0 00-.77-.05A5.69 5.69 0 004.17 15.4a5.69 5.69 0 005.69 5.69 5.69 5.69 0 005.69-5.69V9.01a7.35 7.35 0 004.29 1.37V7.29a4.29 4.29 0 01-3.24-1.47z',
    youtube:   'M23 12s0-3.9-.5-5.8a3 3 0 00-2.1-2.1C18.5 3.6 12 3.6 12 3.6s-6.5 0-8.4.5A3 3 0 001.5 6.2C1 8.1 1 12 1 12s0 3.9.5 5.8a3 3 0 002.1 2.1c1.9.5 8.4.5 8.4.5s6.5 0 8.4-.5a3 3 0 002.1-2.1C23 15.9 23 12 23 12zM9.9 15.6V8.4l6.3 3.6-6.3 3.6z',
    x:         'M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z',
    linkedin:  'M19 0H5C2.2 0 0 2.2 0 5v14c0 2.8 2.2 5 5 5h14c2.8 0 5-2.2 5-5V5c0-2.8-2.2-5-5-5zM8 19H5V8h3v11zM6.5 6.7c-1 0-1.7-.8-1.7-1.7s.8-1.7 1.7-1.7 1.7.8 1.7 1.7-.7 1.7-1.7 1.7zM20 19h-3v-5.6c0-3.4-4-3.1-4 0V19h-3V8h3v1.8c1.4-2.6 7-2.8 7 2.5V19z',
    website:   'M12 2a10 10 0 100 20 10 10 0 000-20zm6.9 6h-3a15.7 15.7 0 00-1.4-3.6A8 8 0 0118.9 8zM12 4c.8 1.2 1.4 2.5 1.8 4h-3.6c.4-1.5 1-2.8 1.8-4zM4.3 14a8 8 0 010-4h3.4a16.5 16.5 0 000 4H4.3zm.8 2h3a15.7 15.7 0 001.4 3.6A8 8 0 015.1 16zm3-8h-3a8 8 0 014.4-3.6A15.7 15.7 0 008.1 8zM12 20c-.8-1.2-1.4-2.5-1.8-4h3.6c-.4 1.5-1 2.8-1.8 4zm2.2-6H9.8a14.6 14.6 0 010-4h4.4a14.6 14.6 0 010 4zm.3 5.6a15.7 15.7 0 001.4-3.6h3a8 8 0 01-4.4 3.6zm1.8-5.6a16.5 16.5 0 000-4h3.4a8 8 0 010 4h-3.4z'
  };

  var PLATFORMS = [
    { key: 'instagram', label: 'Instagram', base: 'https://instagram.com/',   icon: 'instagram' },
    { key: 'tiktok',    label: 'TikTok',    base: 'https://tiktok.com/@',     icon: 'tiktok'    },
    { key: 'youtube',   label: 'YouTube',   base: 'https://youtube.com/@',    icon: 'youtube'   },
    { key: 'x_handle',  label: 'X',         base: 'https://x.com/',           icon: 'x'         },
    { key: 'linkedin',  label: 'LinkedIn',  base: 'https://linkedin.com/in/', icon: 'linkedin'  },
    { key: 'website',   label: 'Website',   base: null,                       icon: 'website'   }
  ];

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;             // never innerHTML for user data
    return n;
  }

  function svgIcon(path) {
    var ns = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('fill', 'currentColor');
    svg.setAttribute('aria-hidden', 'true');
    var p = document.createElementNS(ns, 'path');
    p.setAttribute('d', path);
    svg.appendChild(p);
    return svg;
  }

  /* ---------------- render ---------------- */

  function card(c) {
    var wrap = el('article', 'cd-card');

    var top = el('div', 'cd-card-top');
    top.appendChild(el('div', 'cd-avatar', initials(c.name)));

    var id = el('div', 'cd-card-id');
    id.appendChild(el('h3', 'cd-card-name', c.name));
    var where = [c.city, c.country_residence].filter(Boolean).join(', ');
    id.appendChild(el('div', 'cd-corridor', c.country_origin + ' → ' + (where || '—')));
    top.appendChild(id);
    wrap.appendChild(top);

    if (c.tagline) wrap.appendChild(el('p', 'cd-tagline', c.tagline));

    var niches = Array.isArray(c.niches) ? c.niches : [];
    if (niches.length || c.open_to_collabs || c.open_to_brand_work) {
      var tags = el('div', 'cd-tags');
      niches.slice(0, 5).forEach(function (n) { tags.appendChild(el('span', 'cd-tag', n)); });
      if (c.open_to_brand_work) tags.appendChild(el('span', 'cd-tag is-open', 'Open to brand work'));
      if (c.open_to_collabs)    tags.appendChild(el('span', 'cd-tag is-open', 'Open to collabs'));
      wrap.appendChild(tags);
    }

    if (c.followers_total) {
      var reach = el('div', 'cd-reach');
      reach.appendChild(el('b', null, compact(c.followers_total)));
      reach.appendChild(document.createTextNode(' combined reach'));
      wrap.appendChild(reach);
    }

    var links = el('div', 'cd-links');
    PLATFORMS.forEach(function (p) {
      var url = toUrl(c[p.key], p.base);
      if (!url) return;
      var a = el('a', 'cd-link');
      a.href = url;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.setAttribute('aria-label', c.name + ' on ' + p.label);
      a.title = p.label;
      a.appendChild(svgIcon(ICONS[p.icon]));
      links.appendChild(a);
    });
    if (links.childNodes.length) wrap.appendChild(links);

    return wrap;
  }

  function state(title, body) {
    var s = el('div', 'cd-state');
    s.appendChild(el('h3', null, title));
    s.appendChild(el('p', null, body));
    return s;
  }

  function stats(rows) {
    els.sCount.textContent  = rows.length ? String(rows.length) : '—';
    var reach = rows.reduce(function (a, c) { return a + (c.followers_total || 0); }, 0);
    els.sReach.textContent  = reach ? compact(reach) : '—';
    els.sBased.textContent  = String(uniq(rows, 'country_residence').length || '—');
    els.sOrigin.textContent = String(uniq(rows, 'country_origin').length || '—');
  }

  function uniq(rows, key) {
    var seen = {};
    rows.forEach(function (r) {
      var v = (r[key] || '').trim();
      if (v) seen[v.toLowerCase()] = v;
    });
    return Object.keys(seen).map(function (k) { return seen[k]; }).sort();
  }

  function fillSelect(sel, values, allLabel) {
    sel.textContent = '';
    var o = el('option', null, allLabel);
    o.value = '';
    sel.appendChild(o);
    values.forEach(function (v) {
      var opt = el('option', null, v);
      opt.value = v;
      sel.appendChild(opt);
    });
  }

  function apply() {
    var q    = (els.search.value || '').trim().toLowerCase();
    var plat = els.platform.value;
    var org  = els.origin.value;
    var bas  = els.based.value;
    var nic  = els.niche.value;
    var av   = els.avail.value;

    var rows = ALL.filter(function (c) {
      if (plat && c.primary_platform !== plat) return false;
      if (org && c.country_origin !== org) return false;
      if (bas && c.country_residence !== bas) return false;
      if (nic && !(c.niches || []).some(function (n) { return n === nic; })) return false;
      if (av === 'brand' && !c.open_to_brand_work) return false;
      if (av === 'collab' && !c.open_to_collabs) return false;
      if (q) {
        var hay = [c.name, c.tagline, c.city, c.country_origin, c.country_residence,
                   (c.niches || []).join(' '), c.instagram, c.tiktok, c.youtube,
                   c.x_handle, c.linkedin]
                   .filter(Boolean).join(' ').toLowerCase();
        if (hay.indexOf(q) === -1) return false;
      }
      return true;
    });

    els.grid.textContent = '';
    if (!rows.length) {
      els.grid.appendChild(state('No one matches that yet',
        'Try clearing a filter — or be the first creator in that corridor by adding yourself below.'));
    } else {
      var frag = document.createDocumentFragment();
      rows.forEach(function (c) { frag.appendChild(card(c)); });
      els.grid.appendChild(frag);
    }
    els.count.textContent = rows.length + (rows.length === 1 ? ' creator' : ' creators');
  }

  /* ---------------- load ---------------- */

  function load() {
    if (!LIVE) {
      els.setup.hidden = false;
      els.grid.appendChild(state('The directory is not connected yet',
        'Run supabase-schema.sql in your Supabase project, then paste your project URL and anon key into creators/config.js.'));
      els.count.textContent = '0 creators';
      return;
    }

    // No status filter here on purpose: `anon` has no read privilege on the
    // `status` column, so filtering by it is rejected outright. Row Level
    // Security already limits this response to approved profiles server-side.
    var url = CFG.url.replace(/\/+$/, '') +
              '/rest/v1/creators?select=' + encodeURIComponent(COLS) +
              '&order=followers_total.desc.nullslast';

    fetch(url, { headers: { apikey: CFG.anonKey, Authorization: 'Bearer ' + CFG.anonKey } })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (rows) {
        ALL = Array.isArray(rows) ? rows : [];
        stats(ALL);
        fillSelect(els.origin, uniq(ALL, 'country_origin'),    'Any origin');
        fillSelect(els.based,  uniq(ALL, 'country_residence'), 'Anywhere');

        var nicheSet = {};
        ALL.forEach(function (c) {
          (c.niches || []).forEach(function (n) { if (n) nicheSet[n] = true; });
        });
        fillSelect(els.niche, Object.keys(nicheSet).sort(), 'Any niche');

        if (!ALL.length) {
          els.grid.appendChild(state('The directory is open',
            'No approved profiles yet. Add yourself below and you will be the first name a brand sees.'));
          els.count.textContent = '0 creators';
          return;
        }
        apply();
      })
      .catch(function (err) {
        els.grid.appendChild(state('Could not load the directory',
          'Something went wrong reaching Supabase (' + err.message + '). Check the project URL and anon key in config.js.'));
        els.count.textContent = '—';
      });
  }

  /* ---------------- submit ---------------- */

  function say(text, kind) {
    els.msg.textContent = text;
    els.msg.className = 'cd-msg' + (kind ? ' is-' + kind : '');
  }

  function submit(e) {
    e.preventDefault();
    if (!LIVE) { say('The directory is not connected to Supabase yet.', 'err'); return; }
    if (els.form.elements.company.value) return;         // honeypot: silent drop

    var fd = new FormData(els.form);
    var seenNiche = {};
    var niches = String(fd.get('niches') || '')
      .split(',').map(function (s) { return s.trim(); })
      .filter(function (s) {
        if (!s) return false;
        var k = s.toLowerCase();
        if (seenNiche[k]) return false;                 // "Food, Travel, Food" → two tags, not three
        seenNiche[k] = true;
        return true;
      })
      .slice(0, 5);

    var followers = parseInt(String(fd.get('followers_total') || '').replace(/[^\d]/g, ''), 10);

    var row = {
      name:              String(fd.get('name') || '').trim(),
      tagline:           String(fd.get('tagline') || '').trim().slice(0, 140) || null,
      country_origin:    String(fd.get('country_origin') || '').trim(),
      country_residence: String(fd.get('country_residence') || '').trim(),
      city:              String(fd.get('city') || '').trim() || null,
      niches:            niches,
      primary_platform:  String(fd.get('primary_platform') || '') || null,
      followers_total:   isNaN(followers) ? null : followers,
      instagram:         String(fd.get('instagram') || '').trim() || null,
      tiktok:            String(fd.get('tiktok') || '').trim() || null,
      youtube:           String(fd.get('youtube') || '').trim() || null,
      x_handle:          String(fd.get('x_handle') || '').trim() || null,
      linkedin:          String(fd.get('linkedin') || '').trim() || null,
      website:           String(fd.get('website') || '').trim() || null,
      open_to_collabs:   fd.get('open_to_collabs') === 'on',
      open_to_brand_work:fd.get('open_to_brand_work') === 'on',
      email:             String(fd.get('email') || '').trim()
    };

    // The form carries `novalidate` so these are enforced here, not by the browser.
    if (!row.name)              { say('Add your name.', 'err'); return; }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(row.email)) { say('That email does not look right.', 'err'); return; }
    if (!row.country_origin)    { say('Add the country you are from.', 'err'); return; }
    if (!row.country_residence) { say('Add the country you live in.', 'err'); return; }

    var hasLink = ['instagram','tiktok','youtube','x_handle','linkedin','website']
      .some(function (k) { return row[k]; });
    if (!hasLink) { say('Add at least one link — that is the whole point of the directory.', 'err'); return; }

    // Publishing someone's name, city and links needs their explicit agreement.
    if (!els.form.elements.consent.checked) {
      say('Please tick the box agreeing to your profile being shown publicly.', 'err'); return;
    }

    els.submit.disabled = true;
    say('Sending…');

    fetch(CFG.url.replace(/\/+$/, '') + '/rest/v1/creators', {
      method: 'POST',
      headers: {
        apikey: CFG.anonKey,
        Authorization: 'Bearer ' + CFG.anonKey,
        'Content-Type': 'application/json',
        Prefer: 'return=minimal'
      },
      body: JSON.stringify(row)
    })
      .then(function (r) {
        if (r.status === 409) throw new Error('DUPLICATE');
        if (!r.ok) return r.text().then(function (t) { throw new Error(t || ('HTTP ' + r.status)); });
        els.form.reset();
        say('You are in the queue. Once Samuel approves your profile it goes live on this page — usually within a day.', 'ok');
      })
      .catch(function (err) {
        if (err.message === 'DUPLICATE') {
          say('That email is already in the directory. Reply to your confirmation email to update your links.', 'err');
        } else {
          say('That did not send. Check your details and try again.', 'err');
        }
      })
      .then(function () { els.submit.disabled = false; });
  }

  /* ---------------- wire ---------------- */

  ['search','platform','origin','based','niche','avail'].forEach(function (k) {
    if (els[k]) els[k].addEventListener('input', apply);
  });
  if (els.form) els.form.addEventListener('submit', submit);

  load();
})();
