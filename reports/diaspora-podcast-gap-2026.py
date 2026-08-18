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
IMG = os.path.join(HERE, "diaspora-podcast-gap-2026", "img")
OUT = os.path.join(HERE, "diaspora-podcast-gap-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Diaspora Podcast Gap · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 18 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="Everybody Is Talking. Nobody Is Answering. (2026)",
                      author="Africa Global Forum",
                      subject="What the African diaspora listens to, and the territories nobody is working")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("Everybody Is Talking.", h1),
    Paragraph("Nobody is answering.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "The diaspora podcast audience is large, unusually commercially valuable, and mostly less "
        "than a year old. The diaspora podcast <i>shelf</i> is culture, comedy and relationships. "
        "This report maps what exists, gives the honest numbers on what a show can expect, and names "
        "<b>nine subjects we went looking for and could not find anyone covering.</b>", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("43%", big_num), Paragraph("27", big_num),
    Paragraph("42%", big_num), Paragraph("9", big_num),
], [
    Paragraph("of Black US adults listened<br/>to a podcast last month", big_lbl),
    Paragraph("downloads — the median<br/>episode, first seven days", big_lbl),
    Paragraph("of weekly listeners use<br/>YouTube most", big_lbl),
    Paragraph("subjects with demand,<br/>no incumbent and<br/>advertisers waiting", big_lbl),
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
    fig("supply_gap.png",
        "The supply-and-demand map this report is built on — see Section 08. The right column is "
        "what we searched for and did not find, not proof that nothing exists.", max_h=105 * mm),
    Paragraph("Published August 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/diaspora-podcast-gap-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "This report exists because a member of this network asked a practical question: is there "
        "room for another diaspora podcast, and if so, where? The answer is yes, and the room is not "
        "where most people look for it.", body),
]
story += bullets([
    "<b>The audience is large and young in the format.</b> <b>43%</b> of Black adults in the United "
    "States listened to a podcast in the last month, and <b>75%</b> of monthly listeners actively "
    "seek out content on Black stories and perspectives. Nearly half — <b>48%</b> — have been "
    "listening for under a year.",
    "<b>It converts unusually well.</b> <b>61%</b> of Black weekly listeners recommended a product "
    "after hearing about it on a podcast, against <b>49%</b> of US weekly listeners generally; "
    "<b>52%</b> bought something, against 44%.",
    "<b>It is a video product now.</b> YouTube is the most-used podcast service, at about <b>42%</b> "
    "of weekly consumers in the US. In the UK it has overtaken Spotify for the first time "
    "(<b>29% vs 28%</b>). Among Gen Z, <b>59%</b> consume podcasts on YouTube.",
    "<b>The download reality is brutal.</b> The median podcast episode gets <b>27 downloads</b> in "
    "its first seven days. The top 10% gets 409. The top 1% gets 4,615.",
    "<b>Money follows subject, not just size.</b> General host-read advertising runs about "
    "<b>$15–30 CPM</b>. Personal finance and investing runs <b>$40–65</b>. A small show about money "
    "can out-earn a large show about vibes.",
    "<b>And the shelf is lopsided.</b> Diaspora podcasting is well supplied with culture, comedy, "
    "dating, identity, faith and founder interviews. We searched for shows covering visas, credential "
    "recognition, the earnings gap, remittances, building from abroad and returning — and did not "
    "find them.",
    "<b>Two structural gaps are enormous.</b> Roughly <b>6.9 million Africans live in Asia and the "
    "Gulf</b> — a third of the entire diaspora — and we found no podcast serving them. Francophone "
    "and Lusophone diasporas are similarly thin.",
])
story += [
    Paragraph("The diaspora is well served for company and badly served for answers. That is the "
              "opening.", pull),
]

# ================= 02 =================
story += [
    PageBreak(),
    Paragraph("02 · The Audience Is Real, and It Is New", h2),
    fig("audience.png",
        "Fig 1 — From the Black Podcast Listener Report, Edison Research with SXM Media and "
        "Mindshare USA. This measures Black American adults, which overlaps with but is not the same "
        "as the African diaspora — see Method."),
    Paragraph(
        "Two numbers matter more than the headline. The first is <b>75%</b> — the share of Black "
        "monthly listeners who actively seek out content focused on Black stories and perspectives. "
        "That is not passive availability. That is demand expressing itself as search behaviour, "
        "which is the condition under which a new show can actually be found.", body),
    Paragraph(
        "The second is <b>48% listening for under a year, 27% for under six months.</b> This audience "
        "is not settled. In a mature market the incumbents own the habit. Here, half the audience "
        "arrived recently and has not yet decided what it listens to. That window does not stay open "
        "indefinitely.", body),
    Paragraph(
        "On the continent, the picture is consistent. South Africa, Nigeria, Kenya, Ghana and Angola "
        "are Africa's biggest podcast-consuming countries, and Kenya, Nigeria and South Africa each "
        "carry over a thousand active shows.", body),
    Paragraph(
        "One characteristic of African podcasting distinguishes it sharply from the US and European "
        "markets: <b>audiences and creators skew female</b>, where the Western podcast market skews "
        "male. That shapes what already works and what an incoming show is competing with.", body),
]

# ================= 03 =================
story += [
    PageBreak(),
    Paragraph("03 · It Converts Better Than Average", h2),
    fig("commercial_premium.png",
        "Fig 2 — Actions taken after hearing a podcast advertisement. Edison Research with SXM Media "
        "and Mindshare USA."),
    Paragraph(
        "This is the single most commercially important fact in the report, and the one least "
        "discussed by people starting shows. Black weekly podcast listeners <b>act on advertising at "
        "rates roughly a quarter higher</b> than the national average — 61% against 49% on "
        "recommendation, 52% against 44% on purchase. In an advertising market that buys on cost per "
        "thousand, an audience that converts at 1.25× the base rate is worth more than its size "
        "suggests.", body),
    Paragraph(
        "What that means practically: <b>you do not need a large show to have a sellable one.</b> The "
        "pitch to an advertiser is not “I have 50,000 listeners.” It is “I have 4,000 listeners in a "
        "demographic that converts a quarter better than your existing buy, and nobody else is "
        "selling access to them.” That is a stronger position than raw scale, and it is available "
        "immediately.", body),

    Paragraph("04 · It Is a Video Product Now", h2),
    fig("platforms.png",
        "Fig 3 — Platform preference among weekly podcast consumers. Edison Research US and UK data."),
    Paragraph(
        "If you take one operational decision from this report, take this one. <b>YouTube is now the "
        "most-used podcast platform</b>, at roughly 42% of weekly podcast consumers in the United "
        "States. In the UK it has overtaken Spotify for the first time on record. Among Gen Z the "
        "figure is 59%. In the US, <b>51% of people aged 12+ have watched a podcast</b>, against 70% "
        "who have listened.", body),
]
story += bullets([
    "<b>Launching audio-only is choosing to be smaller.</b> It is a legitimate choice with real cost "
    "savings, but it should be a decision, not an oversight.",
    "<b>YouTube is a search engine.</b> Nobody searches YouTube for “three friends chatting.” People "
    "search it for “how do I get my nursing qualification recognised in the UK.” A practical show is "
    "discoverable in a way a conversational one is not.",
    "<b>Distribution on the continent is a separate problem.</b> African podcasting has a documented "
    "obstacle in that dedicated podcast apps are not reliably pre-installed on Android handsets. If "
    "part of your audience is on the continent, YouTube and WhatsApp matter more than Apple Podcasts.",
])

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("05 · What Already Exists", h2),
    Paragraph("The diaspora podcast scene is not empty. It is concentrated.", body),
    Paragraph(
        "At the top, the shows are real businesses with real reach. <i>The Receipts</i>, hosted by "
        "British-Nigerian and British-Ghanaian women, reports over <b>100,000 weekly listens across "
        "71 countries</b>, and moved from independent to BBC Radio 1Xtra to Spotify. <i>I Said What I "
        "Said</i>, running from Lagos since 2017, is routinely described as one of Africa's biggest "
        "podcasts and is now in its eighth season.", body),
    Paragraph(
        "Below them sits a wide field of diaspora shows — <i>Afros in the Diaspora</i>, "
        "<i>Conversations from the Diaspora</i>, <i>The New African Diasporas Podcast</i> and many "
        "others — covering immigration as emotional transition, identity, family expectation, "
        "generational difference, and the stigma around therapy in African and immigrant communities.",
        body),
    Paragraph(
        "That work is good and it is needed. But look at the shape of it. Nearly all of it belongs to "
        "one broad category: <b>the experience of being African abroad, discussed.</b> Culture, "
        "comedy, dating, identity, mental health, faith, and interviews with founders. What is almost "
        "entirely absent is the other category: <b>the mechanics of being African abroad, "
        "explained.</b>", body),

    Paragraph("06 · The Honest Numbers", h2),
    fig("downloads.png",
        "Fig 4 — First-week download benchmarks, from Buzzsprout platform data. Log scale — the "
        "distribution spans two orders of magnitude."),
    Paragraph(
        "<b>The median podcast episode receives 27 downloads in its first seven days.</b> Not 27,000. "
        "Twenty-seven. Reaching 97 puts you in the top quarter of all podcasts. Reaching 409 puts you "
        "in the top tenth.", body),
]
story += bullets([
    "<b>The discouraging half.</b> Podcasting has almost no barrier to entry and therefore enormous "
    "attrition. Most shows are heard by a few dozen people and stop within a year. If your plan "
    "requires 50,000 listeners to work, your plan will not work.",
    "<b>The encouraging half.</b> The bar for being a genuinely significant show is far lower than "
    "people assume. A few hundred engaged listeners is top-decile. A thousand is top 5%. For a "
    "specific, underserved, commercially attractive audience, that is achievable — and enough to sell.",
])
story += [
    Paragraph("You are not competing with Joe Rogan. You are competing with 27.", pull),
]

# ================= 07 =================
story += [
    PageBreak(),
    Paragraph("07 · What a Thousand Listens Is Worth", h2),
    fig("cpm.png",
        "Fig 5 — Reported CPM ranges by category, 2026. Ranges vary by source and by whether the "
        "figure is buy-side or sell-side."),
    Paragraph(
        "Advertising is sold on CPM — cost per thousand listens. General host-read mid-roll "
        "advertising runs about <b>$15–30</b>. Personal finance and investing shows command "
        "<b>$40–65</b>. Business and B2B shows sit at $35–55.", body),
    Paragraph(
        "Do the arithmetic, because it inverts the usual assumption. A comedy show with <b>10,000</b> "
        "listens an episode at $20 CPM earns roughly <b>$200</b> per ad slot. A money show for the "
        "diaspora with <b>3,000</b> listens at $55 CPM earns roughly <b>$165</b> — from less than a "
        "third of the audience.", body),
    Paragraph(
        "And the second show has a structural advantage the first does not: <b>its subject matter "
        "matches the advertisers who most want this audience.</b> Remittance companies, digital "
        "banks, currency services, immigration law firms, credential-evaluation services, diaspora "
        "mortgage products, insurers. Those are endemic advertisers for a diaspora money show and "
        "irrelevant to a comedy show.", body),
    Paragraph(
        "Two practical thresholds. Most direct sponsorships become viable around <b>5,000 downloads "
        "per episode</b>; some ad networks will work with shows from around <b>500</b>. But the more "
        "useful principle is the one the industry states plainly: a thousand dedicated listeners in a "
        "valuable niche is easier to sell than ten thousand disengaged ones.", body),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · The Gap", h2),
    Paragraph(
        "Here is where this report can do something most market analyses cannot. Africa Global Forum "
        "has spent 2026 publishing research on what Africans abroad actually need to know — eleven "
        "fact-checked reports on visas, migration destinations, earnings gaps, credential "
        "recognition, remittances, property, intermarriage and investment failure.", body),
    Paragraph(
        "Those reports are, in effect, <b>a documented map of diaspora information demand.</b> Set "
        "that against the podcast supply described in Section 05 — the map is on the cover — and the "
        "mismatch is stark.", body),
    Paragraph(
        "The pattern is consistent enough to state as a rule. <b>Diaspora podcasting covers how it "
        "feels. It does not cover how it works.</b>", body),
    Paragraph(
        "That is not a criticism of the existing shows, which are doing what they set out to do and "
        "doing it well. It is an observation about where an entrant has room. Every one of the "
        "subjects in the right-hand column has three properties an incoming show wants: <b>documented "
        "demand, no incumbent, and endemic advertisers with money.</b>", body),

    Paragraph("09 · Nine Territories Nobody Is Working", h2),
    Paragraph("Each of these is a show. Each has a named audience, a specific question, and an "
              "evidence base that already exists in this library.", body),
    table([
        [Paragraph("The territory", th), Paragraph("The demand evidence", th),
         Paragraph("Who would advertise", th)],
        [Paragraph("<b>1. Status and the cost of staying legal</b>", cell),
         Paragraph("Fees across 26 countries; the UK shortens its post-study window in January 2027",
                   cell),
         Paragraph("Immigration law firms, relocation, insurers", cell)],
        [Paragraph("<b>2. Getting your qualification recognised</b>", cell),
         Paragraph("<b>41.4%</b> of non-EU citizens in the EU work below their qualification level",
                   cell),
         Paragraph("Credential evaluators, exam providers, universities", cell)],
        [Paragraph("<b>3. The earnings gap, and closing it</b>", cell),
         Paragraph("<b>26.1%</b> pay gap for sub-Saharan African workers against 9.0% for European "
                   "arrivals", cell),
         Paragraph("Recruiters, professional bodies, training", cell)],
        [Paragraph("<b>4. Money home without losing it</b>", cell),
         Paragraph("Sending $200 to sub-Saharan Africa costs <b>8.78%</b> against a 3% UN target",
                   cell),
         Paragraph("Remittance firms, neobanks, FX — high-CPM fintech", cell)],
        [Paragraph("<b>5. Building and buying from abroad</b>", cell),
         Paragraph("~<b>10%</b> of rural African land is formally documented; 56,000 abandoned "
                   "projects in Nigeria", cell),
         Paragraph("Developers, property lawyers, escrow, surveyors", cell)],
        [Paragraph("<b>6. Going back</b>", cell),
         Paragraph("Between <b>20% and 50%</b> of immigrants leave within five years; 75% in the "
                   "Netherlands", cell),
         Paragraph("Pensions, health insurance, relocation, property", cell)],
        [Paragraph("<b>7. The Gulf</b>", cell),
         Paragraph("<b>6.9 million</b> Africans in Asia and the Gulf — a third of the diaspora", cell),
         Paragraph("Remittance firms, recruiters, legal services", cell)],
        [Paragraph("<b>8. Francophone and Lusophone Africa abroad</b>", cell),
         Paragraph("France is the largest single host of African students; the market is almost "
                   "entirely anglophone", cell),
         Paragraph("Everything above, with no competition", cell)],
        [Paragraph("<b>9. The second generation, as adults</b>", cell),
         Paragraph("Migrant-stock data misses them; Nigerian-ancestry in the US is <b>60% larger</b> "
                   "than Nigerian-born", cell),
         Paragraph("Financial services, travel, education", cell)],
    ], [50 * mm, 66 * mm, 54 * mm]),
    Paragraph(
        "If you want the single strongest commercial pick, it is <b>number four</b>. It combines the "
        "highest-CPM advertising category in podcasting with the most universal diaspora activity. If "
        "you want the strongest <i>strategic</i> pick — the one where you could own the category "
        "outright for years — it is <b>number seven or number eight</b>.", body),
]

# ================= 10 & 11 =================
story += [
    PageBreak(),
    Paragraph("10 · The Gulf, Again", h2),
    Paragraph(
        "This is the third AGF report in a row to arrive at the same blind spot from a different "
        "direction, which is usually a sign the blind spot is real.", body),
    Paragraph(
        "Roughly <b>6.9 million Africans live in Asia and the Gulf</b> — about a third of the 20.7 "
        "million living outside the continent, and more than double the number in North America. Our "
        "music report found no Gulf presence anywhere in the African music economy. This one searched "
        "for podcasts serving that population and <b>did not find them either.</b>", body),
    Paragraph(
        "We want to be careful about what that means. Our search was in English, from outside the "
        "region, using Western podcast directories. There may well be Arabic, Amharic, Somali, "
        "Tigrinya or Swahili-language shows we simply could not see, and we would genuinely like to "
        "be corrected. But an audience of nearly seven million people that is invisible to standard "
        "discovery is, either way, an underserved audience.", body),
    Paragraph(
        "The commercial logic is unusually clean. Gulf-based African workers are <b>overwhelmingly "
        "remitters</b> — that is frequently the entire purpose of the migration — which makes them "
        "the single most attractive audience on earth for remittance and financial-services "
        "advertisers.", body),
    Paragraph("A third of the diaspora, an obvious advertiser base, and no incumbent. If that is not "
              "whitespace, nothing is.", pull),
    Paragraph(
        "The honest counterweight: this is also the hardest of the nine to execute. Discretionary "
        "income is lower, listening may be on cheaper devices and constrained data, and some subject "
        "matter is politically sensitive in the countries where the audience lives. It is whitespace "
        "because it is difficult, not because nobody noticed.", body),

    Paragraph("11 · The Language Gap", h2),
    Paragraph(
        "Almost everything described in this report is in English. That reflects the market, and it "
        "is a strange fact about a continent where <b>France hosts the largest single population of "
        "African students</b> and where French, Portuguese and Arabic are the working languages of a "
        "very large share of the diaspora.", body),
    Paragraph(
        "Our searches surfaced a handful of relevant French-language shows — work on Françafrique, on "
        "Kenyan experience in France, on African studies — but nothing resembling the practical "
        "diaspora-service podcast this report is describing, in any language other than English.",
        body),
    Paragraph(
        "For anyone who works comfortably in French or Portuguese, that is the lowest-competition "
        "entry point in this entire analysis. The diaspora questions are identical — residence "
        "permits, credential recognition, remittances, property — and the answers differ mainly in "
        "jurisdiction. The research burden is real; the competitive burden is close to zero.", body),
]

# ================= 12 & 13 =================
story += [
    PageBreak(),
    Paragraph("12 · If You Are Starting One", h2),
]
story += bullets([
    "<b>Pick a question, not a topic.</b> “Diaspora life” is a topic and it is taken. “How much does "
    "it cost to bring your mother to live with you, and can you?” is a question, and it is "
    "searchable, answerable and sponsorable.",
    "<b>Publish on YouTube from episode one</b>, even if the video is unglamorous. It is where 42% of "
    "the audience is and the only platform where a title answering a specific question gets found by "
    "someone who was not looking for you.",
    "<b>Build for search, not for the feed.</b> Episode titles should be the questions people type. A "
    "practical show accumulates an audience for years from episodes published once.",
    "<b>Aim for the top decile, not for fame.</b> 409 downloads in week one is a genuinely successful "
    "show. Set that as the target and it is reachable within a year.",
    "<b>Sell the conversion rate, not the download count.</b> Fig 2 is your media kit.",
    "<b>Get a guest with the actual answer.</b> The differentiator for a practical show is not "
    "charisma, it is access — the immigration solicitor, the credential assessor, the person who did "
    "the requalification. That is a network problem, which is exactly what this Forum is for.",
    "<b>Do not price it as a hobby that might make money.</b> Ten to twenty episodes in a specific "
    "vertical is a sellable asset well before it is a large show.",
    "<b>Expect the first year to be quiet.</b> Half of all episodes get under 27 downloads. "
    "Consistency is the entire strategy, because most competitors stop.",
])
story += [
    Paragraph("13 · The Format Decision", h2),
    Paragraph("One structural choice determines most of the rest, and it is worth making "
              "deliberately.", body),
]
story += bullets([
    "<b>The conversation show</b> — two or three friends, weekly, personality-led. Cheap, enjoyable, "
    "and the most crowded part of the market. It lives on relationship with the hosts, which takes "
    "years to build and cannot be searched for. This is what most people start and why most stop.",
    "<b>The service show</b> — one question per episode, answered properly, usually with a guest who "
    "has the credential. Harder to make, requires actual research, and is the format this report's "
    "evidence points at. It compounds.",
    "<b>The narrative show</b> — produced, reported, documentary-style. Highest quality ceiling, "
    "highest cost, hardest to sustain independently.",
])
story += [
    Paragraph(
        "Given the gap on the cover and the CPM structure in Fig 5, <b>the service format is where "
        "the unclaimed ground is.</b> It is also, conveniently, the format that suits someone whose "
        "advantage is a network and a research library rather than a stand-up act.", body),
]

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("14 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First, most podcasts fail, and the reason is usually consistency rather than quality.</b> "
        "The evidence is unambiguous that shows stop. A podcast is a weekly obligation for years, and "
        "the median outcome is 27 downloads and a quiet ending after eleven episodes. Anyone starting "
        "should plan for a year of near-silence and decide in advance whether they will keep going "
        "through it.", body),
    Paragraph(
        "<b>Second, the gap may be a gap for a reason.</b> We have argued that nobody is making "
        "practical diaspora shows. The honest alternative explanation is that people have tried and "
        "found that audiences say they want practical information and actually listen to "
        "entertainment. We found no evidence either way. The counter-evidence is the 75% seeking-out "
        "figure and the fact that these questions get thousands of views when answered on YouTube by "
        "immigration lawyers and accountants — just not in podcast form.", body),
    Paragraph(
        "<b>Third, this audience deserves better than engagement bait.</b> A show about visas, money "
        "and qualifications is a show where being wrong has consequences for people's lives. The "
        "reason the existing service content is thin is partly that it is genuinely hard to do "
        "responsibly — rules change, jurisdictions differ, and “I heard it on a podcast” is a bad "
        "basis for a visa decision. If you take the gap, take the obligation that comes with it.",
        body),
]

# ================= 15 =================
story += [
    PageBreak(),
    Paragraph("15 · Method &amp; Limits", h2),
    Paragraph("This report assembles published audience, platform and industry figures as at "
              "18 August 2026 and sets them against a manual review of the diaspora podcast field.",
              body),
]
story += bullets([
    "<b>“We could not find a show doing this” is not “no show exists.”</b> The supply map and Section "
    "09 rest on searches conducted in English through Western podcast directories and search engines. "
    "Podcast discovery is genuinely poor, small shows are close to invisible, and we will certainly "
    "have missed things. Treat the right-hand column as <i>an absence of visible supply</i> — which "
    "is what matters commercially anyway — rather than proof of a vacuum.",
    "<b>The audience data is about Black Americans, not the African diaspora.</b> The Edison figures "
    "in Fig 1 and Fig 2 measure Black US adults 18+. That population overlaps with the African "
    "diaspora but is mostly not it. We use it because it is the best-measured proxy available and no "
    "equivalent study of the African diaspora specifically exists. This is a real limitation.",
    "<b>Download benchmarks come from one hosting platform.</b> Buzzsprout's data reflects its own "
    "customer base, which skews toward independent and smaller shows. The percentile ladder is "
    "directionally sound rather than exact.",
    "<b>CPM figures vary widely by source</b> and depend on whether they are buy-side or sell-side, "
    "host-read or programmatic. Treat Fig 5 as a ranking of categories, not a rate card.",
    "<b>African podcast market projections are forecasts</b> from commercial research firms and we "
    "have not relied on them for any conclusion. The Africa listening ranking has no published "
    "volumes attached.",
    "<b>The demand column in Section 09 is our own research library</b>, which is a defensible but "
    "not neutral source. It reflects what we chose to investigate. It is evidence that these "
    "questions have answers worth publishing, not proof that a podcast audience exists for each.",
    "<b>We have not surveyed anyone.</b> There is no primary audience research in this report. A "
    "hundred conversations with actual listeners would be worth more than everything here, and "
    "remains the obvious next step for anyone serious.",
    "<b>Named shows are cited as illustrations</b>, not as an exhaustive or ranked list, and reported "
    "listener figures are those the shows or platforms have published themselves.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Black Podcast Listener Report (Edison Research, SXM Media, Mindshare USA); Edison Research "
        "on YouTube as the preferred podcast service and Edison Podcast Metrics UK; Buzzsprout on "
        "download benchmarks; MillionPodcasts and industry rate guides on CPM; Reuters Institute on "
        "African podcasting economics; Spotify via Vanguard on African listening rankings; Rephonic "
        "and BBC reporting on named shows. Demand evidence throughout is drawn from AGF's own report "
        "library. Full inline links in the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/diaspora-podcast-gap-2026<br/>"
        "Companion reports: You Sent the Money. Did You Buy Anything? · How Long Until It Was Worth "
        "It?<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
