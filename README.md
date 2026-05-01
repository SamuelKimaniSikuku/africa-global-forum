# Africa Global Forum

> The convening platform for the African diaspora — connecting capital, careers, community and culture across the global Africa.

A static, single-page marketing website for Africa Global Forum (AGF). Built with vanilla HTML, CSS, and JavaScript. No build step required.

![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## Pillars

The site is structured around four core pillars:

1. **Investment Opportunities** — deal flow, syndicates, and funds across the continent.
2. **Jobs & Connections** — talent network, executive search, mentorship, job board.
3. **Community Driven** — global city chapters, salons, cultural programming.
4. **Member Services** — banking, legal, immigration, education, repatriation support.

---

## Project structure

```
agf-site/
├── index.html          # Main page
├── css/
│   └── styles.css      # All styles
├── js/
│   └── main.js         # Mobile menu, scroll reveal, form handling
├── assets/             # (place images, logos, favicons here)
├── .github/
│   └── workflows/
│       └── deploy.yml  # Auto-deploy to GitHub Pages
├── .gitignore
├── LICENSE
└── README.md
```

---

## Quick start

### View locally

The simplest option — just open the file:

```bash
open index.html
```

For a proper local server (recommended, so paths resolve correctly):

```bash
# Python 3
python3 -m http.server 8000

# Node (if you have it)
npx serve .

# PHP
php -S localhost:8000
```

Then visit `http://localhost:8000`.

---

## Deploy to GitHub Pages

### Option A — Automatic (recommended)

This repo includes a GitHub Actions workflow at `.github/workflows/deploy.yml` that auto-deploys on every push to `main`.

1. Push this repo to GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment → Source**, select **GitHub Actions**.
4. Push a commit. The workflow will deploy automatically.
5. Your site will be live at `https://<your-username>.github.io/<repo-name>/`.

### Option B — Branch-based (no Actions)

1. Push the repo to GitHub.
2. Go to **Settings → Pages**.
3. Under **Source**, select branch `main` and folder `/ (root)`.
4. Save. Site goes live in a minute or two.

### Custom domain

1. Add a `CNAME` file at the root containing your domain (e.g. `africaglobalforum.org`).
2. Configure your DNS with the records GitHub provides in **Settings → Pages**.

---

## Deploy elsewhere

Because it's static HTML/CSS/JS, this site works anywhere:

- **Netlify** — drag the folder onto [app.netlify.com/drop](https://app.netlify.com/drop), or connect the repo.
- **Vercel** — `vercel` CLI or import the repo at [vercel.com](https://vercel.com).
- **Cloudflare Pages** — connect the repo, no build command needed, output directory `/`.
- **Any static host / S3 / nginx** — just upload the files.

---

## Customization

### Colors

All colors are CSS variables at the top of `css/styles.css`:

```css
:root{
  --ink: #0E0B08;        /* near-black for text & dark sections */
  --paper: #F4EFE6;      /* warm off-white background */
  --terracotta: #C8421A; /* primary accent */
  --ochre: #D89B2C;      /* secondary accent */
  --rust: #7A2E12;
  --forest: #2A3D2A;
  /* … */
}
```

### Fonts

Loaded from Google Fonts in `index.html` `<head>`:

- **Fraunces** — display serif (headings)
- **Manrope** — body sans-serif
- **JetBrains Mono** — small caps & labels

To swap, replace the `<link>` tag and update `font-family` declarations in `styles.css`.

### Content

Edit `index.html` directly. Sections are clearly commented:

```html
<!-- HERO -->
<!-- MISSION -->
<!-- FOUR PILLARS -->
<!-- NUMBERS -->
<!-- INITIATIVES -->
<!-- VOICES -->
<!-- JOIN -->
<!-- FOOTER -->
```

### Images

Currently the site uses CSS gradients as placeholders for hero, initiative cards, and voice avatars. To use real photos:

1. Drop images into `/assets/` (e.g. `assets/voices/amara.jpg`).
2. Replace the gradient backgrounds in `styles.css` with `background-image: url('../assets/...');`.
3. Recommended: optimize images first (try [squoosh.app](https://squoosh.app)) and use `.webp` where possible.

### Logo

The current logo is a CSS-drawn geometric mark (`.logo-mark`). To use a real logo:

```html
<a class="logo" href="#">
  <img src="assets/logo.svg" alt="Africa Global Forum" width="38" height="38">
  <div class="logo-text">Africa Global Forum<small>EST · The Diaspora Network</small></div>
</a>
```

### Membership form

The form in `index.html` currently just shows a success state via `js/main.js`. To wire it to a real backend:

- **Formspree** — change `<form>` to `<form action="https://formspree.io/f/YOUR_ID" method="POST">` and remove the JS handler.
- **Mailchimp** — paste their embed form HTML into the `.join-form` container.
- **Airtable** — use [Airtable Forms](https://airtable.com/forms) and embed the iframe.
- **Custom backend** — modify the `fetch` call inside `js/main.js`.

---

## To-do before launch

- [ ] Replace placeholder leadership profiles in the **Voices** section with real names, photos, and bios
- [ ] Replace gradient placeholders with real hero and initiative imagery
- [ ] Add a real logo SVG to `/assets/`
- [ ] Wire the membership form to a real backend
- [ ] Add a favicon set (`/assets/favicon.ico`, `apple-touch-icon.png`, etc.)
- [ ] Replace the founder quote with a real quote and headshot
- [ ] Update all `<a href="#">` placeholder links with real URLs
- [ ] Add Google Analytics / Plausible / Fathom tracking if needed
- [ ] Add an `og:image` to the meta tags for social sharing previews
- [ ] Set up a custom domain

---

## Browser support

Modern evergreen browsers (Chrome, Firefox, Safari, Edge — last 2 versions). Uses:

- CSS Grid & Flexbox
- CSS custom properties
- `IntersectionObserver` (with graceful degradation)
- `backdrop-filter`

---

## License

[MIT](LICENSE) — do whatever you want with it. Attribution appreciated but not required.

---

## Contributing

PRs welcome. Keep it simple — no build tools, no frameworks. The whole point is that this is a static site anyone can edit.
