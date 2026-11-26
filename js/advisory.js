/* Real, private enquiry intake. Success is shown only after durable server confirmation. */
(function () {
  'use strict';
  const form = document.getElementById('advisoryEnquiry');
  if (!form) return;
  const button = document.getElementById('enquiry-submit');
  const status = document.getElementById('enquiry-status');
  const config = window.AGF_SUPABASE;
  const interest = new URLSearchParams(window.location.search).get('interest');
  if (interest && Array.from(form.elements.interest.options).some(o => o.value === interest)) form.elements.interest.value = interest;
  function message(text, state) { status.textContent = text; status.dataset.state = state; }
  if (!config || !config.url || !config.anonKey || !window.crypto.randomUUID) {
    message('Please email admin@africaglobalforum.com to send your enquiry.', 'error');
    return;
  }
  button.disabled = false;
  let requestId = crypto.randomUUID();
  let sending = false;
  form.addEventListener('input', function () { if (!sending) requestId = crypto.randomUUID(); });
  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    if (sending) return;
    for (const el of form.querySelectorAll('input:not([type="hidden"]), textarea')) el.value = el.value.trim();
    if (!form.reportValidity()) return;
    const payload = Object.fromEntries(new FormData(form));
    payload.request_id = requestId;
    sending = true;
    const fields = Array.from(form.querySelectorAll('input, select, textarea'));
    fields.forEach(field => { field.disabled = true; });
    button.disabled = true;
    button.textContent = 'Sending…';
    form.setAttribute('aria-busy', 'true');
    message('Sending your enquiry…', 'pending');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch(config.url + '/functions/v1/advisory-enquiry', {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + config.anonKey, 'apikey': config.anonKey },
        body: JSON.stringify(payload), signal: controller.signal
      });
      const result = await response.json();
      if (!response.ok || !result.ok || result.reference !== requestId) {
        if (response.status === 429) throw new Error('You have sent several enquiries recently. Please try again in an hour or email admin@africaglobalforum.com.');
        if (response.status === 400) throw new Error('Please check the required fields and include a brief of at least 20 characters. Your entries have been kept.');
        throw new Error('We could not confirm receipt. Your entries have been kept. Please retry or email admin@africaglobalforum.com.');
      }
      form.reset();
      message('Thank you. AGF has received your enquiry and will review it. Reference: ' + result.reference + '. We’ll use your email to respond if we can help.', 'success');
      requestId = crypto.randomUUID();
      status.focus();
    } catch (error) {
      message(error.name === 'AbortError' ? 'The connection timed out. Your entries have been kept. Please retry; repeated attempts with the same details will not create duplicate enquiries.' : (error instanceof TypeError ? 'There was a connection problem. Your entries have been kept. Please retry or email admin@africaglobalforum.com.' : error.message), 'error');
      status.focus();
    } finally {
      clearTimeout(timeout); fields.forEach(field => { field.disabled = false; }); sending = false; button.disabled = false; button.textContent = 'Send enquiry'; form.removeAttribute('aria-busy');
    }
  });
})();
