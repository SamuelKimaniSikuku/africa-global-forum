#!/usr/bin/env python3
"""Generate the AGF report PDF: Your Address Pays Better Than Your Following (2026)."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, KeepTogether, Image, PageBreak
)

# ---- AGF brand palette ----
INK        = colors.HexColor("#0E0B08")
PAPER      = colors.HexColor("#F4EFE6")
TERRACOTTA = colors.HexColor("#C8421A")
OCHRE      = colors.HexColor("#D89B2C")
RUST       = colors.HexColor("#7A2E12")
FOREST     = colors.HexColor("#2A3D2A")
CLAY       = colors.HexColor("#A05A2C")
MUTED      = colors.HexColor("#6B635A")
LIGHT      = colors.HexColor("#EAE2D4")
WHITE      = colors.white

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "diaspora-creator-income-2026", "img")
OUT = os.path.join(HERE, "diaspora-creator-income-2026.pdf")

CONTENT_W = 170 * mm

styles = getSampleStyleSheet()


def S(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)


body    = S("body", fontName="Helvetica", fontSize=9.5, leading=14.5, textColor=INK, spaceAfter=7)
lede    = S("lede", fontName="Helvetica", fontSize=12, leading=18, textColor=INK, spaceAfter=8)
h1      = S("h1", fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=INK, spaceAfter=6)
h2      = S("h2", fontName="Helvetica-Bold", fontSize=14, leading=17, textColor=TERRACOTTA,
            spaceBefore=16, spaceAfter=5, keepWithNext=1)
h3      = S("h3", fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=RUST,
            spaceBefore=10, spaceAfter=3, keepWithNext=1)
label   = S("label", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=OCHRE, spaceAfter=3)
small   = S("small", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MUTED)
cap     = S("cap", fontName="Helvetica-Oblique", fontSize=7.8, leading=10.5, textColor=MUTED,
            spaceBefore=3, spaceAfter=10)
pull    = S("pull", fontName="Helvetica-BoldOblique", fontSize=11.5, leading=16,
            textColor=RUST, spaceBefore=6, spaceAfter=8)
th      = S("th", fontName="Helvetica-Bold", fontSize=8.4, leading=11, textColor=WHITE)
cell    = S("cell", fontName="Helvetica", fontSize=8.6, leading=12, textColor=INK)
cell_b  = S("cell_b", fontName="Helvetica-Bold", fontSize=8.6, leading=12, textColor=INK)
cover_w = S("cover_w", fontName="Helvetica", fontSize=10, leading=15, textColor=WHITE)
big_num = S("big_num", fontName="Helvetica-Bold", fontSize=21, leading=25, textColor=WHITE,
            alignment=TA_CENTER)
big_lbl = S("big_lbl", fontName="Helvetica", fontSize=9, leading=13, textColor=OCHRE,
            alignment=TA_CENTER)


def bullets(items, st=body):
    return [Paragraph(f'<font color="#C8421A">&bull;</font>&nbsp;&nbsp;{i}', st) for i in items]


def fig(name, caption, max_w=CONTENT_W, max_h=205 * mm):
    """Place a chart PNG scaled to fit, with its caption."""
    path = os.path.join(IMG, name)
    iw, ih = ImageReader(path).getSize()
    w = max_w
    h = w * ih / iw
    if h > max_h:
        h = max_h
        w = h * iw / ih
    return KeepTogether([Image(path, width=w, height=h), Paragraph(caption, cap)])


def table(data, widths, header=True):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LIGHT),
    ]
    if header:
        cmds += [("BACKGROUND", (0, 0), (-1, 0), TERRACOTTA),
                 ("LINEBELOW", (0, 0), (-1, 0), 0, WHITE)]
        for r in range(1, len(data)):
            if r % 2 == 1:
                cmds.append(("BACKGROUND", (0, r), (-1, r), WHITE))
    t.setStyle(TableStyle(cmds))
    return t


def callout(text, bg=FOREST):
    t = Table([[Paragraph(text, cover_w)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 11), ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
    ]))
    return KeepTogether([Spacer(1, 3 * mm), t, Spacer(1, 5 * mm)])


# ---------- page furniture ----------
def furniture(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(INK)
    canvas.rect(0, A4[1] - 16 * mm, A4[0], 16 * mm, fill=1, stroke=0)
    canvas.setFillColor(OCHRE)
    canvas.rect(0, A4[1] - 16.8 * mm, A4[0], 0.8 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(20 * mm, A4[1] - 10.5 * mm, "AFRICA GLOBAL FORUM")
    canvas.setFillColor(OCHRE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "Your Address Pays Better · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Rates as at 11 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="Your Address Pays Better Than Your Following (2026)",
                      author="Africa Global Forum",
                      subject="Which social platforms actually earn Africans abroad money")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])

story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("Your Address Pays Better", h1),
    Paragraph("Than Your Following",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Which social platforms actually earn Africans abroad money — and why the diaspora holds a "
        "structural advantage over creators back home that almost nobody is deliberately using.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("1,000×", big_num), Paragraph("~10", big_num),
    Paragraph("112", big_num), Paragraph("$0", big_num),
], [
    Paragraph("gap between the best and<br/>worst-paying platforms", big_lbl),
    Paragraph("countries in TikTok's payout<br/>programme — none African", big_lbl),
    Paragraph("paying supporters needed<br/>for $1,000 a month", big_lbl),
    Paragraph("Instagram's direct ad-revenue<br/>share on Reels", big_lbl),
]], colWidths=[CONTENT_W / 4] * 4)
kpi.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), INK),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 14),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story += [kpi, Spacer(1, 6 * mm)]
story += [fig("views_for_1000.png",
              "Monthly views required to earn $1,000 on each platform, using the midpoint of each "
              "published rate range. Log scale — each gridline is ten times the last.")]
story += [Paragraph(
    "Published August 2026 by Africa Global Forum · "
    "africaglobalforum.com/reports/diaspora-creator-income-2026", small), PageBreak()]

# ================= 01 =================
story += [
    Paragraph("01 · Executive Summary", h2),
    Paragraph(
        "Almost every guide to making money online tells you to grow your following. That is the wrong "
        "variable. For an African living abroad in 2026, income from social media is decided mostly by two "
        "things you can choose deliberately on day one: <b>which platform you post to</b>, and <b>which "
        "country your audience watches from</b>. Follower count is a distant third. The gaps are not "
        "marginal — they are order-of-magnitude.", body),
]
story += bullets([
    "<b>The same 100,000 views can be worth $1,000 or $50</b>, depending entirely on platform and audience "
    "geography. YouTube long-form to a US or UK audience pays roughly <b>$7.50–$12 per 1,000 views</b>; "
    "Facebook Reels typically pays <b>$0.02–$0.20</b>.",
    "<b>TikTok's payout programme does not operate in Africa.</b> The Creator Rewards Program runs in "
    "roughly ten countries — the US, UK, Germany, France, Japan, South Korea, Brazil, Mexico and a few "
    "others. <b>None of them are African.</b> If you live in London or Toronto you are eligible; your cousin "
    "in Lagos, posting the same video to the same audience, is not.",
    "<b>Instagram pays no direct ad-revenue share on Reels at all.</b> It is a brilliant place to build an "
    "audience and a poor place to be paid by the platform.",
    "<b>X is the worst-paying major platform by a distance</b> — roughly $8–$12 per <i>million</i> verified "
    "impressions.",
    "<b>112 people paying $10 a month beats 100,000 monthly views on almost any platform</b> — and it is a "
    "far more reachable target for a diaspora creator with a specific, committed audience.",
])
story += [Paragraph(
    "The diaspora is sitting on a payout eligibility that people back home cannot access, serving an "
    "audience that Western advertisers pay a premium to reach. Very few people are using both facts "
    "on purpose.", pull)]

# ================= 02 =================
story += [
    Paragraph("02 · The Two Numbers That Decide Everything", h2),
    Paragraph(
        "Strip away the noise and creator income from any ad-funded platform is one multiplication: "
        "<b>views × RPM = income</b>. RPM — revenue per mille — is what you actually receive per 1,000 views "
        "<i>after</i> the platform takes its cut. It is not CPM, which is what the advertiser pays before "
        "the split, and confusing the two is the most common way creators overestimate their earnings.", body),
    Paragraph(
        "Almost all advice concentrates on views, because views feel like the thing you control. But RPM "
        "varies by a factor of about <b>1,000×</b> across platforms and audiences, while realistic view "
        "counts for an individual creator vary by maybe 10×. <b>The variable nobody optimises is the one "
        "that matters most.</b> RPM is set by three things, in order of impact: which platform; where your "
        "audience watches from; and what your content is about.", body),
]

# ================= 03 =================
story += [
    Paragraph("03 · Who Can Even Get Paid", h2),
    Paragraph(
        "Before rates, there is a prior question most comparisons skip: <b>are you allowed into the payout "
        "programme at all?</b> Monetisation programmes are geographically restricted, and the restrictions "
        "do not follow where your audience is — they follow where <i>you</i> are.", body),
    fig("eligibility.png",
        "Fig 1 — Payout access depends on where the creator is, not where the audience is. "
        "“Conditional” means available in principle but gated by country availability, platform invitation, "
        "or whether the payment rails reach you.", max_w=130 * mm),
    Paragraph(
        "The <b>TikTok row is the important one</b>. A Nigerian creator in Manchester and a Nigerian creator "
        "in Lagos can post the identical video, to the identical audience, and get identical views. "
        "<b>One gets paid by TikTok. The other does not.</b> The difference is a postcode.", body),
    Paragraph(
        "This is a genuine, legal, structural advantage the diaspora holds — and one of the very few places "
        "where the migration trade-off pays a dividend rather than charging a fee. It is also, quietly, the "
        "reason a lot of “African creator success” stories turn out to involve someone living in "
        "Atlanta or Croydon.", body),
    Paragraph(
        "<b>A warning attached to it.</b> Some creators back home use VPNs or foreign-registered accounts to "
        "get around geographic restrictions. This violates platform terms, and the usual outcome is not a "
        "warning but permanent demonetisation and forfeited earnings. If you are in the diaspora you do not "
        "need to do any of this — and if you are advising family at home, the honest advice is to build on "
        "platforms that <i>do</i> pay them (YouTube) rather than risk a ban on one that does not. The one "
        "platform genuinely open almost everywhere is <b>YouTube</b>, whose Partner Programme operates "
        "across Nigeria, Kenya, South Africa, Ghana, Egypt and much of the continent.", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · What Each Platform Actually Pays", h2),
    fig("platform_rpm.png",
        "Fig 2 — Earnings per 1,000 views, log scale. The distance from top to bottom is roughly a "
        "factor of a thousand."),
    Paragraph("YouTube long-form — the only platform that reliably pays real money", h3),
    Paragraph(
        "US RPM sits around <b>$7.50–$12</b>, and the whole system is built for durability: videos keep "
        "earning for years, the audience is searchable, and the Partner Programme is open in most African "
        "countries as well as every diaspora country. Finance, insurance and B2B command the top of the "
        "range; US CPMs in those niches run $20–$38 and occasionally above $50.", body),
    Paragraph("YouTube Shorts — the same platform, a fraction of the rate", h3),
    Paragraph(
        "Shorts are paid from a shared pool rather than per-video ad revenue, and the effective RPM is a "
        "small fraction of long-form. They are a distribution tool that feeds subscribers to your long-form "
        "catalogue. Treating Shorts as an income stream in themselves is one of the most common and "
        "expensive mistakes.", body),
    Paragraph("TikTok — good reach, modest pay, closed to Africa", h3),
    Paragraph(
        "The Creator Rewards Program pays roughly <b>$0.40–$1.20 per 1,000 views</b>, and requires 10,000 "
        "followers, 100,000 views in the previous 30 days, and videos over one minute. Reach is unmatched "
        "for a standing start — but the money is modest and the door is shut unless you live in one of about "
        "ten countries.", body),
    Paragraph("Facebook — the one most diaspora creators underestimate", h3),
    Paragraph(
        "Meta consolidated its programmes into a single <b>Content Monetization Program</b> in 2025, "
        "bundling in-stream ads, Reels ads, subscriptions, Stars and bonuses into one payout. Rates split "
        "sharply by format: <b>Reels typically return $0.02–$0.20 per 1,000 views</b>, while <b>longer video "
        "in high-CPM niches with a Western audience can reach $1–$4</b>. Facebook deserves more attention "
        "from diaspora creators than it gets, for an unglamorous reason: <b>it is still where the older "
        "African audience is</b>, at home and abroad. Diaspora community groups, church networks, hometown "
        "associations and market pages remain overwhelmingly Facebook-native.", body),
    Paragraph("Instagram — no ad share, and that is the whole story", h3),
    Paragraph(
        "Instagram Reels carries <b>no direct ad-revenue share</b>. Creator income comes through invite-only "
        "bonus programmes, brand deals, affiliate links and Shopping. Instagram is a superb audience-building "
        "and brand-deal shopfront and a non-existent ad-revenue business. Build there, earn elsewhere.", body),
    Paragraph("X / Twitter — effectively unpaid", h3),
    Paragraph(
        "Ads Revenue Sharing requires an X Premium subscription, a verified account, at least 500 followers "
        "and roughly 5 million impressions over three months. The payout is approximately <b>$8–$12 per "
        "million verified impressions</b>, weighted toward engagement from other Premium users rather than "
        "raw reach. Sources disagree on the exact volume needed to clear $1,000 a month, but they agree on "
        "the conclusion: <b>treat X ad revenue as a bonus, never as income.</b>", body),
    Paragraph("LinkedIn — pays nothing directly, and may still pay you best", h3),
    Paragraph(
        "LinkedIn has no creator ad-revenue programme at all. For a professional in the diaspora it is "
        "nonetheless frequently the highest-earning platform on this list, because it converts to consulting "
        "work, speaking fees, job offers and B2B clients — income that never appears in a creator-fund "
        "dashboard. If you are an accountant, engineer, nurse or founder, an hour on LinkedIn is very often "
        "worth more than an hour on TikTok.", body),
]

# ================= 05 =================
story += [
    Paragraph("05 · The Geography Multiplier", h2),
    Paragraph(
        "Now the part that changes strategy. <b>Your RPM is set by where your audience sits, not where you "
        "sit.</b>", body),
    fig("geography_rpm.png",
        "Fig 3 — YouTube RPM by audience location. The same video, the same effort, the same view "
        "count — ten to twenty times the money."),
    Paragraph(
        "One widely cited illustration: <b>100,000 views from a US audience might earn about $800; the same "
        "100,000 views from India, under $100</b>. African-audience RPMs are less well documented than "
        "India's but sit broadly in that lower band, for the same structural reason: advertiser demand and "
        "purchasing power, not audience quality.", body),
    Paragraph(
        "This produces an uncomfortable but important conclusion. <b>A channel about Africa, made for "
        "viewers in Africa, is the hardest possible way to earn from advertising.</b> Not because the "
        "audience is less valuable as people — because the ad market prices them lower.", body),
    Paragraph(
        "The diaspora sweet spot is content about the African experience, made for people living in the "
        "West. Same culture, same authority, ten times the ad rate.", pull),
    Paragraph(
        "This is not a call to abandon home audiences. It is a call to be deliberate about which of your "
        "formats is the <i>ad-funded</i> one. Diaspora-facing content — navigating visas, sending money "
        "home, raising children between cultures, African food in Western supermarkets, professional life as "
        "an immigrant — is watched in London, Toronto, Houston and Berlin, and priced accordingly. "
        "Home-facing content can then be monetised through direct payment, sponsorship or products instead.", body),
]

# ================= 06 =================
story += [
    Paragraph("06 · What $1,000 a Month Actually Takes", h2),
    Paragraph(
        "Rates in the abstract are hard to feel. The cover chart shows the same information as a workload, "
        "and the spread is the entire argument of this report. <b>100,000 views a month is a serious but "
        "achievable target</b> for a focused creator with a good niche — roughly 25,000 views a week, or one "
        "solid video. <b>Ten million monthly views is a full-time media operation.</b> One hundred million is "
        "a national broadcaster. All three of those numbers pay the same $1,000.", body),
    Paragraph(
        "Two things follow. First, <b>a diaspora creator who picks YouTube long-form with a Western audience "
        "is starting the race a hundred metres from the line while a Facebook Reels creator starts ten "
        "kilometres back.</b> Second, if you are already getting 300,000 monthly views on TikTok and earning "
        "a few hundred dollars, the problem is not your content. It is your platform.", body),

    Paragraph("07 · The 112-Person Shortcut", h2),
    Paragraph(
        "Everything above assumes you are paid by advertisers. There is a second model, and for most "
        "diaspora creators it is both faster and more reliable: <b>being paid directly by the people who "
        "value your work.</b>", body),
    fig("supporters_for_1000.png",
        "Fig 4 — Paying supporters needed for $1,000/month, after platform fees. Patreon's average "
        "pledge sits in the $7–$15 range across most categories.", max_w=150 * mm),
    Paragraph(
        "Put the two charts side by side. <b>You need 100,000 monthly YouTube views, or 112 people who pay "
        "you $10 a month.</b> For a diaspora creator, the 112 is usually the easier number. Your audience is "
        "not a general public — it is a specific group of people with a specific, expensive, poorly-served "
        "problem: how to move, how to stay legal, how to get credentials recognised, how to send money "
        "without losing 8% of it, how to raise children who understand where they came from. People pay for "
        "that. They scroll past entertainment.", body),
    Paragraph(
        "The ceiling is real too, not theoretical: Substack's top 500 creators average around <b>$840,000 a "
        "year</b> in subscription revenue, and Patreon's top 500 around <b>$620,000</b>. Those are the "
        "extreme top of the distribution and nobody should plan around them — but they establish that the "
        "model scales. <b>Substack suits writing and analysis</b>; <b>Patreon suits video, audio and "
        "community</b>. Both let you own the relationship, which is the part no algorithm can take away. "
        "A channel is rented. An email list is owned.", body),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · What the Platform Keeps", h2),
    fig("take_rate.png",
        "Fig 5 — Platform take rates. Patreon and Substack figures include roughly 3% payment "
        "processing on top of the headline plan fee.", max_w=155 * mm),
    Paragraph(
        "YouTube keeps <b>45%</b> of long-form ad revenue — the highest cut on this chart by a wide margin. "
        "Substack takes a flat 10% plus processing; Patreon runs 5%, 8% or 12% by plan, plus processing. But "
        "a take rate is meaningless without a base. <b>45% of a large number beats 8% of nothing</b>, which "
        "is why YouTube still wins on absolute earnings for most creators with real reach.", body),
    Paragraph(
        "One practical note for diaspora creators specifically: <b>check that the payout rail reaches you "
        "before you build on a platform.</b> Programmes that pay via Stripe or direct bank transfer are "
        "straightforward from most Western countries and considerably more complicated from several African "
        "ones. This is another quiet advantage of a diaspora address, and another reason to be the family "
        "member who sets up the account.", body),
]

# ================= 09 =================
story += [
    Paragraph("09 · The Diaspora's Real Edge", h2),
    fig("scorecard.png",
        "Fig 6 — AGF's scorecard for a diaspora creator. A judgement built from the rates and "
        "eligibility above, not a measured index — the weighting is ours.", max_w=150 * mm),
]
story += bullets([
    "<b>You are eligible where home is not.</b> TikTok's programme, Meta's bonus schemes and most payment "
    "rails work from your address and not from Lagos or Nairobi. This is the most concrete advantage on the "
    "list, and it expires the moment those programmes expand — so it is worth using now.",
    "<b>Your audience is priced in hard currency.</b> Diaspora-facing content is watched from high-RPM "
    "markets. You get Western ad rates for African subject matter — a combination almost nobody else can "
    "offer credibly.",
    "<b>You have authority nobody can fake.</b> You have actually done the visa run, the credential "
    "conversion, the first winter, the awkward call home about money. Creators back home cannot make that "
    "content truthfully, and Western creators cannot make it at all.",
    "<b>Your audience has money and an expensive problem.</b> The diaspora spends on remittances, flights, "
    "visas, school fees and legal advice. That makes it commercially valuable to advertisers, and it makes "
    "people willing to pay directly for genuinely useful help.",
])
story += [Paragraph(
    "A Ghanaian nurse in Manchester explaining NMC registration to other African nurses is sitting on a "
    "higher-value audience than a general lifestyle channel with ten times the followers.", pull)]

# ================= 10 =================
story += [
    Paragraph("10 · What Doesn't Work", h2),
    Paragraph("An honest list, because most creator advice is written by people selling courses.", body),
]
story += bullets([
    "<b>Posting the same clip everywhere and hoping.</b> The rate difference between platforms is roughly "
    "1,000×. Cross-posting is fine as distribution; it is not a strategy.",
    "<b>Chasing followers instead of RPM.</b> A 50,000-follower Instagram account can earn less from the "
    "platform than a 2,000-subscriber YouTube channel in a finance niche.",
    "<b>Building your whole business on short-form.</b> Shorts, Reels and TikToks pay a fraction of "
    "long-form and stop earning almost immediately. They are the shop window, not the shop.",
    "<b>Waiting for brand deals.</b> They arrive after you have an audience with a clear identity, not "
    "before, and they are unpredictable income. Build a floor you control first.",
    "<b>VPNs and foreign accounts to fake eligibility.</b> Against platform terms; the usual penalty is "
    "permanent demonetisation and forfeited balance.",
    "<b>Assuming virality equals income.</b> Ten million Facebook Reels views is roughly $1,000. One "
    "well-targeted YouTube video with 100,000 views is the same money and it keeps earning next year.",
])

# ================= 11 =================
story += [
    Paragraph("11 · The Playbook", h2),
]
story += bullets([
    "<b>Pick one long-form home and one short-form feeder.</b> For almost every diaspora creator that is "
    "<b>YouTube long-form</b> as the home, plus TikTok or Reels as the feeder. The feeder builds reach; the "
    "home earns money and compounds.",
    "<b>Aim your ad-funded content at diaspora viewers, not home viewers.</b> Same expertise, same culture, "
    "roughly ten times the RPM. Serve the home audience too — just do not expect advertisers to pay you "
    "properly for it.",
    "<b>Choose the highest-value niche you can speak to honestly.</b> Money, immigration, careers, "
    "credentials, health and business carry the highest advertiser bids and the highest willingness to pay "
    "directly. If you have professional expertise, that is your niche — not a general vlog.",
    "<b>Open the direct-payment channel at 1,000 followers, not 100,000.</b> Substack for writing, Patreon "
    "for video and community. You need about 112 paying people, and small audiences convert better than "
    "large ones.",
    "<b>Use your eligibility while it is an advantage.</b> Get the TikTok and Meta monetisation accounts set "
    "up in your own name and location now. That advantage narrows every year these programmes expand.",
    "<b>If you are a professional, do not ignore LinkedIn.</b> It pays nothing per view and frequently "
    "out-earns everything else through consulting, speaking and clients.",
    "<b>Collect emails from day one.</b> Every platform here can change its rates or close its programme "
    "without warning — Meta shut down its Reels Play bonus in August 2025. An email list is the only asset "
    "here you actually own.",
    "<b>Track RPM, not views.</b> Look at earnings per 1,000 views monthly, per format and per audience "
    "country. It is the number that tells you what to make more of.",
])

# ================= 12 =================
story += [
    Paragraph("12 · Method &amp; Limits", h2),
    Paragraph(
        "<b>What this report is:</b> a comparison of published creator-monetisation rates and eligibility "
        "rules as at 11 August 2026, read specifically for someone from Africa living abroad.", body),
]
story += bullets([
    "<b>RPM figures are ranges, not guarantees.</b> Actual earnings vary enormously by niche, season "
    "(Q4 is always highest), audience country mix and format.",
    "<b>Published RPM data is mostly industry-aggregated, not audited.</b> Platforms do not publish "
    "per-country creator payout rates, so these come from analytics firms and creator-reported data. They "
    "are directionally reliable and individually imprecise.",
    "<b>Facebook rates vary by an order of magnitude</b> between Reels and long video, and sources conflict. "
    "We have given both bands rather than a single number.",
    "<b>X's payout basis has shifted</b> toward engagement from Premium users, so impression-based estimates "
    "are less reliable than they were. Sources disagree on what monthly volume yields $1,000; we have said "
    "so rather than pick one.",
    "<b>African-audience RPM is poorly documented.</b> We use India as the documented low-RPM comparator and "
    "say so, rather than publishing an African figure we cannot source.",
    "<b>Eligibility lists change.</b> TikTok has expanded its programme repeatedly. Verify current country "
    "availability before building a plan around it.",
    "<b>The Fig 6 scorecard is AGF's own judgement</b>, not a measured index.",
    "<b>The $1,000 calculations use rate midpoints</b> and exclude tax, equipment, software and time. They "
    "measure gross platform revenue, not profit.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Lenos and Fluxnote on YouTube CPM/RPM by country and niche; Creators Agency and Multilogin on "
        "TikTok Creator Rewards eligibility and rates; Fluxnote and Meta on the Content Monetization Program "
        "and Creator Fast Track; InfluencerFee on Instagram Reels; Influencer Marketing Hub and Kompozy on X "
        "Ads Revenue Sharing; SocialSeconds and Substack on subscription platform fees and creator earnings. "
        "Full inline links in the web edition.", small),
    Spacer(1, 6 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=8),
]
story += [callout(
    "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit together, "
    "and bounce ideas. This research is part of an open library, free to read and share. The Forum itself "
    "is by application.<br/><br/>"
    "Read the web edition with live source links: "
    "africaglobalforum.com/reports/diaspora-creator-income-2026<br/>"
    "Companion reports: The Visa Treadmill · Where the Door Is Actually Open<br/>"
    "Apply to join: africaglobalforum.com", bg=INK)]

doc.build(story)
print("wrote", OUT)
