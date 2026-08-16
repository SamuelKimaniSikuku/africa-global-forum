#!/usr/bin/env python3
"""Generate the AGF report PDF: The Visa Treadmill — What It Costs to Stay Legal (2026)."""

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
IMG = os.path.join(HERE, "who-pays-for-african-music-2026", "img")
OUT = os.path.join(HERE, "who-pays-for-african-music-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "Where Africa Is Heard · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 15 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="Twenty Countries Listen. Four of Them Pay. (2026)",
                      author="Africa Global Forum",
                      subject="Where African music is heard outside Africa, and which countries actually pay for it")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("Twenty Countries Listen.", h1),
    Paragraph("Four of them pay.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "One Afrobeats single is certified in more than <b>twenty countries</b> — 5 million units in "
        "the United States, <b>1.56 million in India</b>, Diamond in Poland, number one in the "
        "Netherlands. African music is heard almost everywhere. It is <i>paid for</i> in about four "
        "places, and that gap is the whole story.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("22", big_num), Paragraph("1.56m", big_num),
    Paragraph("8", big_num), Paragraph("4.4×", big_num),
], [
    Paragraph("countries where one African<br/>song is certified", big_lbl),
    Paragraph("certified units in India —<br/>the third-biggest<br/>market for it", big_lbl),
    Paragraph("countries where it went<br/>to number one", big_lbl),
    Paragraph("what one British stream<br/>is worth in Brazilian ones", big_lbl),
]], colWidths=[CONTENT_W / 4] * 4)
kpi.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), INK),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, 0), 12), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 12),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story += [kpi, Spacer(1, 6 * mm)]

story += [
    fig("where_listened.png",
        "Fig 1 — Certified units by country for Rema's “Calm Down”, the most certified African "
        "record ever made. Log scale — each gridline is ten times the last.",
        max_h=150 * mm),
    Paragraph("Published August 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/who-pays-for-african-music-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Our previous report established <i>that</i> the money behind African music is abroad. This "
        "one asks the obvious follow-up: <b>abroad where?</b> The answer depends on which question "
        "you are actually asking, and the four sensible questions give four different league tables.",
        body),
]
story += bullets([
    "<b>African music is heard in at least twenty-two countries outside Africa at certified scale.</b> "
    "One song — Rema's “Calm Down”, ~1.89bn streams — is certified from 5 million units in the "
    "United States and 1.8 million in the UK to 1.56 million in India, Diamond in Poland, Canada, "
    "France and Brazil, and Platinum across Germany, Italy, Spain, Australia, New Zealand, Portugal, "
    "Belgium, Switzerland, Denmark, Norway, the Netherlands and Austria.",
    "<b>It has been number one in eight countries</b> — the Netherlands, Belgium, Switzerland, "
    "Portugal, Luxembourg, Canada, South Africa and on Romanian airplay — and number one on "
    "Billboard's Global Excl. US chart.",
    "<b>India is the third-largest market by certified units</b>, ahead of Canada, Germany and "
    "France. Poland went Diamond. Neither has an African migration story to explain it.",
    "<b>By new listeners</b>, the top five are the United States, Brazil, France, the United Kingdom and "
    "Germany — in that order — on Spotify's 2025 ranking of where Afrobeats gained the most new "
    "listeners. Nigeria is sixth. Afrobeats listeners grew 22% globally in a year.",
    "<b>By money, the order changes completely.</b> Estimated per-stream payouts run from about "
    "$0.0080 in Iceland and $0.0078 in Norway down to $0.0010 in Brazil and $0.0008 in India. "
    "Britain, at about $0.0044, leads the big markets.",
    "<b>One British stream is worth about 4.4 Brazilian ones.</b> Brazil ranks second by listeners "
    "and roughly eleventh by what those listeners are worth.",
    "<b>By diaspora, the map moves again.</b> Of the 20.7 million Africans living outside Africa, "
    "Europe holds about 11 million, Asia including the Gulf about 6.9 million, and Northern America "
    "only about 2.7 million.",
    "<b>The Gulf is the blind spot.</b> Nearly seven million Africans live in Asia and the Gulf, and "
    "that region is almost entirely absent from the African-music economy.",
    "<b>By live revenue it is Britain first, and it is not close.</b> A UK stadium at 60,000, a UK "
    "arena that sold out in twelve minutes, a Portuguese beach festival drawing 40,000 people from "
    "180 countries, and Madison Square Garden.",
    "<b>The growth frontier pays badly.</b> Indonesia (+4,530%), India (+1,650%), Brazil (+500%) and "
    "Latin America (+400%) are the fastest-growing markets — and every one is a bottom-tier payout "
    "market.",
])
story += [
    Paragraph("The countries that listen to African music and the countries that pay for it are two "
              "different lists, and the gap between them is the whole story.", pull),
]

# ================= 02 =================
story += [
    Paragraph("02 · Four Questions, Four Maps", h2),
    Paragraph("&ldquo;Which countries support African music?&rdquo; sounds like one question. It is "
              "four, and they have genuinely different answers:", body),
]
story += bullets([
    "<b>Who listens?</b> Raw audience. The number that gets quoted in press releases, and the least "
    "connected to income.",
    "<b>Who pays?</b> Payout per stream, set by that country's subscription price and premium "
    "penetration — not by how much anyone there loves the music.",
    "<b>Who shows up?</b> The live circuit. Where the diaspora is dense enough, and rich enough, to "
    "fill a room at Western ticket prices.",
    "<b>Who is actually there?</b> Where Africans abroad live — which is not the same as where the "
    "industry has built anything.",
])
story += [
    Paragraph("Confusing these four is the most common and most expensive mistake in African music "
              "commentary. A country can be first on one list and eleventh on another.", body),
]

# ================= 03 & 04 (new) =================
story += [
    PageBreak(),
    Paragraph("03 · Where It Is Actually Heard", h2),
    Paragraph(
        "Start with the question you actually asked: <b>where is African music listened to?</b> "
        "Streaming platforms do not publish country-level listener counts, so the honest way to "
        "answer it is with the one measure that <i>is</i> audited and published country by country — "
        "industry certifications.", body),
    Paragraph(
        "We use Rema's “Calm Down” as the measuring stick. It is the most globally successful African "
        "song ever recorded — roughly <b>1.89 billion streams worldwide</b> — and it is certified in "
        "more than twenty countries. Every number in Fig 1 on the cover was independently verified by "
        "a national industry body. Read down that list and the answer to “where is African music "
        "listened to?” stops being <i>the UK and America</i> and becomes something much wider:", body),
]
story += bullets([
    "<b>The United States is first</b> at 5 million certified units, and <b>the United Kingdom "
    "second</b> at 1.8 million. No surprise so far.",
    "<b>India is third</b> — 1.56 million units, certified 13× Platinum. It is ahead of Canada, "
    "Germany, France, Italy and Spain. Almost nobody discussing Afrobeats markets mentions India.",
    "<b>Continental Europe is thick with it.</b> Germany 600k, France 333k, Italy 300k, Spain 240k, "
    "plus Belgium, Switzerland, Austria, Denmark, Norway, the Netherlands and Portugal.",
    "<b>Poland took Diamond</b> at 250,000 units — more than Spain, more than Nigeria.",
    "<b>Australia and New Zealand</b> together account for 680,000 units. The Pacific is a real "
    "African-music market and it appears in none of the usual commentary.",
    "<b>Nigeria is eleventh</b> at 200,000 units — below Poland, above Brazil. The country that made "
    "the song certifies a twenty-fifth of what America does.",
])
story += [
    Paragraph("African music is not heard in a handful of diaspora capitals. On the evidence of the "
              "biggest African song ever made, it is heard in at least twenty-two countries across "
              "five continents — and the third-largest of them is India.", pull),
    Paragraph(
        "Two honest caveats before you over-read this. Certification thresholds differ between "
        "countries, so units measure <i>absolute consumption</i>, not popularity relative to a "
        "country's size — 40,000 units in the Netherlands is a far higher per-head figure than "
        "250,000 in Poland. And this is one song, whose remix featured Selena Gomez, which certainly "
        "inflated the American, Canadian and Australian numbers.", body),
]

story += [
    PageBreak(),
    Paragraph("04 · The Places Nobody Expects", h2),
    Paragraph(
        "Certified volume is one signal. Reaching <b>number one</b> is a different and in some ways "
        "better one, because it measures a song beating everything else in that country in the same "
        "week — a like-for-like contest against the local market.", body),
    fig("number_ones.png",
        "Fig 2 — Countries where “Calm Down” or its remix reached number one, plus the Billboard "
        "Global Excl. US chart. Romania is an airplay chart; the rest are national singles charts."),
    Paragraph(
        "An African song has topped the national chart in the <b>Netherlands, Belgium, Switzerland, "
        "Portugal, Luxembourg, Canada and South Africa</b>, led <b>Romanian airplay</b>, and reached "
        "number one on <b>Billboard's Global Excl. US</b> chart — which is to say it was, for a "
        "period, the biggest song in the world outside America.", body),
    Paragraph(
        "It reached number two in <b>France</b> and number two in <b>Lebanon</b>. It went Gold in "
        "<b>Chile</b> on 10 million streams and Platinum in <b>Greece</b> on 2 million. These are not "
        "diaspora markets in any meaningful sense. There is no significant Nigerian community in "
        "Bucharest or Santiago.", body),
    Paragraph(
        "That matters for how you think about the whole question. The story of the last decade was "
        "<i>the diaspora carried African music abroad</i>, and that is true. But the evidence here "
        "shows a second stage that has already happened: <b>the music has detached from the diaspora "
        "and is now travelling on its own.</b> Poland, Romania, Chile, Greece, India, Indonesia and "
        "Thailand have no African migration story to explain their numbers. They just liked the song.",
        body),
    Paragraph(
        "The Netherlands is the sharpest illustration of why a listening map and a revenue map are "
        "different documents. It is a <i>number one country</i> — the song topped both Dutch charts — "
        "and it sits at the bottom of Fig 1 on certified units, because it is a small country. "
        "Popular, not large. Both facts are true and they answer different questions.", body),
]

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("05 · Where the New Listeners Are Coming From", h2),
    fig("listener_rank.png",
        "Fig 3 — Spotify's 2025 ranking of the countries gaining the most new Afrobeats listeners. "
        "Spotify published the order without magnitudes, which is why this is drawn as a ladder."),
    Paragraph(
        "The <b>United States</b> leads — the largest single audience, the arena circuit, the award "
        "infrastructure. <b>Brazil</b> is second, and that is the genuinely surprising entry: deep "
        "Yoruba cultural roots, no significant recent African migration, and Afrobeats streams up "
        "roughly 500% since 2020. <b>France</b> is third, driven by collaborations with Dadju, Tayc "
        "and Tiakola and by the largest African-descended population in continental Europe. "
        "<b>Britain</b> is fourth and <b>Germany</b> fifth.", body),
    Paragraph(
        "Note what is not here. No Gulf state. No Canada. No Netherlands. And Nigeria — the country "
        "that makes the music — is sixth on a ranking of where its own genre is finding new ears.",
        body),
    Paragraph(
        "Britain sitting fourth deserves a caveat that runs the other way. The UK is not a growth "
        "market for Afrobeats the way Brazil is, because <i>it converted years ago</i>. It has had "
        "its own weekly Official Afrobeats Chart since July 2020. Growth rankings systematically "
        "flatter new markets and understate mature ones, which is exactly why you cannot read this "
        "chart as a support ranking.", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("06 · Where the Money Is", h2),
    Paragraph(
        "This is the ranking that decides who eats. It is set by two things, neither cultural: what a "
        "subscription costs in that country, and what share of listeners pay for one rather than "
        "using the free tier. Three things stand out.", body),
    fig("rate_ladder.png",
        "Fig 4 — Estimated Spotify payout per stream by listener country (Chartlex, 2026). Rates "
        "are estimates — Spotify does not publish per-country rates.", max_h=140 * mm),
]
story += bullets([
    "<b>Britain leads the major markets at about $0.0044</b> — ahead of Germany, Canada, Australia, "
    "the United States and France. The US has the bigger audience; the UK has the better rate.",
    "<b>The Nordics are in a league of their own.</b> Iceland and Norway pay roughly twice what "
    "Britain pays and about eight times what Brazil pays. They are tiny markets that behave like "
    "large ones because almost everyone in them subscribes.",
    "<b>The entire bottom of the table is where the growth is.</b> Brazil, Indonesia and India — the "
    "three fastest-expanding audiences for African music — sit at $0.0010, $0.0010 and $0.0008.",
])
story += [
    Paragraph(
        "These are estimates, and it matters that you know that. Spotify does not publish per-country "
        "rates. See Method &amp; Limits, where we also correct a figure we published three days ago.",
        body),
]

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("07 · The Exchange Rate Between Countries", h2),
    fig("exchange_rate.png",
        "Fig 5 — The same figures as Fig 4, expressed as an exchange rate. Derived by dividing each "
        "country's estimated rate by Brazil's."),
    Paragraph(
        "Divide any country's rate by Brazil's and you get something more useful than a decimal with "
        "four zeros in it: a currency conversion between audiences.", body),
    Paragraph(
        "<b>One Norwegian stream is worth 7.8 Brazilian ones. One British stream is worth 4.4.</b> An "
        "artist with a million Brazilian streams and 230,000 British ones is earning roughly the same "
        "amount from each — and will spend the whole year being congratulated about Brazil.", body),
    Paragraph("A million streams is not a fact about your income. It is a fact about your fame. The "
              "invoice depends on which passports those listeners hold.", pull),
    Paragraph(
        "This is also the honest way to read a Spotify for Artists dashboard. The map of listener "
        "countries is not a map of revenue; it is a map that has to be weighted before it means "
        "anything. Very few artists do the weighting.", body),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("08 · The Two Leagues", h2),
    fig("two_leagues.png",
        "Fig 6 — The top five growth markets plotted against what a stream from each is worth. Four "
        "are in one league; Brazil is in another."),
    Paragraph(
        "Put the two rankings on one chart and the structure of the whole export market appears. Four "
        "of the top five markets — the US, France, the UK and Germany — are clustered tightly between "
        "$0.0037 and $0.0044. They are, financially, near-interchangeable. Brazil sits by itself at a "
        "quarter of the rate.", body),
    Paragraph(
        "The tight cluster has a strategic implication that runs against instinct. If the US, UK, "
        "France and Germany all pay within about 15% of each other, then <b>choosing between them on "
        "royalty rate is pointless</b>. Choose on everything else: which one has the diaspora density "
        "to fill a venue, which has the radio and playlist infrastructure, which gives you a visa. "
        "The money is a wash; the platform is not.", body),
    Paragraph(
        "And Brazil's position is not a criticism of Brazil. Brazilian listeners are not paying less "
        "because they care less — they are paying less because Spotify charges them less, for "
        "entirely defensible reasons of purchasing power. The problem is not Brazilian fans. It is "
        "that an artist reading a stream count cannot see the difference, and nothing in the "
        "interface tells them.", body),
]

# ================= 07 =================
story += [
    Paragraph("09 · Where the Diaspora Actually Lives", h2),
    fig("diaspora_where.png",
        "Fig 7 — The 20.7 million Africans living outside the continent, by region. From our report "
        "The Diaspora, Counted."),
    Paragraph(
        "Now overlay the people. <b>Europe holds more than half of the African diaspora</b> — roughly "
        "11 million against Northern America's 2.7 million. The American cultural dominance of "
        "Afrobeats discourse is not proportionate to how many Africans actually live in America.",
        body),
    Paragraph(
        "This explains several things at once. It explains why Britain and France punch so hard: high "
        "payout rates <i>and</i> dense African populations in the same cities. It explains why Afro "
        "Nation is in Portugal rather than Florida — a European festival serving a European diaspora "
        "that can drive or take a budget flight to the Algarve. And it explains why Germany, fifth by "
        "listeners, is the market most people underrate.", body),
    Paragraph("Nearly seven million Africans live in Asia and the Gulf. There is no Gulf Afrobeats "
              "chart, no Gulf festival circuit, and no Gulf entry anywhere in the payout tables. That "
              "is the largest unserved African music audience in the world.", pull),
    Paragraph(
        "We flag this carefully rather than overclaim it. Gulf states are largely low-payout streaming "
        "markets with restrictive live-events regimes and a migrant population on temporary contracts "
        "with limited discretionary income. There are real reasons the industry has not gone there. "
        "But &ldquo;there are reasons&rdquo; and &ldquo;there is no opportunity&rdquo; are different "
        "statements, and a third of the diaspora is currently served by neither the recorded nor the "
        "live economy.", body),
]

# ================= 08 =================
story += [
    Paragraph("10 · The Live Circuit", h2),
    fig("live_circuit.png",
        "Fig 8 — Documented capacities on the African-music live circuit outside Africa. Two of the "
        "four are in Britain."),
    Paragraph(
        "If streaming is where support is measured badly, live is where it is measured honestly. "
        "Nobody divides your gate receipts by a national ARPU. A ticket is a ticket.", body),
    Paragraph(
        "On this ranking <b>Britain is first and it is not close</b>. Burna Boy became the first "
        "African artist to sell out a UK stadium, playing to 60,000 at London Stadium. Wizkid sold out "
        "the 20,000-capacity O2 in twelve minutes. The UK has both the venues and the density.", body),
    Paragraph(
        "<b>Portugal is the anomaly and the most interesting case in this report.</b> It has a modest "
        "payout rate ($0.0018), a small domestic African population, and hosts the largest Afrobeats "
        "festival on earth: Afro Nation in Portimão draws over 40,000 people from 180 countries. "
        "Portugal is not supporting African music with its own consumers. It is supporting it by "
        "being a place other countries' diasporas can affordably fly to. That is a real and "
        "underrated form of support, and it is invisible in every streaming statistic.", body),
    Paragraph(
        "The <b>United States</b> contributes the prestige tier — Madison Square Garden, the award "
        "ceremonies, the label deals. The 2026 tour routing of major African artists tells the same "
        "story as the data: London, New York, Toronto, Houston, Atlanta, Paris, Amsterdam. It is a "
        "map of the diaspora with a Portuguese beach attached.", body),
]

# ================= 09 =================
story += [
    Paragraph("11 · The Growth Frontier", h2),
    fig("growth_frontier.png",
        "Fig 9 — The fastest-growing markets for African music. Every one of them is a bottom-tier "
        "payout market."),
    Paragraph(
        "Indonesia is up <b>4,530%</b> over five years. India <b>1,650%</b>, the Philippines "
        "<b>1,492%</b>, Thailand <b>1,370%</b>. Brazil is up <b>500%</b> and Latin America as a "
        "region more than <b>400%</b> since 2020, with <b>183% year-on-year growth in 2025</b> alone. "
        "User-made playlists tagged “Afrobeats” grew <b>135%</b> between 2020 and 2025, and <i>Hot "
        "Hits Naija</i>, <i>African Heat</i> and <i>Gbedu</i> are the top three entry points for "
        "young listeners worldwide.", body),
    Paragraph(
        "Note that the Asian bloc is now four countries deep, not one. Indonesia, India, the "
        "Philippines and Thailand are all growing at four figures. Set that beside Fig 1 — where "
        "India already ranks third by certified units — and Asia stops looking like a curiosity and "
        "starts looking like the second front.", body),
    Paragraph(
        "This is genuinely thrilling and financially modest, and both halves of that sentence are "
        "true. Indonesia, India and Brazil pay $0.0010, $0.0008 and $0.0010 respectively. The "
        "frontier is expanding into precisely the countries that pay the least.", body),
    Paragraph(
        "Which is not an argument against the frontier. It is an argument for reading it correctly. "
        "Cultural reach and revenue are on different clocks: reach arrives first, and revenue arrives "
        "years later if and when those markets convert to paid subscriptions. Brazil in 2026 looks a "
        "lot like where Britain was with Afrobeats around 2015. The difference is that Britain then "
        "converted, because British listeners could afford £10 a month.", body),
]

# ================= 10 =================
story += [
    Paragraph("12 · The Scorecard", h2),
    Paragraph("Putting the four maps together gives four distinct kinds of country. This grouping is "
              "ours, not anyone's official ranking — but every column in it is sourced.", body),
    table([
        [Paragraph("Tier", th), Paragraph("Countries", th),
         Paragraph("What they give", th), Paragraph("What they lack", th)],
        [Paragraph("1. The core", cell_b),
         Paragraph("United Kingdom, United States, France, Germany", cell),
         Paragraph("High payout rate, large audience, dense diaspora, working live circuit. All four "
                   "in the top five for growth.", cell),
         Paragraph("Nothing structural. These are the markets to win.", cell)],
        [Paragraph("2. Pays well, under-built", cell_b),
         Paragraph("Canada, Australia, Netherlands, Ireland, Norway, Denmark, Sweden, Iceland", cell),
         Paragraph("Payout rates at or above the core — the Nordics roughly double it. Canada and the "
                   "Netherlands have real diaspora density.", cell),
         Paragraph("Little dedicated infrastructure: few festivals, no charts, thin promoter "
                   "networks.", cell)],
        [Paragraph("3. Audience without revenue", cell_b),
         Paragraph("Brazil, Indonesia, India, Mexico, Latin America broadly", cell),
         Paragraph("The growth. Enormous, fast, culturally genuine, and the future of the genre's "
                   "reach.", cell),
         Paragraph("Payout rates one-quarter to one-fifth of the core. Revenue lags reach by years.",
                   cell)],
        [Paragraph("4. Diaspora without an economy", cell_b),
         Paragraph("The Gulf states, and much of Asia", cell),
         Paragraph("Roughly 6.9 million Africans — a third of the entire diaspora.", cell),
         Paragraph("Everything else. No chart, no circuit, no payout tier, minimal discretionary "
                   "income.", cell)],
    ], [26 * mm, 36 * mm, 56 * mm, 52 * mm]),
    Paragraph(
        "The single most valuable observation in that table is that <b>tier 2 is underexploited</b>. "
        "Canada, the Netherlands, Australia and the Nordics pay as well as or better than the core "
        "markets and have almost no dedicated African-music infrastructure. That is not a gap in the "
        "audience. It is a gap in the promoters, the playlists and the touring routes — which is a "
        "fixable, commercial problem rather than an economic one.", body),
]

# ================= 11 & 12 =================
story += [
    Paragraph("13 · If You Are an Artist", h2),
]
story += bullets([
    "<b>Weight your dashboard before you read it.</b> Multiply your listener counts by roughly the "
    "Fig 5 factors. Your top revenue country is frequently not your top listener country, and it is "
    "usually the UK, the US or Germany.",
    "<b>Do not pick between the US, UK, France and Germany on royalty rate.</b> They pay within about "
    "15% of each other. Pick on visa access, promoter relationships, diaspora density and touring "
    "economics.",
    "<b>Route tours through tier 2.</b> Toronto, Amsterdam, Sydney, Oslo, Dublin. High-paying markets "
    "with real African populations and almost no competition for the audience's attention.",
    "<b>Treat frontier growth as marketing, not revenue.</b> Indonesia at +4,530% is a superb story "
    "to tell a label. It is not a budget line.",
    "<b>Britain is the highest-leverage single market on earth for African music.</b> Best rate among "
    "the majors, an Official Afrobeats Chart, stadium-scale live capacity, a dense diaspora. If you "
    "can only build one foreign market properly, build that one.",
    "<b>Register your publishing in the territories that pay.</b> A UK or German stream that is not "
    "correctly registered pays nothing at 4.4× nothing.",
])
story += [
    Paragraph("14 · If You Are a Fan, Promoter or Investor", h2),
]
story += bullets([
    "<b>Where you stream from matters more than how much you stream.</b> A Nigerian in Oslo streaming "
    "on a Norwegian account is worth roughly 7.8 Brazilian listeners to the artists they love. The "
    "address is doing the work.",
    "<b>Upgrade off the free tier if you are in a tier 1 or 2 country.</b> The pool an artist is paid "
    "from is built from subscription revenue in your country. In a high-ARPU market, converting is "
    "the single highest-leverage thing a fan can do.",
    "<b>A ticket still beats everything.</b> One £60 show delivers more to an artist than hundreds of "
    "thousands of streams from a low-rate market.",
    "<b>Promoters: tier 2 is the opening.</b> Canada, the Netherlands, Australia and the Nordics have "
    "the payment power and the population, and nobody is systematically serving them.",
    "<b>Investors: the gap is infrastructure, not talent.</b> Portugal proves a country can become a "
    "major node in this economy without a large domestic African population or a high payout rate — "
    "purely by building the venue and the routing. That is a business, and it is replicable.",
])

# ================= 13 =================
story += [
    Paragraph("15 · The Uncomfortable Part", h2),
    Paragraph("Three things this data says that the celebration around African music tends not to.",
              body),
    Paragraph(
        "<b>First, &ldquo;support&rdquo; is mostly a function of a country's wealth, not its "
        "affection.</b> Norway is not eight times more enthusiastic about Afrobeats than Brazil. It "
        "is eight times richer per subscriber. Almost everything in this report is a purchasing-power "
        "story wearing a cultural costume, and it is worth resisting the temptation to read affection "
        "into any of these rankings.", body),
    Paragraph(
        "<b>Second, the concentration is a risk.</b> Four countries — the UK, US, France and Germany "
        "— carry a hugely disproportionate share of the revenue attached to African music. Any genre "
        "whose income depends on remaining fashionable in four Western markets is exposed in a way "
        "that a genre with a paying domestic market is not.", body),
    Paragraph(
        "<b>Third, and least comfortable: the diaspora's value here is partly a function of having "
        "emigrated.</b> The same person is worth 4.4 times more to a Nigerian artist in London than "
        "in Lagos. That is not a moral fact and nobody should feel good about it, but it is the "
        "mechanism, and pretending otherwise leads artists to make bad decisions about where to spend "
        "their effort.", body),
    Paragraph("The fix is not for Africans abroad to stream harder. It is for African markets to "
              "become places where a subscription is affordable and a royalty is collectable. "
              "Everything else is a workaround.", pull),
]

# ================= 14 =================
story += [
    Paragraph("16 · Method &amp; Limits", h2),
    Paragraph("This report assembles published streaming, royalty and migration figures as at "
              "15 August 2026, read for what they say about which countries outside Africa materially "
              "support African music.", body),
]
story += bullets([
    "<b>A correction to our own previous report.</b> On 12 August we published <i>The Music Is "
    "African. The Money Is Abroad.</i> &mdash; using a figure of roughly $300 per million streams in Nigeria. "
    "The per-country table we use here implies about $1,100 per million for Nigeria — a three- to "
    "four-fold difference, from overlapping sources. Both are estimates of an unpublished number and "
    "we cannot resolve which is closer. The honest position is that the Nigerian rate is somewhere in "
    "the $300–$1,100 per million band, that the direction and rough magnitude of the gap to Western "
    "markets is robust across every source we found, and that the precise multiple — whether it is "
    "33× or 4× — is not. We have left the earlier report standing and flagged it there and here "
    "rather than quietly restate it.",
    "<b>Fig 1 and Fig 2 measure one song, not a genre.</b> We use “Calm Down” because it is the most "
    "certified African record ever made and therefore gives the widest country coverage available "
    "anywhere. It is not a proxy for all African music. A different song — an amapiano record, a "
    "Francophone one — would produce a different and probably narrower map.",
    "<b>The remix inflates some of those numbers.</b> The version featuring Selena Gomez is what "
    "carried the song in the United States, Canada and Australia, and those three totals should be "
    "read as African-music-plus-American-pop rather than as pure African-music demand. The European "
    "and Asian certifications are largely for the original.",
    "<b>Certification thresholds differ between countries.</b> Diamond is 333,333 units in France and "
    "800,000 in Canada. Units in Fig 1 therefore measure absolute consumption, not popularity "
    "relative to a country's size — small, rich countries such as the Netherlands look far weaker on "
    "units than they are per head. Certified units also depend on whether and when a label applied, "
    "so absence from Fig 1 is not proof of absence of listeners.",
    "<b>Fig 2 mixes chart types.</b> Most entries are national singles charts; Romania is an airplay "
    "chart and Global Excl. US is a Billboard aggregate. They are not strictly like for like.",
    "<b>Per-stream rates are estimates, not published figures.</b> Spotify does not disclose "
    "per-country rates. Fig 4, Fig 5 and Fig 6 all rest on a single estimated table and inherit its "
    "uncertainty. Treat the tiers as reliable and the decimals as indicative.",
    "<b>Fig 5 is our own arithmetic</b> — each country's estimated rate divided by Brazil's. It is a "
    "ratio of two estimates, so its error is larger than either.",
    "<b>Fig 3 is a growth ranking, not a size ranking.</b> It measures where Afrobeats gained the "
    "most <i>new</i> listeners in 2025, which systematically favours new markets over converted ones. "
    "Britain and the US are almost certainly larger in absolute terms than their positions imply.",
    "<b>The Spotify data is one platform.</b> Apple Music, YouTube, Audiomack and Boomplay have "
    "different geographies and different economics — Audiomack and Boomplay in particular are far "
    "more significant in Africa itself than their global share suggests.",
    "<b>Migrant-stock figures count the foreign-born</b>, not the heritage diaspora. Brazil's "
    "Afrobeats audience is substantially people of African descent whose families have been in Brazil "
    "for centuries, and they appear nowhere in Fig 7. The same applies to African-American audiences "
    "in the US and Caribbean-descended audiences in the UK. Fig 7 measures recent migration only.",
    "<b>The live section is qualitative about magnitudes.</b> Venue capacities are documented; gate "
    "receipts, guarantees and artist splits are not public.",
    "<b>The tier table in Section 12 is our construction</b>, not a published index. We have not "
    "applied weights or produced a composite score, because any weighting would be arbitrary and "
    "would give the grouping a false precision.",
    "<b>&ldquo;African music&rdquo; here leans Nigerian</b>, because Nigeria publishes the most "
    "usable data. Amapiano, Francophone, North African and East African scenes have different "
    "geographies — Francophone African music's relationship with France, in particular, is a much "
    "larger story than this report's treatment of it.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Certification and chart data for “Calm Down” from the compiled national certification "
        "tables (RIAA, BPI, SNEP, BVMI, FIMI, IMI, Music Canada, ARIA, Pro-Música Brasil, ZPAV and "
        "others); Spotify's 2025 Afrobeats rankings via MP3Bullet and Music Ally; Chartlex on per-country "
        "royalty rates; Spotify Wrapped 2025 via Techpoint Africa on global listener growth; The "
        "Creative Brief on Latin American and Asian growth rates; Afro Nation on festival attendance; "
        "Official Charts on the UK Afrobeats Chart; IFPI Global Music Report 2026 on market sizes; "
        "UN DESA migrant-stock data via our own report The Diaspora, Counted. Full inline links in "
        "the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/who-pays-for-african-music-2026<br/>"
        "Companion reports: The Music Is African. The Money Is Abroad. · Your Address Pays Better "
        "Than Your Following<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
