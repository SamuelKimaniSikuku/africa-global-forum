/* ============================================
   Africa Global Forum — Listen to this report
   Browser-native text-to-speech player.
   Self-contained: injects its own UI + styles.
   No-ops gracefully when speech synthesis or
   the article container is unavailable.
   ============================================ */
(function () {
  'use strict';

  if (!('speechSynthesis' in window) || typeof SpeechSynthesisUtterance === 'undefined') return;

  var container = document.querySelector('.report-body-content') || document.querySelector('article');
  if (!container) return;

  // ---------- Collect readable blocks ----------
  var blocks = [];
  var nodes = container.querySelectorAll('h2, h3, p, li, blockquote');
  nodes.forEach(function (el) {
    // Skip elements that live inside another collected element (li inside collected p never happens;
    // but p inside blockquote can) — keep it simple: skip nested duplicates.
    if (el.parentElement && el.parentElement.closest && el.parentElement.closest('blockquote') && el.tagName === 'P') return;
    var text = (el.innerText || '').replace(/\s+/g, ' ').trim();
    if (text.length > 1) blocks.push({ el: el, text: text });
  });
  if (blocks.length < 3) return;

  var totalWords = blocks.reduce(function (n, b) { return n + b.text.split(' ').length; }, 0);
  var estMinutes = Math.max(1, Math.round(totalWords / 170));

  // ---------- Split long text into utterance-safe chunks ----------
  function chunkText(text) {
    if (text.length <= 220) return [text];
    var sentences = text.match(/[^.!?]+[.!?]+["')\]]*\s*|.+$/g) || [text];
    var chunks = [], cur = '';
    sentences.forEach(function (s) {
      if ((cur + s).length > 220 && cur) { chunks.push(cur.trim()); cur = s; }
      else cur += s;
    });
    if (cur.trim()) chunks.push(cur.trim());
    return chunks;
  }

  // ---------- Voice selection ----------
  var chosenVoice = null;
  function pickVoice() {
    var voices = speechSynthesis.getVoices() || [];
    if (!voices.length) return;
    var prefs = ['Google UK English Female', 'Google US English', 'Samantha', 'Daniel', 'Serena'];
    for (var i = 0; i < prefs.length; i++) {
      var v = voices.filter(function (x) { return x.name.indexOf(prefs[i]) === 0; })[0];
      if (v) { chosenVoice = v; return; }
    }
    chosenVoice = voices.filter(function (x) { return /^en(-|_)/i.test(x.lang); })[0] || voices[0];
  }
  pickVoice();
  if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.addEventListener('voiceschanged', pickVoice);
  }

  // ---------- Styles ----------
  var css = ''
    + '.agf-listen{position:fixed;right:22px;bottom:22px;z-index:900;font-family:"JetBrains Mono",monospace}'
    + '.agf-listen-btn{display:inline-flex;align-items:center;gap:9px;background:#0E0B08;color:#F4EFE6;border:none;border-radius:999px;padding:13px 20px;font-family:inherit;font-size:12px;letter-spacing:0.08em;text-transform:uppercase;cursor:pointer;box-shadow:0 10px 30px -12px rgba(14,11,8,0.5);transition:background 0.2s,transform 0.2s}'
    + '.agf-listen-btn:hover{background:#C8421A;transform:translateY(-1px)}'
    + '.agf-listen-panel{display:none;align-items:center;gap:8px;background:#0E0B08;color:#F4EFE6;border-radius:999px;padding:9px 12px;box-shadow:0 10px 30px -12px rgba(14,11,8,0.5)}'
    + '.agf-listen.is-open .agf-listen-btn{display:none}'
    + '.agf-listen.is-open .agf-listen-panel{display:inline-flex}'
    + '.agf-listen-panel button{background:transparent;border:1px solid rgba(244,239,230,0.25);color:#F4EFE6;border-radius:999px;width:34px;height:34px;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;font-family:inherit;font-size:11px;padding:0}'
    + '.agf-listen-panel button:hover{border-color:#C8421A;color:#C8421A}'
    + '.agf-listen-panel .agf-listen-rate{width:auto;padding:0 10px}'
    + '.agf-listen-progress{font-size:10px;letter-spacing:0.08em;color:rgba(244,239,230,0.6);padding:0 4px;min-width:52px;text-align:center}'
    + '.agf-listen-current{background:rgba(200,66,26,0.10);box-shadow:-4px 0 0 0 #C8421A;transition:background 0.3s}'
    + '@media (max-width:640px){.agf-listen{right:14px;bottom:14px}}';
  var styleEl = document.createElement('style');
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // ---------- UI ----------
  var root = document.createElement('div');
  root.className = 'agf-listen';
  root.innerHTML =
    '<button type="button" class="agf-listen-btn" aria-label="Listen to this report">' +
      svgSpeaker() + '<span>Listen &middot; ' + estMinutes + ' min</span>' +
    '</button>' +
    '<div class="agf-listen-panel" role="group" aria-label="Audio player">' +
      '<button type="button" class="agf-listen-toggle" aria-label="Pause">' + svgPause() + '</button>' +
      '<span class="agf-listen-progress">0%</span>' +
      '<button type="button" class="agf-listen-rate" aria-label="Playback speed">1x</button>' +
      '<button type="button" class="agf-listen-stop" aria-label="Stop">' + svgStop() + '</button>' +
    '</div>';
  document.body.appendChild(root);

  function svgSpeaker() { return '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 010 7M19 5a9 9 0 010 14"/></svg>'; }
  function svgPlay() { return '<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>'; }
  function svgPause() { return '<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>'; }
  function svgStop() { return '<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><rect x="5" y="5" width="14" height="14" rx="1"/></svg>'; }

  var btn = root.querySelector('.agf-listen-btn');
  var toggleBtn = root.querySelector('.agf-listen-toggle');
  var stopBtn = root.querySelector('.agf-listen-stop');
  var rateBtn = root.querySelector('.agf-listen-rate');
  var progressEl = root.querySelector('.agf-listen-progress');

  // ---------- Playback state ----------
  var rates = [1, 1.25, 1.5];
  var rateIdx = 0;
  var blockIdx = 0;
  var chunkQueue = [];
  var playing = false;
  var paused = false;
  var keepalive = null;

  function highlight(i) {
    blocks.forEach(function (b) { b.el.classList.remove('agf-listen-current'); });
    var b = blocks[i];
    if (!b) return;
    b.el.classList.add('agf-listen-current');
    var r = b.el.getBoundingClientRect();
    if (r.top < 80 || r.bottom > window.innerHeight - 80) {
      b.el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  function updateProgress() {
    progressEl.textContent = Math.round((blockIdx / blocks.length) * 100) + '%';
  }

  function speakNext() {
    if (!playing) return;
    if (!chunkQueue.length) {
      blockIdx++;
      if (blockIdx >= blocks.length) { stop(); return; }
      chunkQueue = chunkText(blocks[blockIdx].text);
      highlight(blockIdx);
      updateProgress();
    }
    var text = chunkQueue.shift();
    var u = new SpeechSynthesisUtterance(text);
    if (chosenVoice) u.voice = chosenVoice;
    u.rate = rates[rateIdx];
    u.onend = function () { speakNext(); };
    u.onerror = function () { speakNext(); };
    speechSynthesis.speak(u);
  }

  function play() {
    playing = true;
    paused = false;
    root.classList.add('is-open');
    toggleBtn.innerHTML = svgPause();
    toggleBtn.setAttribute('aria-label', 'Pause');
    chunkQueue = chunkText(blocks[blockIdx].text);
    highlight(blockIdx);
    updateProgress();
    speakNext();
    // Chrome workaround: synthesis silently stops on long sessions unless nudged
    keepalive = setInterval(function () {
      if (playing && !paused && speechSynthesis.speaking) { speechSynthesis.pause(); speechSynthesis.resume(); }
    }, 12000);
  }

  function stop() {
    playing = false;
    paused = false;
    clearInterval(keepalive);
    speechSynthesis.cancel();
    blocks.forEach(function (b) { b.el.classList.remove('agf-listen-current'); });
    blockIdx = 0;
    chunkQueue = [];
    root.classList.remove('is-open');
  }

  btn.addEventListener('click', play);

  toggleBtn.addEventListener('click', function () {
    if (paused) {
      paused = false;
      speechSynthesis.resume();
      toggleBtn.innerHTML = svgPause();
      toggleBtn.setAttribute('aria-label', 'Pause');
    } else {
      paused = true;
      speechSynthesis.pause();
      toggleBtn.innerHTML = svgPlay();
      toggleBtn.setAttribute('aria-label', 'Play');
    }
  });

  stopBtn.addEventListener('click', stop);

  rateBtn.addEventListener('click', function () {
    rateIdx = (rateIdx + 1) % rates.length;
    rateBtn.textContent = rates[rateIdx] + 'x';
    // Apply to subsequent utterances: cancel current chunk, resume from queue
    if (playing && !paused) {
      speechSynthesis.cancel();
      // onend of cancelled utterance won't fire consistently across browsers; restart pump
      setTimeout(function () { if (playing && !speechSynthesis.speaking) speakNext(); }, 150);
    }
  });

  window.addEventListener('beforeunload', function () { speechSynthesis.cancel(); });
})();
