#!/usr/bin/env python3
"""Generate the AGF report PDF: The Music Is African. The Money Is Abroad. (2026)."""

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
IMG = os.path.join(HERE, "music-money-abroad-2026", "img")
OUT = os.path.join(HERE, "music-money-abroad-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Money Is Abroad · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 12 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Music Is African. The Money Is Abroad. (2026)",
                      author="Africa Global Forum",
                      subject="Where African musicians income actually comes from, and why it is the diaspora")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])

story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Music Is African.", h1),
    Paragraph("The money is abroad.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Spotify pays <b>$300</b> for a million streams in Nigeria and <b>$10,000</b> for a million in "
        "Sweden. Which means the diaspora is not Afrobeats' audience. It is Afrobeats' "
        "<i>business model</i> — and almost nobody says so out loud.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("33×", big_num), Paragraph("$0.85", big_num),
    Paragraph("$44.3m", big_num), Paragraph("58%", big_num),
], [
    Paragraph("gap between a Swedish<br/>stream and a Nigerian one", big_lbl),
    Paragraph("a month for Spotify Premium<br/>in Nigeria — cheapest<br/>in the world", big_lbl),
    Paragraph("paid to Nigerian artists by<br/>one platform in 2025", big_lbl),
    Paragraph("of it went to independent<br/>artists and labels", big_lbl),
]], colWidths=[CONTENT_W / 4] * 4)
kpi.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), INK),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 14),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story += [kpi, Spacer(1, 6 * mm)]
story += [fig("per_million.png",
              "Fig 1 — Approximate Spotify payout per million streams, by where the listener is "
              "(Chartlex, 2026). Rates are estimates — Spotify does not publish per-country rates.")]
story += [Paragraph(
    "Published August 2026 by Africa Global Forum · "
    "africaglobalforum.com/reports/music-money-abroad-2026", small), PageBreak()]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Afrobeats and amapiano are the biggest cultural export Africa has produced in a generation. The "
        "music is made in Lagos, Accra and Johannesburg. <b>The revenue is overwhelmingly generated "
        "somewhere else</b> — and mostly by Africans and their descendants living abroad, plus the "
        "non-African audiences the diaspora introduced the music to.", body),
]
story += bullets([
    "<b>A stream is not a stream.</b> Spotify pays roughly <b>$300 per million streams in Nigeria</b> and "
    "<b>$10,000 per million in Sweden</b> — a <b>33-fold gap</b>. The US sits around $3,500.",
    "<b>The reason is the subscription price, not prejudice.</b> Spotify Premium costs about <b>$0.85 a "
    "month in Nigeria</b> — the cheapest in the world — against <b>$12.77 in Sweden</b>. Smaller pot, "
    "thinner slices.",
    "<b>Nigerian artists earned more from one platform than their entire domestic market is worth.</b> "
    "Spotify paid over <b>NGN 60 billion (~$44.3m)</b> to Nigerian artists in 2025. All of Sub-Saharan "
    "Africa's tracked recorded-music revenue that year was <b>$120m</b>, of which Nigeria was <b>under "
    "$26m</b>.",
    "<b>30.3 billion streams</b> of Nigerian music on Spotify in 2025, 1.6 billion listening hours, and "
    "<b>1.3 billion first-time discoveries</b>, up 26% year on year.",
    "<b>58% of those royalties went to independent artists and labels</b> — a genuinely unusual figure for "
    "any music market.",
    "<b>And the live economy is almost entirely a diaspora economy.</b> Burna Boy became the first African "
    "artist to sell out a UK stadium — 60,000 at London Stadium. Wizkid sold out the 20,000-capacity O2 in "
    "twelve minutes and headlined Madison Square Garden. Those are diaspora cities.",
])
story += [Paragraph(
    "Every African artist who “made it” made it on foreign money. That is not a criticism of the "
    "artists. It is a description of where the industry's cash actually sits — and a problem the continent "
    "has not solved.", pull)]

# ================= 02 =================
story += [
    Paragraph("02 · Not All Streams Are Equal", h2),
    Paragraph(
        "An artist in Lagos with a million plays from Nigerian listeners has earned roughly <b>$300</b> "
        "(see cover chart). The same million plays from Swedish listeners is roughly <b>$10,000</b>. "
        "Per-stream, that is about <b>$0.0005 in low-income markets against $0.008 in Norway and "
        "Sweden</b>.", body),
    Paragraph(
        "Here is the arithmetic that makes the whole report click. Spotify paid Nigerian artists about "
        "<b>$44.3 million</b> across <b>30.3 billion streams</b> in 2025. Divide: an average of roughly "
        "<b>$1.46 per thousand streams</b> — nearly <b>five times the local Nigerian rate</b> of about "
        "$0.30 per thousand.", body),
    Paragraph(
        "If Nigerian artists were mostly being played by Nigerians, that average would sit near the "
        "Nigerian rate. It sits five times above it. The listeners paying the bills are overseas.", pull),

    Paragraph("03 · Why — The $0.85 Subscription", h2),
    Paragraph(
        "It would be easy to read the cover chart as discrimination. It is not. It is arithmetic, and "
        "understanding the mechanism matters because it tells you what can and cannot be fixed.", body),
    fig("subscription.png",
        "Fig 2 — Spotify Premium monthly subscription price. Nigeria is the cheapest market in the "
        "world (Pulse; TechCabal)."),
    Paragraph(
        "Streaming royalties are paid from a <i>pool</i>. Each country's pool is essentially what "
        "subscribers in that country paid in, minus the platform's cut, divided among the artists they "
        "listened to. <b>A Nigerian subscriber contributes about $0.85 a month. A Swedish subscriber "
        "contributes $12.77.</b> Fifteen times the money into the pot produces roughly fifteen to thirty "
        "times the money out.", body),
]
story += bullets([
    "<b>Free-tier dominance.</b> In comparable markets more than 80% of users are on the ad-supported free "
    "tier, and ad revenue per listener in Nigeria is a fraction of the subscription equivalent.",
    "<b>ARPU.</b> Average revenue per user sits below about $1.40 a month in many developing markets, "
    "against several times that in North America and Western Europe.",
])
story += [Paragraph(
    "The practical consequence for an artist is uncomfortable but clear: <b>growing your Nigerian audience "
    "grows your fame. Growing your diaspora and Western audience grows your income.</b> They are not the "
    "same project, and conflating them has cost a lot of artists a lot of money.", body)]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · What $1,000 Takes", h2),
    fig("streams_for_1000.png",
        "Fig 3 — Streams needed to earn $1,000, derived from the per-million rates in Fig 1. Gross of "
        "any label, distributor or management share."),
    Paragraph(
        "<b>3.33 million Nigerian streams, or 100,000 Swedish ones.</b> Same thousand dollars.", body),
    Paragraph(
        "Put that beside the streaming economics in our creator income report and the same law appears in a "
        "second industry: <b>where your audience sits determines your income far more than how big it "
        "is.</b> For a video creator the spread was about 1,000-fold across platforms. For a musician it is "
        "33-fold across borders — on the same platform, for the same song, on the same day.", body),
    Paragraph(
        "And note what these numbers are <i>before</i>: this is gross. A signed artist may see anywhere "
        "from a small fraction to about half after the label, distributor, publisher and manager have taken "
        "their positions. The 3.33 million figure is the optimistic version.", body),

    Paragraph("05 · The Market That Isn't There", h2),
    fig("market_vs_payout.png",
        "Fig 4 — Tracked recorded-music revenue against a single platform's payout to Nigerian "
        "artists. Note these measure different things — see Method."),
    Paragraph(
        "Sub-Saharan Africa's tracked recorded-music revenue grew 15.2% in 2025 to <b>$120 million</b>. "
        "<b>South Africa took 78% of it ($93.7m)</b>, on the strength of a mature collections infrastructure "
        "and higher subscription prices. <b>Nigeria — 220 million people and the most culturally dominant "
        "music scene on the continent — accounts for under $26 million of tracked revenue.</b> And Spotify "
        "alone paid Nigerian artists about <b>$44.3 million</b>.", body),
    Paragraph(
        "These two figures measure different things — one is revenue collected <i>inside</i> a territory, "
        "the other is money paid <i>to</i> artists of a nationality from listeners everywhere. But holding "
        "them side by side is exactly the point: <b>the money attached to Nigerian music is not in "
        "Nigeria.</b> It is generated abroad, paid in hard currency, and lands in the accounts of whoever "
        "controls the rights.", body),
    Paragraph(
        "Nigeria has the audience, the talent and the culture. South Africa has the collection society. "
        "Guess which one has 78% of the continent's recorded-music revenue.", pull),
    Paragraph(
        "That is a fixable problem, and it is worth naming plainly: the gap is <b>infrastructure</b> — "
        "royalty collection, rights registration, publishing administration and enforcement. Music that is "
        "not registered properly does not get paid, no matter how many times it is played.", body),
]

# ================= 06 =================
story += [
    Paragraph("06 · The Live Economy", h2),
    Paragraph(
        "Streaming gets the headlines. <b>Live performance is where the diaspora actually hands over "
        "money</b>, and it does so at Western ticket prices.", body),
    fig("venues.png",
        "Fig 5 — Milestone venues for African artists abroad. All three sit in cities with among the "
        "densest African diaspora populations in the world."),
    Paragraph(
        "<b>Burna Boy became the first African artist to sell out a UK stadium</b>, playing to 60,000 at "
        "London Stadium on the <i>Love, Damini</i> tour. <b>Wizkid sold out the 20,000-capacity O2 Arena in "
        "twelve minutes</b>, then added nights that also sold out in under ten — and became the first "
        "Nigerian artist to headline Madison Square Garden.", body),
    Paragraph(
        "Look at the map rather than the milestones. London, New York, Toronto, Houston, Atlanta, Paris, "
        "Amsterdam. <b>The tour routing of a successful African artist is, almost exactly, a map of the "
        "African diaspora.</b> Afro Nation — whose 2026 Portugal edition is headlined by Burna Boy, Asake, "
        "Wizkid and Tyla — is a festival built in Europe for an audience that is substantially diaspora and "
        "diaspora-adjacent.", body),
]
story += bullets([
    "<b>Ticket prices track the local economy, not the artist's.</b> A London ticket is priced in pounds "
    "against London wages.",
    "<b>The artist keeps a much larger share</b> of live revenue than of recorded revenue, where labels and "
    "distributors sit in the middle.",
    "<b>It is not subject to the pool problem.</b> Nobody divides your gate receipts by a national ARPU.",
    "<b>Merchandise attaches to it</b>, at full Western retail.",
])
story += [Paragraph(
    "Which is why the sequence for a serious African artist is now well established: build the streaming "
    "numbers to prove demand, then <b>monetise that demand on a stage in a diaspora city.</b>", body)]

# ================= 07 =================
story += [
    Paragraph("07 · Who Actually Gets Paid", h2),
    Paragraph(
        "One genuinely encouraging finding: <b>58% of the royalties Nigerian artists earned on Spotify in "
        "2025 went to independent artists or labels</b>, not the majors. That is a high independent share "
        "by global standards, and it reflects something real about how Afrobeats grew — through "
        "distribution deals, self-releases and regional labels rather than a traditional major-label "
        "pipeline.", body),
    Paragraph("But the chain still has several hands in it, and each takes a cut before the artist sees "
              "anything:", body),
]
story += bullets([
    "<b>The platform</b> keeps its share before the pool is divided.",
    "<b>The distributor or label</b> takes a percentage — small for a pure distribution deal, very large "
    "for a traditional record deal.",
    "<b>Publishing</b> is a separate revenue stream from the recording, and is the one most commonly left "
    "uncollected by African artists. <b>Unregistered publishing is money sitting in a pot with your name "
    "not on it.</b>",
    "<b>Management, booking agents and producers</b> take their positions on top.",
])
story += [Paragraph(
    "The single most valuable administrative act available to an African artist is the same one available "
    "to an African professional abroad: <b>register the paperwork properly, early, before the money starts "
    "arriving.</b> It is boring, it is cheap, and it is worth more than any amount of promotion.", body)]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · Where the Growth Goes Next", h2),
    fig("growth.png",
        "Fig 6 — Where Afrobeats listening is growing fastest. Indonesia is over five years; Latin "
        "America and Brazil since 2020."),
    Paragraph(
        "The diaspora opened the door. The next wave is walking through it without any diaspora connection "
        "at all: <b>Latin America up more than 400% since 2020, Brazil up 500%, Indonesia up 4,530% over "
        "five years.</b> France, the Netherlands and Mexico are all growing quickly.", body),
    Paragraph(
        "This matters commercially in a specific way. <b>Some of these are high-ARPU markets and some are "
        "not.</b> Growth in France and the Netherlands converts to real money; growth in Indonesia produces "
        "enormous stream counts and modest royalties, for exactly the reasons in Section 03. A rational "
        "artist reads growth charts and revenue charts as two different documents.", body),
    Paragraph(
        "The diaspora's role also changes at this point. For fifteen years it was the <i>audience</i>. It "
        "is now increasingly the <i>bridge</i> — the reason a Brazilian or Indonesian listener encountered "
        "the music at all. That is a less visible contribution and a more valuable one.", body),

    Paragraph("09 · If You Are an Artist", h2),
]
story += bullets([
    "<b>Know which country your streams come from, monthly.</b> Spotify for Artists shows you. A track "
    "doing 2 million plays in Nigeria and 200,000 in the US is earning most of its money from the smaller "
    "number. Most artists have never looked.",
    "<b>Register your publishing before you need to.</b> The recording and the composition are two "
    "different assets paid through two different systems. The second one is where African artists most "
    "often lose money quietly and permanently.",
    "<b>Treat the diaspora city as the revenue event.</b> Streaming proves demand; a show in London, "
    "Houston or Toronto converts it. Route tours by diaspora density, not by fantasy.",
    "<b>Take distribution over a traditional deal if you can survive the wait.</b> The 58% independent "
    "share is not an accident — it is the whole reason Afrobeats built more artist-side wealth than earlier "
    "African music waves.",
    "<b>Do not read stream counts as income.</b> Indonesia at +4,530% is a wonderful cultural fact and a "
    "modest financial one.",
    "<b>Price the home market as marketing, not revenue.</b> A Lagos show and a Lagos stream build the "
    "thing that gets paid for elsewhere.",
])

# ================= 10 =================
story += [
    Paragraph("10 · If You Are a Fan Abroad", h2),
    Paragraph(
        "The diaspora already funds this industry. It could do so more deliberately, and the mechanics are "
        "worth knowing because they are not intuitive.", body),
]
story += bullets([
    "<b>Your paid subscription is worth roughly fifteen Nigerian ones</b> to the artists you listen to. If "
    "you are streaming African music on a free tier in a high-ARPU country, upgrading is one of the "
    "highest-leverage things you can do for the artists you love.",
    "<b>Buying a ticket beats streaming an album a thousand times.</b> A single £60 ticket delivers more to "
    "the artist than hundreds of thousands of streams from a low-ARPU market.",
    "<b>Merchandise and direct-to-fan beat both.</b> No pool, no split, no territory rate.",
    "<b>Streaming in your own country, on your own account, matters.</b> It is your national pool the money "
    "comes from.",
    "<b>If you invest, the infrastructure is the opportunity, not the artists.</b> The gap in Fig 4 is a "
    "collections and rights-administration gap. That is a business, and it is under-built across most of "
    "the continent.",
])

# ================= 11 =================
story += [
    PageBreak(),
    Paragraph("11 · The Uncomfortable Part", h2),
    Paragraph("Three things worth saying plainly, because the celebration around Afrobeats tends to skip "
              "them.", body),
    Paragraph(
        "<b>First, the dependency is real.</b> An industry whose revenue is overwhelmingly foreign is "
        "exposed to foreign taste. Afrobeats is currently fashionable in the West. Genres stop being "
        "fashionable. A domestic market that cannot pay its own artists is a fragile foundation, however "
        "loud the moment.", body),
    Paragraph(
        "<b>Second, the value is captured off the continent.</b> The platforms are American and Swedish, "
        "the major labels are American, Japanese and French, the biggest venues and festivals are European "
        "and American, and the management and booking infrastructure has largely followed the money abroad. "
        "African music is a growth industry whose profit centres are mostly not African.", body),
    Paragraph(
        "<b>Third, and most importantly: none of this is the artists' fault, and the fix is not "
        "artistic.</b> No amount of “support local” solves a $0.85 subscription price against a $12.77 one. "
        "The binding constraints are purchasing power, payment infrastructure, premium conversion and "
        "rights collection. Those are policy and business problems.", body),
    Paragraph(
        "South Africa is 78% of the continent's tracked recorded-music revenue not because it makes 78% of "
        "the music, but because it built the machinery that counts and collects. That is the whole "
        "lesson.", pull),
]

# ================= 12 =================
story += [
    Paragraph("12 · Method &amp; Limits", h2),
    Paragraph(
        "<b>What this report is:</b> an assembly of published streaming, royalty and market figures as at "
        "12 August 2026, read for what they say about where African musicians' income originates.", body),
]
story += bullets([
    "<b>Per-country payout rates are estimates, not published figures.</b> Spotify does not disclose "
    "per-country per-stream rates; the numbers in Fig 1 and Fig 3 come from industry analysis and "
    "creator-reported data. Treat them as bands, not precise prices.",
    "<b>Fig 4 compares two different measures.</b> Tracked recorded-music revenue is collected <i>within</i> "
    "a territory; the Spotify payout is money paid <i>to</i> artists of a nationality from listeners "
    "worldwide. They cannot be summed or subtracted. We place them together deliberately, and the "
    "comparison is directional.",
    "<b>Widely-circulated claims that Nigeria's music industry is worth $2 billion, or that its "
    "recorded-music market was $1.8 billion in 2023, cannot be reconciled</b> with tracked revenue of under "
    "$26 million. Those larger figures appear to capture something else entirely — informal economy, live, "
    "broadcast and adjacent sectors, or simply an error propagating between sources. We have used the "
    "tracked figures and flagged the conflict rather than pick the flattering number.",
    "<b>The $1.46 per thousand streams average is our own arithmetic</b> from two published figures "
    "(NGN 60bn+ royalties over 30.3bn streams), converted at approximately NGN 1,355 to the dollar. Naira "
    "conversions move materially with the exchange rate.",
    "<b>Nothing here measures live revenue directly.</b> Venue capacities are documented; gate receipts, "
    "guarantees and artist splits are not public. The live section is qualitative about magnitudes.",
    "<b>“African music” here leans heavily Nigerian</b>, because Nigeria publishes the most usable data. "
    "Amapiano, Francophone African music, North African and East African scenes have different economics "
    "that this report does not separate out.",
    "<b>Royalty figures are gross to rights-holders</b>, not net to artists. What an individual musician "
    "receives depends entirely on their contracts.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Spotify Loud &amp; Clear reporting via Arise and Africa.com; Chartlex and Beats &amp; Business on "
        "per-country royalty rates; TechCabal on Nigeria's streaming economy and ARPU; Pulse on "
        "subscription pricing; The Freeme Space on Sub-Saharan tracked revenue and the Nigeria collections "
        "gap; AllAfrica on stadium and arena milestones; Punch on Afro Nation 2026. Full inline links in "
        "the web edition.", small),
    Spacer(1, 6 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=8),
]
story += [callout(
    "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit together, "
    "and bounce ideas. This research is part of an open library, free to read and share. The Forum itself "
    "is by application.<br/><br/>"
    "Read the web edition with live source links: "
    "africaglobalforum.com/reports/music-money-abroad-2026<br/>"
    "Companion reports: Your Address Pays Better Than Your Following · How Long Until It Was Worth It?<br/>"
    "Apply to join: africaglobalforum.com", bg=INK)]

doc.build(story)
print("wrote", OUT)
