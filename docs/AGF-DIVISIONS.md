# AGF divisions implementation — 26 November 2026

AGF continues to use its existing static HTML/CSS/JavaScript site and GitHub Pages deployment. The existing paper palette, Fraunces/Manrope/JetBrains Mono typography, logo, community sections, report articles and download URLs are retained.

## Changes

- Homepage: additive Media / Insights / Advisory introduction, Work with us links, Insights commissioning route and Media wording. The report library, filters, community pillars, founder, membership, rate-board link and existing sections remain.
- `/advisory/`: commercial positioning, all requested services, engagement process, founder experience, business boundaries and working enquiry form.
- `/videos/`: AGF Media positioning, expert interviews, podcasts and educational video; sponsorship enquiry route. The honest Coming soon state remains.
- `/editorial-independence/`: editorial decision rights, sponsorship and commissioning labels, material relationship disclosures, confidentiality, member privacy and corrections contact.
- `/terms/#enquiries`: actual enquiry data handling, service boundaries and separate engagement terms. Previous founder experience is no longer described as a current Advisory partnership.
- 74 pages: shared static navigation with Advisory and consistent destination links; editorial/advisory footer links where existing footer columns permit.
- `css/divisions.css`: new layouts, accessible focus styles, responsive navigation and form. Existing global design stylesheet is retained.
- `js/navigation.js`: one menu implementation with Escape, focus handling, outside-click close, expanded state and breakpoint reset. The previous menu code was removed from `main.js` and legacy inline scripts; report filtering, report contents navigation and other scripts remain.
- `js/advisory.js`: validation, clear pending/success/error states, retained fields on errors, safe retries and interest prefilling for research/sponsorship links.
- Sitemap and `llms.txt`: new pages and three divisions, with no changes to report URLs.
- Supabase: private enquiry storage, a server-side intake function and a committed migration. No privileged credentials are sent to the browser.

## Receiving enquiries

Open AGF’s existing Supabase project (`agf-creators`, ref `dsyarsvjytgeajcckaha`), then Table Editor → `public.advisory_enquiries`. Filter `status = new` to review new business enquiries. Status can be changed to `in-review` or `closed` by an authorised administrator.

**Automatic email notifications are not configured.** AGF must review the dashboard. The public form also offers `admin@africaglobalforum.com` as a direct email route. The form does not add contacts to a newsletter or contact them automatically.

Only authorised server/admin access can read or write the table. Anonymous and signed-in public users have no table grants or RPC permission. Row level security is enabled with no public policies; the Supabase informational “RLS enabled, no policy” notice is intentional for this private table.

The Edge Function `advisory-enquiry` requires gateway JWT validation, accepts only the two AGF website origins, validates all fields and website schemes, limits body size, checks a hidden spam field, hashes the network address using a server-only HMAC key, and limits repeated submissions. A request UUID makes unchanged retries idempotent. The browser uses the existing public anon key for compatibility; the service-role key stays in the hosted function environment.

The source form accepts no customer financial records. Enquiry data must be reviewed periodically and deleted when no longer required or when a valid deletion request is handled. This release does not automate retention or email notifications.

## Verification

- `python3 tests/check_site.py`: navigation across 74 pages, duplicate IDs, new internal links and anchors, JSON metadata, unchanged report articles and all 67 homepage report entries.
- JavaScript syntax checks: three shared scripts plus 64 inline scripts across the existing pages.
- Hosted integration checks: 22 checks covering real inserts, repeated request IDs, rate limits, invalid input, request size, origin/JWT restrictions, public reads, direct inserts and direct RPC calls.
- Browser: 320, 768 and 1440 CSS-pixel widths across the homepage, Advisory, Media, editorial policy and a representative report. Mobile menu, Escape/focus return, required fields and error recovery checked.
- Synthetic records use example.com emails and are labelled as tests. Five API test records were marked `closed`; the database connector’s deletion confirmation expired, so they remain identifiable for administrator cleanup. No customer enquiries were modified.

## Deployment and maintenance

The website deploys through the existing GitHub Pages workflow on `main`. Database and Edge Function deployments are separate: reapply neither blindly. Check Supabase migration history first. The hosted migration and function were deployed and tested for this release.

For future endpoint changes, deploy the versioned contents of `supabase/functions/advisory-enquiry/` with JWT verification enabled. Keep the anonymous table/RPC grants revoked. Recheck valid submissions, duplicate protection and public access denial before shipping.

No client testimonials, client roster, partner endorsements, commercial results or performance metrics were created.

## Founder audience update — 26 November 2026

The homepage founder section and Advisory founder section display the personal profile counts supplied in the founder’s screenshots: **13,354 LinkedIn followers** and **12.5K X followers**, with X linked to `https://x.com/SKimani544`. X’s displayed rounded count is retained rather than represented as an exact number. Each platform links to the personal profile, and both sections include the snapshot date. These are separate platform counts, not a combined unique audience or AGF company-page following. Counts are static snapshots; update both HTML sections and their dates when new figures are supplied.


## Discovery-call booking — 27 November 2026

The Advisory hero and enquiry section, plus the homepage footer, link to the public **AGF Growth Discovery Call** Google appointment schedule: https://calendar.app.google/NzKcx4zccWTxscd66. The existing enquiry form and email route remain. Links open in a new tab and load no Google booking scripts on AGF.

The schedule offers 30-minute Google Meet calls on Tuesdays and Thursdays, 10:00–17:00 in Europe/Paris, with calendar conflict checking enabled. It retains Google’s initial 60-day booking window and four-hour minimum notice. The booking form requests name and email, optional company/website, and a required markets-and-goals question. Google generates the meeting details after a booking.

Manage hours, meeting details and questions in Google Calendar → Booking pages → AGF Growth Discovery Call → Edit. Update the hours shown in `advisory/index.html` if the weekly schedule changes. If replacing the booking page, update its link in both `advisory/index.html` and the homepage `index.html`. No test appointment was submitted.
