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
IMG = os.path.join(HERE, "new-ladder-2026", "img")
OUT = os.path.join(HERE, "new-ladder-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The New Ladder · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 14 September 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The New Ladder (2026)",
                      author="Africa Global Forum",
                      subject="Jobs before and after AI, the entry-vs-mid split at home and abroad, and what to expect next")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The New", h1),
    Paragraph("ladder.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "The job market did not collapse after AI. It did something stranger: it split by "
        "level. Young workers in AI-exposed occupations sit 19% below trend while experienced "
        "workers in the same fields hold or gain; UK graduate postings fell 45% in a single "
        "year while the sponsorship salary threshold rose to £41,700 — two jaws of a vise "
        "closing on exactly the rung foreigners enter through. The market that was, the market "
        "that is, the entry-versus-mid divide at home and abroad, the coming mid-level premium "
        "— and the five calls about the future this report will stand behind.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("−19%", big_num), Paragraph("−45%", big_num),
    Paragraph("£41,700", big_num), Paragraph("+78m", big_num),
], [
    Paragraph("young workers vs trend in<br/>AI-exposed occupations —<br/>experienced: flat to rising", big_lbl),
    Paragraph("UK graduate postings in one<br/>year — the entry gate narrows<br/>as the visa clock starts", big_lbl),
    Paragraph("the UK sponsorship threshold<br/>— now priced above most<br/>junior salaries", big_lbl),
    Paragraph("net new jobs worldwide by<br/>2030 (WEF) — the reshuffle,<br/>not the apocalypse", big_lbl),
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
    fig("level_split.png",
        "Fig 1 — The split is by level, not industry (Stanford, ADP payroll data; bars "
        "directional). Same office, same field: the junior seat empties, the experienced seat "
        "gains.", max_h=90 * mm),
    Paragraph("Published September 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/new-ladder-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Every career plan in this network — and every family plan behind it — was drawn on a "
        "map of the old job market. The map has changed while people were mid-journey. Here is "
        "the new one, measured:", body),
]
story += bullets([
    "<b>Before and after, in one line: the jobs did not vanish; the door moved.</b> The "
    "pre-AI market bought graduates in bulk and trained them on repetitive junior work. That "
    "work is precisely what AI now does — so intake collapsed at the bottom while everything "
    "above it held: UK graduate postings fell 45% year-on-year, and 73% of employers now "
    "screen with AI. The aggregate market looks fine. The <i>entry</i> market does not.",
    "<b>The split is by level, not industry.</b> Ages 22–25 in AI-exposed occupations are "
    "~19% below trend while experienced workers in the <i>same occupations</i> are flat to "
    "rising. Entry-level and mid-career are now, functionally, different job markets.",
    "<b>Abroad, the split doubles.</b> The foreign graduate faces the entry squeeze through "
    "two gates on one clock: a hiring market that shrank exactly as the post-study window "
    "opens, and sponsorship thresholds — the UK's now £41,700 — priced above most junior "
    "salaries. Sponsorship migrated up the ladder and out to the shortage lists. Plan for "
    "where it went.",
    "<b>The global rebalance has winners in two buckets.</b> WEF: 170 million roles created, "
    "92 million displaced, net +78 million by 2030 — growth in hands-and-heart work (care, "
    "health, education, trades) and frontier-tech (AI, data, security); decline in routine "
    "information-handling at every level — the diaspora's classic side doors.",
    "<b>The future's biggest prize is the middle.</b> Firms that stopped training juniors "
    "still need tomorrow's seniors — a bottleneck that makes trusted mid-level people the "
    "scarcest asset of the next decade. Every strategy here reduces to one instruction: cross "
    "to mid-level fastest, by any rung available — including building experience at home and "
    "entering the global ladder in the middle.",
])
story += [
    Paragraph("The old market sold ladders. The new one sells a gap — and pays a premium to "
              "everyone who finds a way across it.", pull),
]

# ================= 02 & 03 =================
story += [
    PageBreak(),
    Paragraph("02 · The Market That Was", h2),
    fig("before_after.png",
        "Fig 2 — The old deal and the new one. Not mass unemployment — a redistribution.",
        max_h=95 * mm),
    Paragraph(
        "The 2010s labour market ran on a specific bargain: <b>the credential was the ticket, "
        "and the employer paid for the apprenticeship.</b> A degree opened a junior seat; the "
        "first years were repetitive, supervised work that was simultaneously the firm's grunt "
        "work and the worker's training. The “war for talent” years were that bargain at "
        "maximum generosity — and they are the years the diaspora's playbook was written in: "
        "study abroad, catch the scheme, convert to sponsorship, settle. The load-bearing "
        "detail: <b>the entry rung existed because the repetitive work existed.</b>", body),

    Paragraph("03 · What Actually Changed", h2),
    Paragraph(
        "The change was surgical, not apocalyptic. Total employment did not crash. What "
        "changed is <b>which tasks firms must buy humans for</b> — and the first tasks AI took "
        "were precisely the repetitive junior ones the entry bargain was built on. The result "
        "shows up where the mechanism predicts: hiring freezes at the bottom, stability above "
        "— UK graduate postings −45% year-on-year, entry/junior vacancies down roughly a third "
        "since late 2022, young-worker employment in exposed occupations sliding while "
        "experienced employment holds. And 73% of employers now screen with AI, so the "
        "shrunken doors are also guarded differently.", body),
    Paragraph(
        "Both popular stories are wrong. Not “AI is taking all the jobs” — the WEF's net "
        "projection is positive and experienced workers are gaining. Not “nothing changed” — "
        "tell that to the graduate holding forty rejections. The accurate sentence: <b>AI "
        "repriced the ladder, rung by rung — and the bottom rung took nearly all of the "
        "hit.</b>", body),
    Paragraph(
        "The honest complication: the attribution is genuinely contested. LinkedIn's 2026 "
        "Labor Market Report argues the slow market is <i>not</i> AI's fault — in its data, "
        "hiring trends look similar for the most- and least-exposed roles, and for entry vs "
        "experienced software engineers, with <b>rates and uncertainty as primary "
        "drivers</b>; hiring sits 20–35% below pre-pandemic across advanced economies while "
        "emerging markets surge (India +40%, UAE +37%). A Danish linked-data study found "
        "<b>no detectable average effect on earnings or hours</b> two years after ChatGPT in "
        "its occupations; the NY Fed documents graduate unemployment rising 3.6%→5.6% "
        "(2019→2026, ages 22–27) but points also at remote work destroying entry-job "
        "mentoring. The refined Stanford reading: 22–25s <i>fell ~11%</i> in the two "
        "most-exposed quintiles while <i>growing ~10%</i> in the least — a 19% <i>relative</i> "
        "shortfall, not an absolute collapse. Where that leaves a reader: <b>the entry "
        "squeeze is real and measured; its causes are contested — and for the jobseeker it "
        "barely matters, because every strategy in this report works under both "
        "explanations.</b>", body),
]

# ================= 04 =================
story += [
    Paragraph("04 · Entry vs Mid: The Level Split", h2),
    Paragraph(
        "The Stanford payroll research separates workers by age <i>and</i> occupation "
        "exposure: <b>ages 22–25 in the most AI-exposed occupations are ~19% below trend; the "
        "same ages in less-exposed work are roughly flat; and experienced workers in the very "
        "same exposed occupations are flat to rising</b> (Fig 1). It is not that accounting "
        "is dying and nursing is thriving — it is that <i>junior</i> accounting is dying "
        "while <i>senior</i> accounting thrives. The split runs horizontally through every "
        "exposed industry.", body),
]
story += bullets([
    "<b>Experience inflation:</b> with juniors optional, “entry-level” postings quietly "
    "demand two or three years of experience — the rung is advertised but not really there.",
    "<b>The queue at fewer doors:</b> record graduate cohorts compete for a shrunken intake, "
    "so rejection counts say less about candidates than ever — read alongside our confidence "
    "research.",
    "<b>The quiet appreciation of the middle:</b> the same mechanism that starves the bottom "
    "bids up everyone already across — Section 07's story. Entry and mid-career now have "
    "different prices, queues and politics. Treat them as different markets, because "
    "employers already do.",
])

story += [
    Paragraph("05 · The Same Split, Abroad", h2),
    fig("two_gates.png",
        "Fig 3 — Two gates, one clock. The entry squeeze lands hardest on the person with "
        "the least time to wait it out.", max_h=100 * mm),
    fig("migrant_outcomes.png",
        "Fig 4 — No single migrant story (INSEE, Eurostat, StatCan, BLS). The foreigner's "
        "bigger problem is often the overqualification trap — and it predates AI.",
        max_h=100 * mm),
    Paragraph(
        "The honest baseline first: “foreigners abroad” is not one story. France runs a "
        "persistent gap — immigrant unemployment 11.7% vs 6.9% (2024) — predating GenAI "
        "entirely. The EU's deeper problem: <b>41.4% of employed tertiary-educated non-EU "
        "citizens work below their qualification, vs 20.0% of nationals</b>; Canada reports "
        "the same shape (32.6% vs 19.1%). The US shows near parity in aggregate (4.2% vs "
        "4.3%). The AI-era risk for migrants is therefore not mass exclusion; it is <b>the "
        "deepening of the overqualification trap</b> — more degree-holders parked in "
        "survival work as the junior professional rung thins.", body),
    Paragraph(
        "A local graduate facing the frozen rung can wait — live at home, temp, retry. The "
        "foreign graduate cannot: the post-study visa is a <b>fixed clock</b>, and it starts "
        "precisely when the market gate is narrowest. Then the second gate: the UK's general "
        "threshold, £38,700 in 2024, now sits at <b>£41,700</b> — above most junior salaries "
        "— so even the graduate who wins a rare entry seat may find it cannot legally sponsor "
        "them. Add the sponsor's calculus (why pay fees for a junior when AI plus abundant "
        "local juniors exist?) and the name discount at the algorithmic screen, and the old "
        "convert-the-degree route is triple-gated. Where did sponsorship go? <b>Up and "
        "sideways</b> — up to mid/senior hires that clear thresholds easily, and sideways to "
        "the shortage lists (health, care, trades, teaching), which carry lower thresholds, "
        "dedicated visas and political protection. The door abroad is open at the top of the "
        "ladder and at the hands-and-heart occupations — and nearly shut at the generic "
        "junior office rung in between.", body),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · Where the Jobs Are Going", h2),
    fig("wef.png",
        "Fig 5 — WEF Future of Jobs 2025: the reshuffle, not the apocalypse.",
        max_h=95 * mm),
    fig("growing_declining.png",
        "Fig 6 — The growth is hands-and-heart or frontier-tech; the decline is routine "
        "information-handling — including the diaspora's classic back-office side doors.",
        max_h=92 * mm),
    Paragraph(
        "Read the columns as a diaspora strategist. The growing side is a barbell: "
        "hands-and-heart (care, nursing, education, trades, delivery, green energy — the "
        "ageing rich world's unfakeable needs) and frontier-tech (AI, data, security). "
        "African migration corridors already run heavily into the first bucket. The "
        "declining side contains the clerical, data-entry and bookkeeping roles that carried "
        "a generation from survival work into the middle class. Those bridges are the ones "
        "burning. Pick an end, or pick the frontier — the middle of the old office is not "
        "where the next foothold is.", body),
    Paragraph(
        "The frontier end now has a headcount: LinkedIn counts <b>1.3 million new AI-enabled "
        "jobs globally in two years</b> plus 600,000 new data-centre jobs in the last year, "
        "with “AI Engineer” the #1 US role and Head-of-AI positions up ~30% across major "
        "economies — the “new-collar” era, much of it hiring without traditional "
        "gatekeeping. The US BLS puts numbers under the other end for 2025–35: healthcare "
        "support +13.3%, computer/mathematical +7.3%, office and administrative support "
        "−4.0% — and projects <b>60% of new jobs by 2030 from occupations not typically "
        "requiring a degree</b>. The culture is following the money: majorities in the US "
        "(62%) and UK (55%) now prefer trades to corporate careers, and ~6 in 10 Gen Z call "
        "trades more meaningful than office work. The barbell is not a hardship posting. It "
        "is where the market's respect went.", body),
]

# ================= 07 =================
story += [
    Paragraph("07 · The Mid-Level Premium", h2),
    fig("midlevel.png",
        "Fig 7 — Why the middle is becoming the best real estate in the labour market.",
        max_h=105 * mm),
    Paragraph(
        "AI floods the market with drafts, code and analysis — making the scarce input "
        "<b>judgement</b>: knowing which output is wrong, risky, or good enough to sign. "
        "Judgement lives at mid-level and above. The experienced worker with AI does what a "
        "senior plus several juniors did — so firms bid up the one and stop hiring the "
        "several. <b>Accountability</b> completes the moat: clients, courts and regulators "
        "require a human name on the decision. And the twist that turns description into "
        "forecast: <b>the training bottleneck</b>. The juniors firms are not hiring today are "
        "the seniors they cannot hire in five years — the market is manufacturing a mid-level "
        "shortage, and whoever stands on the middle rungs when it bites will enjoy the best "
        "seller's market in modern white-collar history. Every strategy reduces to one "
        "sentence: <b>get across the gap to trusted mid-level, faster than the old ladder "
        "assumed, by any rung available.</b>", body),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · Crossing the Gap", h2),
    fig("crossing.png",
        "Fig 8 — Five ways over the missing rungs, at home and abroad.", max_h=108 * mm),
    Paragraph(
        "<b>The adjacent door</b>: services, operations, support and field roles still hire "
        "at entry — and sit one internal move from the analyst seat that never advertises "
        "externally; inside beats outside in a frozen market. <b>Bolted-on rungs</b>: "
        "licensed and apprenticed paths — nursing, trades, training contracts, residencies — "
        "are the one part of the economy where training is <i>contractual</i>, and the "
        "shortage lists make them the most visa-durable routes abroad. <b>Arriving "
        "pre-experienced</b>: nobody funds the junior years anymore, so evidence them "
        "yourself — internships, freelance contracts, shipped projects. <b>Sequencing "
        "through home</b> — Section 10. And <b>AI as seniority prosthetic</b>: the junior "
        "who manages AI output like a supervisor — delegating, reviewing, catching errors, "
        "taking responsibility — is performing the mid-level act early; documented, that is "
        "the fastest synthetic experience available.", body),

    Paragraph("09 · What Employers Now Buy", h2),
    Paragraph(
        "Four things, in rising order of scarcity. <b>AI-fluency as a floor</b> — assumed, "
        "the way spreadsheet literacy was in 2010. <b>Proof over paper</b> — portfolios and "
        "shipped outcomes carry the interview; degrees still matter to visas and licences, "
        "decreasingly to the market. <b>Judgement with accountability</b> — the willingness "
        "to say “this is right, and I answer for it” is the human act AI cannot perform and "
        "firms most underprice in juniors who show it early. And rarest: <b>trust across "
        "contexts</b> — holding a client, reading a room, carrying bad news, bridging a "
        "Lagos supplier and a London boardroom. Note who that favours: the relational "
        "attention our cultures train, the code-switching the diaspora lives daily, the "
        "voice this series has been rebuilding. The market that stopped buying our paperwork "
        "has started, without noticing, to price our upbringing. The platform data agrees: "
        "US postings requiring AI-literacy skills grew 70% YoY; 75% of companies say people "
        "skills matter <i>more</i> in the AI age; skills-first organisations grew AI talent "
        "pipelines 8.2×; and applicants connected to an employee are 3.6× more likely to be "
        "hired — network-building as measured arithmetic.", body),
]

# ================= 10 =================
story += [
    PageBreak(),
    Paragraph("10 · The Home-First Sequence", h2),
    Paragraph(
        "The old playbook sequenced abroad-first: leave at the bottom, climb over there — "
        "rational when foreign entry rungs were plentiful. The new market inverts the "
        "arithmetic. <b>Entry rungs still exist at home</b>: Nairobi, Lagos, Accra and Kigali "
        "firms still hire juniors and hand them real responsibility fast — the thing the "
        "Western market stopped doing. Meanwhile the door abroad now opens at <i>mid-level</i>, "
        "where thresholds clear easily and sponsors compete. Put the facts together: <b>two "
        "or three years of genuine responsibility at home, then entering the global ladder "
        "in the middle, increasingly beats arriving abroad at a bottom rung that no longer "
        "exists.</b>", body),
    Paragraph(
        "Run the numbers: the home-first candidate arrives above the £41,700 threshold "
        "instead of under it; skips the entry bloodbath; carries managed-real-projects proof "
        "no graduate scheme provides; and pays for none of it in survival-job years. The "
        "costs are real — home salaries during the building years, the WhatsApp optics of "
        "classmates who flew first, and the discipline of choosing employers who genuinely "
        "develop people. The macro data backs the sequence directly: advanced-economy "
        "hiring runs 20–35% below pre-pandemic while <b>India is +40% and the UAE +37%</b>; "
        "and the landmark AI-at-work study (5,172 support agents, mostly in the Philippines) "
        "found productivity gains land largest on the <i>less experienced</i> — AI "
        "compresses the junior learning curve fastest exactly where juniors still get "
        "hired. The direction is unmistakable, and it redeems something this "
        "library keeps finding: the diaspora's strongest position was never “escaped” — it "
        "is <b>bilingual in both economies</b>, and the new ladder now pays for the home "
        "years instead of discounting them.", body),
]

# ================= 11 =================
story += [
    PageBreak(),
    Paragraph("11 · What to Expect Next", h2),
    fig("expect.png",
        "Fig 9 — The five calls this report will stand behind across every AI scenario.",
        max_h=108 * mm),
    Paragraph(
        "Nobody knows AI's ceiling, so this report only makes calls that hold across "
        "scenarios. <b>The entry squeeze persists</b> — firms have learned to run leaner at "
        "the bottom, and organisational learning does not un-learn. <b>The mid-level "
        "shortage arrives</b> on the training-bottleneck logic — the single best positioning "
        "bet available. <b>Credentials deflate, proof appreciates</b> — monotonic in every "
        "scenario. <b>Migration politics tighten before easing</b> — electorates watching "
        "their own graduates idle will not liberalise junior sponsorship, while the same "
        "ageing electorates expand the shortage lists; ride the lists, not the vibes. And "
        "<b>reskilling becomes rent</b> — with 39% of core skills turning over in five "
        "years, learning is a standing charge, not a phase. Two more currents, without "
        "betting the house: <b>the third door is opening</b> — with 52% of professionals "
        "job-hunting and seekers outpacing openings at the highest rate since the pandemic, "
        "“founder” profiles grew 60% YoY and “creator” nearly 90% since 2021, with 4 in 10 "
        "Gen Z wanting self-employment; for a diaspora over-indexed on entrepreneurship, "
        "the squeezed ladder makes the built-your-own rung more rational. And <b>adoption "
        "lags exposure</b>: only 20.2% of OECD firms reported using AI in 2025 (52% of "
        "large firms, 17% of small) — the squeeze is sharpest at the prestige employers "
        "graduates queue for, and smaller firms remain the under-fished pond. What this "
        "report will "
        "<i>not</i> predict: which job titles are “safe”. The honest unit of safety is the "
        "level, the licence, and the proof.", body),

    Paragraph("12 · The African Advantage", h2),
    Paragraph(
        "The growing barbell's hands-and-heart end is where African corridors already run, "
        "with visas attached and AI structurally locked out. The trust-and-judgement premium "
        "prices the capacities our cultures train. The home-first sequence converts Africa's "
        "young labour markets from the thing you flee into <b>the continent's apprenticeship "
        "system</b> — the place the entry rung still exists — feeding the global mid-level "
        "shortage richer markets are manufacturing. And demography does the long arithmetic: "
        "the ageing world is running out of exactly the people the youngest continent "
        "produces. AI changes which door they enter through. It does not change that the "
        "doors, on a twenty-year view, need them more than ever. The diaspora's role: <b>the "
        "bridge</b> — the mid-level professional mentoring the junior at home across the "
        "gap; the chama funding a training contract instead of a generic master's; the Forum "
        "thread mapping which employers develop and which sponsors sponsor. The old ladder "
        "was climbed alone, in one country. The new one is crossed in networks, across two — "
        "and a diaspora is, by definition, the network that spans them.", body),
]

# ================= 13 =================
story += [
    PageBreak(),
    Paragraph("13 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First: some people mid-journey are on the wrong ladder, and kindness is saying "
        "so early.</b> The cousin two years into a generic degree chosen for the old market; "
        "the graduate burning their visa window on the vanished analyst intake; the family "
        "still selling land for repriced credentials — the sunk-cost instinct will keep them "
        "climbing toward a missing rung. Name where the ladder actually goes, grieve the "
        "plan briefly, re-route while the window is open. A hard conversation this year "
        "beats a survival-job decade.", body),
    Paragraph(
        "<b>Second: the entry squeeze is doing quiet damage this community should name.</b> "
        "Behind every “lazy graduate” joke at a family gathering is a young person with "
        "eighty applications into a market 45% smaller, judged by elders whose entry rung "
        "existed. The rejection arithmetic has changed; the shame machinery has not. A "
        "community that understands Fig 1 stops auditing its juniors and starts building "
        "them bridges — introductions, first contracts, portfolio commissions. Judge the "
        "market, not the child.", body),
    Paragraph(
        "<b>Third: the mid-level premium has an expiry date too.</b> This report's central "
        "bet — cross to mid, collect the shortage premium — is a decade's strategy, not a "
        "lifetime's. AI capability is not finished, and the judgement moat will be tested "
        "from below continuously. The durable posture is not a rung but a habit: re-skill "
        "annually, keep proof current, hold a licence where possible, maintain the "
        "two-economy network — and never let one country, one employer, or one ladder own "
        "your whole plan. That is the oldest diaspora skill there is.", body),
]

# ================= 14 =================
story += [
    Paragraph("14 · Method &amp; Limits", h2),
    Paragraph("This report combines payroll-data research, vacancy statistics, visa-policy "
              "records and employer surveys, as at 14 September 2026 — with the futures flag "
              "its forward sections require.", body),
]
story += bullets([
    "<b>The level-split findings</b> (~13% in the 2025 paper, ~19% by mid-2026; less-exposed "
    "peers flat; experienced flat to rising) are Brynjolfsson, Chandar &amp; Chen (Stanford; "
    "ADP payroll data) — US data, one large provider, relative-to-trend measures. Fig 1's "
    "bars are directional renderings, not exact magnitudes for the second and third rows.",
    "<b>The UK vacancy figures</b> (graduate postings −45% YoY; positions −33% in 2025 to "
    "the lowest since 2018; entry/junior −32% since late 2022) come from job-board and "
    "institute analyses with differing definitions; we cite the consistent direction. "
    "Attribution to AI specifically is partial — interest rates and post-pandemic correction "
    "contribute.",
    "<b>The threshold figures</b> (£38,700 → £41,700) are UK policy as amended July 2025; "
    "occupation and shortage-list thresholds differ, and other destinations vary — the UK is "
    "the emblematic case, not a universal quote.",
    "<b>The WEF projections</b> are employer <i>expectations</i> from a structured survey, "
    "not a forecast model. We use them for composition and direction.",
    "<b>The attribution debate is presented as live, because it is.</b> LinkedIn's Labor "
    "Market Report attributes the slow market to rates and uncertainty, finding similar "
    "trends across exposure levels; Stanford's revision finds the exposed-young gap "
    "persists after firm-shock controls but attenuated by education controls — a ~19% "
    "relative shortfall (−11% most-exposed quintiles vs +10% least), not an absolute "
    "decline; Denmark's linked-data study bounds average effects near zero for its window; "
    "the NY Fed adds remote-work mentoring loss as a rival channel. We treat the squeeze as "
    "fact and its causes as contested.",
    "<b>The migrant-outcome statistics</b> (France 11.7/6.9%; EU overqualification "
    "41.4/20.0%; Canada 32.6/19.1%; US 4.2/4.3%) use differing definitions of “immigrant” "
    "and are context, not a ranking — none isolates an AI effect.",
    "<b>The LinkedIn figures</b> (1.3m AI-enabled jobs; 600k data-centre roles; +70% "
    "AI-literacy postings; 75% people-skills; 8.2× and 3.6×; founder/creator growth; trades "
    "sentiment) are platform and commissioned-survey data with the selection biases of "
    "both. The BLS projections are US-only.",
    "<b>The 73% AI-screening figure</b> is from employer surveys of varying methodology; "
    "estimates range ~70–90%+. The direction — automated screening as the norm — is not in "
    "dispute.",
    "<b>Sections 07, 10, 11 and 12 are interpretive:</b> the mid-level-shortage thesis "
    "extrapolates the visible training bottleneck forward; home-first sequencing is strategy "
    "built on documented dynamics, not a measured cohort outcome; the five “expect” calls "
    "are judgement limited to scenario-robust claims.",
    "<b>Nothing here is career advice for a specific situation</b> — corridors, fields and "
    "licences differ enormously. And per this library's standing disclosure: AI was used in "
    "producing this research, under the same editorial and verification standards as every "
    "report — maximum tool, human voice, receipts kept.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Brynjolfsson, Chandar &amp; Chen, “Canaries in the Coal Mine” (Stanford Digital "
        "Economy Lab) and its 2026 update; LinkedIn's Labor Market Report 2026; a member-shared research dossier (“Jobs Before and After Generative AI”, Sept 2026) whose primary citations — ILO youth trends and GenAI exposure index, OECD adoption data, the Denmark NBER study, the QJE support-agent study, NY Fed advisories, INSEE, Eurostat, StatCan and BLS — we verified and cite; WEF Future of Jobs Report 2025; IES and HEPI on "
        "the UK graduate market; UK Skilled Worker threshold analyses; employer AI-screening "
        "surveys via industry reporting; and this library's prior measurement in the "
        "graduate-market, CV, visa, student-cost and AI reports. Full inline links in the "
        "web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, "
        "sit together, and bounce ideas. This research is part of an open library, free to "
        "read and share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/new-ladder-2026<br/>"
        "Companion reports: The Algorithm at the Border · The Graduate Job Market · The Name "
        "on the CV · Open-Door Countries<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
