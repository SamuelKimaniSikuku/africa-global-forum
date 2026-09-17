#!/usr/bin/env python3
"""Generate the AGF report PDF: The Leapfrog Test — AI and the Developing World (2026)."""

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
IMG = os.path.join(HERE, "leapfrog-test-2026", "img")
OUT = os.path.join(HERE, "leapfrog-test-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Leapfrog Test · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 17 September 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Leapfrog Test (2026)",
                      author="Africa Global Forum",
                      subject="AI and the developing world: employment, poverty, the rising value of education, and the university strategy for the class of 2030")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Leapfrog", h1),
    Paragraph("test.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Our two previous AI reports watched the wave from the departure lounge. This one "
        "turns around and looks at home. The paradox: the developing world has the least AI "
        "exposure on paper — 11% of jobs in low-income countries versus 34% in rich ones — "
        "and the most at stake in practice, because the ladder it planned to climb (call "
        "centres, back offices, services exports) runs straight through the work AI does "
        "best. Will unemployment rise? Will poverty increase? Does education become worth "
        "more, or less? And how should a student in Nairobi, Lagos or Accra choose a "
        "university for a market nobody has seen yet? The evidence, question by question.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("34% vs 11%", big_num), Paragraph("847m", big_num),
    Paragraph("85.3%", big_num), Paragraph("21.9%", big_num),
], [
    Paragraph("GenAI job exposure, rich<br/>versus low-income countries<br/>(ILO) — the asymmetry", big_lbl),
    Paragraph("people under the $3.00/day<br/>line in 2024 — most in<br/>Sub-Saharan Africa", big_lbl),
    Paragraph("of African employment is<br/>informal — work AI cannot<br/>reach, and formality never did", big_lbl),
    Paragraph("return per year of university<br/>in Sub-Saharan Africa —<br/>the highest on earth", big_lbl),
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
    fig("asymmetry.png",
        "Fig 1 — The ILO's refined global exposure index: the wave hits offices, and the "
        "developing world's employment is mostly not in offices.", max_h=88 * mm),
    Paragraph("Published September 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/leapfrog-test-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Every member of this network has a version of the same question waiting at home: a "
        "sibling choosing a degree, a cousin asking whether the BPO job is safe, parents "
        "asking whether school fees still make sense. The answers, evidence first:", body),
]
story += bullets([
    "<b>The exposure is asymmetric — and it cuts both ways.</b> The ILO finds 34% of "
    "employment in high-income countries in occupations with generative-AI exposure versus "
    "11% in low-income ones, with only 3.3% of jobs worldwide in the highest-exposure "
    "category. The developing world's farms and stalls are out of AI's reach — but the jobs "
    "that ARE exposed are precisely the modern, formal, exportable ones every development "
    "plan depends on.",
    "<b>Will unemployment rise? Mostly the wrong question.</b> With 85.3% of African "
    "employment informal, the unemployment rate will barely move. The real number: 10–12 "
    "million young Africans enter the labour market yearly against ~3 million formal jobs. "
    "AI threatens to freeze that 4-to-1 shortfall in place by automating the routine office "
    "work poor countries hoped to sell.",
    "<b>Will poverty increase? Not directly — but the escape routes narrow.</b> 847 million "
    "people — 10.4% of humanity — live under the $3.00/day line (2024). AI will not fire the farmer; the risk is slower "
    "exits — the services-export ladder (India's 5.4M IT-BPM workers, the Philippines' 1.8M "
    "BPO workers with ~1M roles at automation risk by 2030) is being pulled up just as "
    "Africa reaches for it. Expect inequality to widen before poverty moves.",
    "<b>Does education become worth more? Yes — with a twist.</b> Returns to university in "
    "Sub-Saharan Africa are 21.9% per year of schooling, the highest on earth. AI raises the "
    "value of what scarce educated people do while deflating the credential-alone. Education "
    "is worth more; generic education is worth less.",
    "<b>The strategy is a fork, not a verdict.</b> Choose fields where AI amplifies scarce "
    "professionals — health, agriculture, energy, engineering, teaching — or build for local "
    "problems; stack AI-fluency on any degree as the free second major. Ten rules inside.",
])
story += [
    Paragraph(
        "The mobile phone found Africa without landlines and made it the world leader in "
        "mobile money. AI now arrives at a continent without enough teachers, doctors or "
        "formal jobs. Whether it repeats the leapfrog or pulls up the ladder is the defining "
        "economic test of the next decade.", pull),
]

# ================= 02 =================
story += [
    Paragraph("02 · The Asymmetry", h2),
    Paragraph(
        "When the ILO mapped every occupation on earth against what generative AI can do, "
        "the exposure landed where the offices are: about one job in four worldwide, but 34% "
        "in high-income countries against 11% in low-income ones — and only 3.3% of world "
        "employment in the highest-exposure category, overwhelmingly clerical. Read naively, "
        "the developing world is safe: the farmer, the trader, the mason and the matatu "
        "driver do work AI cannot touch.", body),
    Paragraph(
        "Read properly, it is harsher. Exposure is where the productivity gains land too — "
        "the rich world's offices are about to get cheaper to run while the poor world's "
        "fields are not. And the exposed 11% is not a random 11%: it is the civil service, "
        "the banks, the telecoms, the BPO parks — the formal, tax-paying, exportable sliver "
        "every development strategy treats as the seed of the future economy. AI spares the "
        "developing world's present and aims at its planned future. Adoption is early "
        "everywhere — only 20.2% of OECD firms used AI in 2025 (52% of large firms, 17% of "
        "small) — which is exactly why the next five years of choices still matter.", body),
]
story += [
    Paragraph(
        "Two 2026 studies sharpen the asymmetry. The World Development Report 2026 splits "
        "exposure into halves: only 4.5% of developing-economy jobs are amenable to "
        "generative-AI AUTOMATION (versus 14.2% in high-income ones) — but 16.2% could see "
        "meaningful PRODUCTIVITY GAINS, nearly matching the rich world's 18.7%. The downside "
        "is three times smaller; the upside is almost the same size (modelled potentials, "
        "not observed layoffs). And the ILO–World Bank study of 135 countries, pointedly "
        "titled Disruption without Dividend, adds the timing problem: vulnerable clerical "
        "workers are often already online while the farmers and small firms who stand to "
        "gain mostly are not — the automation risk can arrive before the productivity "
        "benefit does. That sequencing, not the exposure percentage, is the number-one "
        "thing developing-country policy has to beat.", body),
]

# ================= 03 =================
story += [
    Paragraph("03 · The Ladder Being Pulled Up", h2),
    fig("ladder.png",
        "Fig 2 — The escape ladder that worked meets the machine that does the same work "
        "(NASSCOM, IBPAP, Philippine government statements).", max_h=110 * mm),
    Paragraph(
        "The one development strategy of the last thirty years that reliably worked without "
        "factories: India built a 5.4-million-worker IT-BPM industry on rich-world firms "
        "sending routine information work to cheaper, English-speaking graduates; the "
        "Philippines followed with a 1.8-million-worker, ~$40-billion BPO industry that "
        "became its economic crown jewel. No ports, no heavy industry, no mineral luck — "
        "just educated young people, connectivity and wage differences.", body),
    Paragraph(
        "African capitals have spent a decade climbing onto the same ladder — Kenya's "
        "Silicon Savannah added on the order of 20,000 BPO jobs in a single recent year, "
        "with Ghana, Rwanda, Senegal and Egypt running versions of the same play. The timing "
        "is the tragedy: generative AI's most proven skill is routine information work — "
        "exactly the ladder's bottom rungs. Estimates put around a million Philippine BPO "
        "roles at automation risk by 2030 (the planning secretary calls the figure possibly "
        "overstated — the debate itself is the point). What gets pulled up is not Africa's "
        "existing jobs; it is Africa's NEXT jobs.", body),
    Paragraph(
        "Update (September 2026): the warning stopped being theoretical. In India, the "
        "largest IT firms — an industry now counting around six million workers — added "
        "almost no net employees in the first nine months of fiscal 2026, and one major "
        "provider made its largest-ever staff reduction: a collapse in entry-level "
        "recruitment, not mass dismissal. In the Philippines, more than two-thirds of "
        "BPO association members are running AI pilots, clients press for AI-driven "
        "cost cuts, and investment has slowed. And freelance work flowing to developing "
        "economies fell sharply in 2025 (platform data cited by the World Bank; sector "
        "figures are industry-reported, flagged as such in Method). For Nairobi, Accra "
        "and Kigali this is the most relevant early-warning system on earth: watch "
        "Manila's and Bengaluru's headcounts the way farmers watch the sky.", body),
    Paragraph(
        "One counter-current: the QJE field experiment found support agents 15% more "
        "productive with an AI assistant, the largest gains going to the least experienced — "
        "in a Philippine-staffed operation. Read one way, automation in slow motion. Read "
        "the other, AI narrows the experience gap and makes the cheaper worker MORE "
        "competitive per dollar for as long as humans stay in the loop. Which reading wins "
        "will be decided market by market.", body),
]
story += [
    Paragraph(
        "The first hiring-demand evidence from a developing region points the same way: a "
        "World Bank analysis of South Asian online vacancies (Aug 2020–Feb 2025, dominated "
        "by India's urban white-collar market) found postings in the most AI-exposed AND "
        "substitutable occupations roughly 20% below other occupations after ChatGPT. "
        "Advertised demand, not employment — but the developing world's first measured "
        "entry-squeeze. The canary sings in Bangalore too.", body),
]

# ================= 04 =================
story += [
    Paragraph("04 · Will Unemployment Rise?", h2),
    fig("jobs_math.png",
        "Fig 3 — The honest arithmetic (AfDB, ILO). The formal-jobs crisis is not coming "
        "with AI — it was already here.", max_h=105 * mm),
    Paragraph(
        "The statistically honest answer: the unemployment rate will probably not move much "
        "— and that is not good news. Sub-Saharan Africa records some of the world's LOWEST "
        "youth unemployment rates (~8.4%) for a reason that flatters nobody: where there is "
        "no unemployment insurance, almost nobody can afford to be unemployed. 85.3% of "
        "African employment is informal, and informal work is nearly AI-proof. The rate is a "
        "rich-country instrument pointed at a poor-country economy; the ILO's 408-million "
        "global jobs gap is the truer gauge.", body),
    Paragraph(
        "The number that will move is the one already broken: 10–12 million young Africans "
        "enter the labour market yearly against roughly 3 million formal jobs — a 4-to-1 "
        "gap that predates ChatGPT. What AI threatens is the gap's closing mechanism: the "
        "classic first formal jobs — clerk, teller, data-entry operator, junior accountant, "
        "call-centre agent — are the highest-exposure occupations in the ILO index. The "
        "forecast is not mass unemployment; it is a longer queue for the same scarce formal "
        "doors, more educated young people absorbed downward into informality, and a "
        "widening gap between the credentialed and the connected few who cross. Readers of "
        "our New Ladder report will recognise the shape: the entry rung thins first, "
        "everywhere — the developing world simply had fewer rungs to begin with.", body),
]
story += [
    Paragraph(
        "Kenya's 2026 Economic Survey makes it concrete: of the 822,100 jobs the economy "
        "added in 2025, 87.2% were informal (KNBS; series excludes small-scale "
        "agriculture). Work is being created, in volume — but overwhelmingly outside the "
        "formal door AI now guards. And one measurement rule matters most: employment is "
        "not the same as an adequate income. A retrenched clerk who turns to irregular "
        "trading still counts as employed while earnings collapse — the honest dashboard "
        "tracks earnings, hours and job quality, not a rate that can FALL when discouraged "
        "people stop searching.", body),
]
story += [
    Paragraph(
        "The youth bulge multiplies every number here. Africa holds about 532 million "
        "people aged 15–35, and roughly 90% of employed young Africans work informally "
        "(Mastercard Foundation, 2026). In Eastern and Southern Africa alone, about 8 "
        "million enter the labour market yearly and fewer than one million secure waged "
        "jobs (World Bank). Whatever AI does to entry-level hiring lands on this cohort "
        "— which is why the composition of losses matters more than the count: a "
        "country can lose few jobs overall and still close the door that graduates, "
        "and especially young women, were relying on.", body),
]

# ================= 05 =================
story += [
    Paragraph("05 · Will Poverty Increase?", h2),
    fig("poverty_chain.png",
        "Fig 4 — The poverty question, link by link. 847 million under the $3.00 line "
        "(World Bank March 2026 update, 2021 PPP); nearly half of Sub-Saharan Africa.", max_h=150 * mm),
    Paragraph(
        "The World Bank\u2019s March 2026 update counts 847 million people — 10.4% of the world — under its $3.00/day line in 2024 (with a model-based 10.0% nowcast for 2026: a projection, not a survey). The extreme poor are overwhelmingly rural, informal and agricultural — the LEAST "
        "AI-exposed workers on earth. AI cannot fire people it never employed; there is no "
        "direct mechanism by which it throws the world's poorest out of work. The indirect "
        "mechanism is the one to watch: poverty falls through exits — the formal wage job, "
        "the services-export role, the remittance from abroad (which our research priced at "
        "an 8.78% corridor cost) — and AI narrows the first two directly while squeezing the "
        "third through the diaspora's own thinning entry rung. Slower exits mean poverty "
        "falling more slowly than it should, while AI's gains pile up on the connected, "
        "educated, urban and powered: a wider gap inside every developing country.", body),
    Paragraph(
        "Yet the counterweight is real. Poverty is a bundle of absences — no doctor, no "
        "tutor, no lawyer, no market information — and AI collapses the price of exactly "
        "these, delivered through the phone mobile money already put in the poorest hands. "
        "So: no, poverty will not surge because of AI — but whether it keeps FALLING depends "
        "on which force wins, the pulled-up ladder or the leapfrog.", body),
]
story += [
    Paragraph(
        "Two disciplines keep that answer honest. First, the counterweight has limits: a "
        "family earning KES 30,000 against a KES 28,000 essentials basket that loses 20% "
        "of its income sits KES 4,000 short a month — and even with a 10% cheaper basket, "
        "still KES 1,200 short. Cheaper services soften an income shock; they do not "
        "replace an income. Second, no defensible single number for AI-driven poverty "
        "exists — a credible estimate needs household incomes, affected occupations, "
        "replacement work, prices and transfers, and multiplying an exposure rate by a "
        "population is not it. This report refuses to invent one.", body),
]
story += [
    Paragraph(
        "And one channel the first edition under-weighted: the lost graduate job "
        "impoverishes households even when the graduate was never poor. One salaried "
        "earner often supports several dependants and pays siblings' school fees; when "
        "that income falls, local-shop spending drops, remittances to rural relatives "
        "stop, and children's education is the first cost cut. A short shock to one "
        "person becomes a long-term loss for a family. The offsets do not reach the "
        "same people automatically: extreme-poverty budgets are dominated by food, "
        "fuel, rent and transport — none of which AI meaningfully cheapens.", body),
]

# ================= 06 =================
story += [
    Paragraph("06 · The Leapfrog Case", h2),
    fig("leapfrog.png",
        "Fig 5 — Why the wave could lift instead of drown — stated as strongly as the "
        "evidence allows.", max_h=150 * mm),
    Paragraph(
        "Africa skipped the landline for mobile and the bank branch for M-Pesa, which moves "
        "value equal to roughly half of Kenya's GDP through phones. Leapfrogging is the "
        "documented national habit, and AI is the most leapfroggable technology ever "
        "shipped: no factory, no branch network — its capital requirement is a connection "
        "and its interface is human language. The continent that could never train enough "
        "teachers, doctors and agronomists can now put a competent first draft of each in "
        "every pocket at near-zero marginal cost.", body),
    Paragraph(
        "The value chain is climbable, and this network watches people climb it: from the "
        "ugly $2/hour annotation floor (exploitative AND a foothold, both true at once) to "
        "structured remote roles at $1,000–2,000 a month, to developers fine-tuning models "
        "for African languages, to founders building for problems the Valley cannot see. Add "
        "the demographic asymmetry — median age near 19, the youngest workforce on earth, "
        "while the ageing rich world runs short of exactly such people — and the leapfrog "
        "case stops sounding like a TED talk and starts sounding like arithmetic.", body),
    Paragraph(
        "And the study every optimist must sit with: a randomized experiment gave 640 "
        "Kenyan entrepreneurs GPT-4 business advice (2023 fieldwork; Management Science, "
        "July 2026) and found no detectable average improvement in revenue or profit — and "
        "the initially weakest businesses did nearly 10% WORSE, following fluent advice "
        "they lacked the cash or customers to implement, while stronger firms showed "
        "suggestive gains. The lesson is not that AI fails in Africa; it is sharper: "
        "advice is not capital, and the gains land first on those already ahead — the same "
        "concentration the IMF's 2026 intelligence-divide paper warns of at country level. "
        "The leapfrog is real; it is not automatic, and it lands unevenly.", body),
    Paragraph(
        "The pessimists' case is Section 03; the optimists' case is this section. Both are "
        "real, both are running, and no serious economist knows which wins. That is why this "
        "report is called a test.", pull),
]

# ================= 07 =================
story += [
    Paragraph("07 · The Constraints", h2),
    fig("constraints.png",
        "Fig 6 — What stands between the developing world and the leapfrog (SDG7 tracking "
        "2026; ITU Facts and Figures 2025).", max_h=125 * mm),
    Paragraph(
        "The June 2026 SDG7 update counts 655 million people without electricity in 2024 "
        "— more than 560 million of them in Sub-Saharan Africa — and no model capability "
        "reaches a phone that cannot charge. Connectivity stacks on top: internet use runs "
        "23% in low-income countries against 94% in high-income ones (36% for the ITU "
        "Africa region), and mobile broadband fails the affordability benchmark in about "
        "60% of low- and middle-income countries. The continent hosts a sliver of global data-centre capacity, so the "
        "leapfrog runs on rented rails: models trained, priced and governed elsewhere, "
        "payable in dollars. African languages remain a rounding error in training data, so "
        "the tools perform worst for the users who need them most. And the oldest constraint "
        "compounds them all: the engineers who could build local AI are the same individuals "
        "on every rich-world shortage list.", body),
    Paragraph(
        "The conclusion, without flinching: the leapfrog is possible, not promised. The "
        "countries that clear the constraints — Mission 300, the push to connect 300 million "
        "Africans to electricity by 2030, is the scale required — get the leapfrog. The "
        "countries that do not will consume AI as an import, and the value will flow the way "
        "it always has.", body),
    Paragraph(
        "Update (September 2026) — and, for the first time in this report, a position. "
        "The revised member dossier behind this update argues, and we agree after "
        "checking its citations, that current evidence most resembles CONCENTRATED "
        "GAINS in middle-income and urban economies (falling entry vacancies beside "
        "stable experienced hiring — the South Asian postings data, India's junior "
        "freeze and the Kenyan advice trial all point this way) combined with SLOW "
        "ADOPTION in low-income and rural ones, with broad access confined so far to "
        "sectors governments deliberately fund, such as health and agricultural "
        "extension. A judgement, not a forecast — test it by watching: the ratio of "
        "entry to experienced vacancies; median real earnings of workers under 30; BPO "
        "and IT headcounts (and the share of outsourcing revenue from AI-augmented "
        "versus labour-based contracts); and the poverty rate among urban households "
        "with a tertiary-educated head — which, in the concentrated-gains future, "
        "rises even while national poverty falls.", body),
]

# ================= 08 =================
story += [
    Paragraph("08 · Is Education Worth More Now?", h2),
    fig("education.png",
        "Fig 7 — Psacharopoulos & Patrinos (World Bank): a year of university in "
        "Sub-Saharan Africa raises earnings more than anywhere on earth.", max_h=95 * mm),
    Paragraph(
        "Step one, the baseline almost nobody in the anxiety-discourse knows: returns to "
        "education in Sub-Saharan Africa are the highest in the world — 21.9% per year of "
        "tertiary schooling against a world average near 16% — because educated people are "
        "scarce (tertiary enrolment near 9–10% versus ~40% worldwide). This is the opposite "
        "of the rich-world problem, where degrees are abundant and the graduate premium "
        "erodes.", body),
    Paragraph(
        "Step two, what AI does to the premium: it deflates the credential that certifies "
        "routine information-handling — the degree headed for data entry, basic bookkeeping "
        "or scripted support — while amplifying the professional whose scarce judgement it "
        "extends: the doctor supervising AI triage across three counties, the agronomist "
        "whose advice reaches a million farmers through a chatbot she trains, the teacher "
        "orchestrating AI tutors. In an economy where the educated are scarce, augmentation "
        "is worth more, not less. Education becomes worth more in the AI era — and the "
        "degree-as-paper worth less — at the same time. The 21.9% was always an average "
        "across both kinds of graduate; AI is prising the average apart.", body),
    Paragraph(
        "Three 2025–26 findings flesh out both halves. On the premium's persistence: the "
        "OECD's latest comparison shows tertiary-educated workers in Brazil and South "
        "Africa out-earning secondary-educated ones by more than 140%, and across 22 low- "
        "and lower-middle-income countries the ILO finds unemployment among "
        "tertiary-educated 15–29-year-olds FALLING 1.1 points over 2023–25 — four times "
        "the improvement for secondary graduates. On the learning itself, the experiments "
        "split exactly like the labour market: a Nigerian randomized evaluation of "
        "supervised after-school AI tutoring delivered about +0.3 standard deviations in "
        "six weeks — among the strongest cheap education interventions on record — while a "
        "Turkish high-school experiment found students who practised with an unguarded "
        "chatbot scored 17% WORSE on the unaided exam (a hint-giving tutor removed the "
        "harm). Same tool, opposite outcomes, one variable: whether the human is still "
        "doing the thinking.", body),
    Paragraph(
        "The certificate point, one level sharper: AI does not change the value of "
        "knowledge; it changes the value of the certificate as a SIGNAL. When anyone "
        "can produce a polished essay or working code in minutes, a submitted document "
        "proves less about its author. Employers respond by raising credential "
        "requirements or shifting to practical tests, oral examinations and portfolios "
        "of supervised work — and both responses reward the same thing: demonstrable "
        "competence that survives being questioned. A degree that builds that is worth "
        "more than before; a degree that provides only the paper is worth less.", body),
    Paragraph(
        "“Is university still worth it?” has different answers in London and "
        "Lagos. Where degrees are abundant, AI erodes the premium. Where degrees are "
        "scarce, AI multiplies what the degree-holder can do. Scarcity was always Africa's "
        "educational curse. In the AI era it quietly becomes the hedge.", pull),
]

# ================= 09 =================
story += [
    Paragraph("09 · The University Decision", h2),
    Paragraph(
        "The old playbook said: get ANY degree, because the paper itself opened formal "
        "doors. That playbook is dying. The new one has three moving parts.", body),
    Paragraph("Run the substitute-or-amplify fork on the local economy", h3),
    Paragraph(
        "Ask of any intended career: does AI do this job's core tasks, or does it extend "
        "the reach of the scarce person doing them? The amplify list is long and physical: "
        "medicine and nursing, agriculture and agronomy, energy and electrical engineering, "
        "construction and the licensed trades, teaching, logistics, water. The substitute "
        "list is the tragic one: generic business-administration, clerical tracks, routine "
        "accounting, the “computer packages” certificates — training aimed at "
        "exactly the office work AI eats first. The fork is not STEM-versus-arts; it is "
        "routine-versus-judgement.", body),
    Paragraph("Price the local university honestly against the foreign one", h3),
    Paragraph(
        "With the rich world's graduate rung thinning and its student doorways narrowing by "
        "policy, the study-abroad-at-any-cost premium is shrinking — while the local degree "
        "plus demonstrable AI-era skills plus a shipped project increasingly beats the "
        "foreign degree alone. The foreign university still wins for frontier "
        "specialisations and research careers. But it is now a considered purchase, not a "
        "default — and the student who builds locally first and goes abroad at master's "
        "level, funded and specialised, extracts more from both systems at a fraction of "
        "the family's risk.", body),
    Paragraph("Treat AI-fluency as the free second major", h3),
    Paragraph(
        "Nurse-plus-AI, agronomist-plus-AI, accountant-plus-AI each out-earn all three "
        "alone — and in a low-adoption economy, the first fluent person in any organisation "
        "becomes its de facto transformation officer, whatever the job title says. That is "
        "a promotion path no curriculum lists.", body),
]
story += [
    Paragraph("The vetting toolkit", h3),
    Paragraph(
        "Because \u201cchoose well\u201d is useless without a method: before paying anything, "
        "compare three realistic programmes (including one vocational or lower-cost "
        "route), read about 30 recent local vacancies for the occupations each leads to, "
        "and talk to recent graduates and employers. Then the method that works when no "
        "outcome data is published — and in most developing-country universities none "
        "is: find five recent graduates of each shortlisted programme and ask two "
        "questions: what are you doing now, and how long did it take? Five honest "
        "answers beat any brochure. Put three questions to the institution — which "
        "employers take placements, how is UNAIDED work assessed, is the qualification "
        "recognised by the professional body — because a vague answer is itself the "
        "data. Stress-test the financing against twelve months "
        "without a graduate job, using local starting-pay evidence rather than the salary "
        "on the poster. And treat institutional AI-marketing as noise: a UNESCO survey of "
        "200 universities across 19 Latin American and Caribbean countries found 87% using "
        "AI somewhere but only 26% with any formal AI strategy. Ask instead how the "
        "institution teaches AI use, examines UNAIDED competence, and trains its own "
        "lecturers.", body),
]
story += [
    fig("fields.png",
        "Fig 8 — Exposure by field: how much of each field's ENTRY-LEVEL tasks current "
        "AI can do (dossier assessment built on World Bank task categories, vacancy "
        "evidence and sector reporting; * = low direct, high indirect). Not a "
        "statistical ranking.", max_h=190 * mm),
    Paragraph(
        "Three patterns matter more than any row. The licence is the moat — "
        "accounting, law, health and certified trades keep the protected core even "
        "where routine work automates. Software is safe for those who can build and "
        "verify, not those who can only prompt — the distinction India's junior freeze "
        "is teaching in real time. And humanities are a route problem, not a subject "
        "problem: paired with teaching, research or a sector they work; aimed at "
        "generic office work they walk into the two HIGH rows.", body),
]

# ================= 10 =================
story += [
    Paragraph("10 · Ten Rules for the Class of 2030", h2),
    fig("rules.png",
        "Fig 9 — The first five rules; the second five below. Written for the student in "
        "the developing country — the mirror of the ten we wrote for the student leaving.",
        max_h=150 * mm),
]
story += bullets([
    "<b>1. Run the fork on your own economy.</b> Substitute or amplify — asked of the "
    "career here, not in California. Health, agriculture, energy, trades and teaching "
    "amplify; generic office-prep substitutes.",
    "<b>2. Don't train for the ladder being pulled up.</b> If BPO is the entry point "
    "available, take it — but climb immediately: quality assurance, team lead, workflow "
    "design, the parts that supervise the machine.",
    "<b>3. Stack AI-fluency on any degree — but keep unaided practice.</b> The tools "
    "are free and the multiplier compounds for forty years. The Turkish experiment's "
    "warning stands: students who let the chatbot do the thinking scored 17% worse "
    "without it. Attempt first, ask for hints, verify, then solve the next one alone.",
    "<b>4. Build for a local problem before you graduate.</b> A shipped solution — however "
    "small — is a portfolio, a possible business and a visa-independent asset at once.",
    "<b>5. Treat university as network and lab, not paper.</b> The credential deflates; "
    "the classmates, professors and projects compound.",
    "<b>6. Aim at the professions scarcity protects.</b> A country with one doctor per "
    "several thousand people cannot automate doctors; it can only amplify them. Licensed, "
    "physical, scarce — three properties AI respects.",
    "<b>7. Learn to sell what you know across borders without moving.</b> Remote work and "
    "the $1,000–2,000/month structured roles are the new middle rung between the $2 "
    "annotation floor and emigration.",
    "<b>8. If you go abroad, go up — not out.</b> Leave for a specific specialisation, "
    "funded, at postgraduate level, with a return thesis — not for a generic degree at the "
    "moment the doorway narrows.",
    "<b>9. Watch electricity, not headlines.</b> Whether your country clears the "
    "constraints — power, connectivity, compute — tells you more about your decade than "
    "any AI announcement.",
    "<b>10. Keep the family ledger honest.</b> University still pays 21.9% a year here — "
    "the best return the family can buy — IF rules 1–6 choose what it buys. The fees "
    "WhatsApp group deserves the fork, not the fear.",
])

# ================= 11 =================
story += [
    Paragraph("11 · What Governments and Universities Must Do", h2),
    Paragraph(
        "Students choose inside systems, and the systems have their own exam to sit. The "
        "checklist that decides which countries pass the leapfrog test:", body),
]
story += bullets([
    "<b>Power first, rhetoric later.</b> Mission 300 — 300 million more Africans connected "
    "by 2030 — is the single highest-leverage AI policy on the continent.",
    "<b>Buy compute access, not compute vanity.</b> Few developing countries need "
    "sovereign frontier models; all need negotiated cloud capacity, data-centre investment "
    "and survivable pricing — plus trustworthy data-protection law.",
    "<b>Fix the curriculum lag.</b> The fastest reform is not new AI faculties; it is "
    "threading the tools through the medicine, agriculture, education and engineering "
    "programmes that already exist.",
    "<b>Fund the language gap.</b> Kiswahili, Hausa, Yoruba, Amharic, Wolof: small money "
    "by global standards, transformative locally — and fixable without anyone's permission.",
    "<b>Regulate the annotation floor.</b> The $2/hour tier is the continent's AI "
    "sweatshop and its on-ramp simultaneously; lift the floor without burning the ramp.",
    "<b>Count honestly.</b> Track the formal-jobs gap, underemployment and the informal "
    "majority — the unemployment rate hides the story.",
])

# ================= 12 =================
story += [
    Paragraph("12 · The Home-Ground Advantage", h2),
    Paragraph(
        "The diaspora member reading this holds a position neither the cousin at home nor "
        "the local employer abroad quite sees. You have watched AI arrive in rich-world "
        "workplaces two or three years before it saturates home markets — you are, "
        "functionally, a time traveller with respect to your home economy's adoption "
        "curve. You hold rich-world savings against home-market costs. You know both the "
        "problems the Valley cannot see and the tools it built. Every previous wave — "
        "mobile, fintech, e-commerce — minted a cohort of diaspora returnees and remote "
        "co-founders who arbitraged exactly this gap.", body),
    Paragraph(
        "The practical forms are concrete: the professional abroad who spends a weekend a "
        "month making a sibling's business AI-literate; the remittance that buys a laptop "
        "and a course instead of only consumption; the mid-career specialist who takes the "
        "mid-level premium home, where scarcity makes it worth double; the Forum member who "
        "mentors three students through the ten rules — free to give, compounding for "
        "decades. The leapfrog, if it happens, will not be executed by governments alone. "
        "It will be executed by networks — and this is one.", body),
]

# ================= 13 =================
story += [
    Paragraph("13 · The Uncomfortable Part", h2),
]
story += bullets([
    "<b>Much of this report is forecast, and AI forecasts have aged badly in both "
    "directions.</b> The 2013 predictions that automation would erase half of all jobs "
    "were wrong; so were the 2023 assurances that nothing would change. This report joins "
    "its two AI siblings on the revisit-by-mid-2027 list.",
    "<b>The leapfrog framing flatters us, and we chose it anyway.</b> The harsher reading "
    "— that AI ends the labour-arbitrage development model outright and M-Pesa is a story "
    "about payments, not a general law of catching up — is held by serious people, not "
    "straw men.",
    "<b>The 21.9% education return is an average over people who got formal jobs in the "
    "old economy.</b> If AI thins the formal sector, yesterday's return may overstate "
    "tomorrow's — which is precisely why the strategy sections insist the return now "
    "depends on WHAT the degree contains.",
    "<b>This network exists because people left, and Rule 8 quietly argues that fewer "
    "should — or should leave differently.</b> We would rather name the tension than "
    "perform neutrality: the question was never whether to go, but when, at what rung, "
    "and with what plan.",
])

# ================= 14 =================
story += [
    Paragraph("14 · Method & Limits", h2),
]
story += bullets([
    "<b>Exposure and adoption:</b> ILO refined global index of occupational GenAI "
    "exposure (34%/11% split, ~25% world, 3.3% highest-exposure, clerical concentration); "
    "OECD adoption surveys (20.2% of firms, 2025). Exposure measures technical potential, "
    "not realised job loss.",
    "<b>Poverty:</b> World Bank $3.00/day (2021 PPP) line, March 2026 update — 847 "
    "million (10.4%) in 2024, model-based 10.0% nowcast for 2026; Sub-Saharan Africa near "
    "46% of its population and a majority of the global total. Estimates are lagged model "
    "updates, not live counts.",
    "<b>Labour markets:</b> ILO (85.3% African informality 2024; 408M global jobs gap; "
    "SSA youth unemployment ~8.4% with the insecurity caveat); AfDB (10–12M annual "
    "entrants vs ~3M formal jobs).",
    "<b>The services ladder:</b> NASSCOM (India ~5.4M), IBPAP and Philippine government "
    "statements (1.8M workers, ~$40B, ~1M at automation risk by 2030, with the official "
    "“may be overstated” caveat quoted); the QJE support-agent experiment "
    "(+15%, largest gains to the least experienced).",
    "<b>Education:</b> Psacharopoulos & Patrinos, World Bank global compilation (SSA "
    "tertiary 21.9%, primary 13.4%, secondary 10.8%). Private returns estimated on past "
    "graduates; the forward-looking caveat is stated.",
    "<b>Infrastructure and access:</b> SDG7 tracking update (June 2026) — 655M without "
    "electricity in 2024, over 560M in Sub-Saharan Africa; Mission 300 as the response; "
    "ITU Facts and Figures 2025 (23%/94% internet use, ~60% of low- and middle-income "
    "countries failing the broadband affordability benchmark).",
    "<b>2026 modelled and experimental evidence</b>, added from a member-shared dossier "
    "whose primary citations we verified and cite: WDR 2026 automation/productivity split "
    "(4.5%/16.2% vs 14.2%/18.7% — modelled potentials); ILO–World Bank Disruption without "
    "Dividend (135 countries); World Bank South Asia Development Update (Lightcast "
    "vacancies — advertised demand, not employment); KNBS Economic Survey 2026 (822,100 "
    "Kenyan jobs in 2025, 87.2% informal); Otis et al., Management Science 2026 (Kenyan "
    "GPT-4 RCT — null average, ~−10% weakest firms); IMF WP 2026/190; OECD Education at a "
    "Glance 2025 (>140% premium, descriptive not causal); ILO youth trends 2026; the "
    "Nigerian tutoring RCT (+0.3 SD, supervised) and Bastani et al., PNAS 2025 (−17% "
    "unaided); UNESCO IESALC, ministerial and TVET publications; ITU 2025.",
    "<b>Softened or unverifiable:</b> country-level BPO automation counts; African "
    "data-centre shares (order of magnitude only); the $2/hour and $1,000–2,000 figures "
    "are journalistic and platform-reported ranges. All forward-looking sections are "
    "analysis, not measurement.",
    "<b>Revised-dossier additions (17 Sep):</b> WDR 2026 high-risk task categories; "
    "Philippine/Indian sector signals via industry reporting (IBPAP pilots, India IT "
    "~6M with near-zero net adds in FY2026's first nine months, largest-ever "
    "reduction at one provider, 2025 fall in freelance flows) — industry-reported, "
    "flagged as such; Mastercard Foundation Africa Youth Employment Outlook 2026 "
    "(~532M aged 15–35, ~90% informal youth employment) and World Bank E/S-Africa "
    "data (~8M entrants vs <1M waged); the exposure-by-field table (author "
    "assessment); the household-transmission channel; the concentrated-gains "
    "judgement with test indicators. The five-graduates vetting method replaces our "
    "survey-denominator advice, which the dossier rightly calls unrealistic.",
    "<b>AI use in production:</b> drafted, charted and fact-checked with AI assistance "
    "under editorial control — the same tools it analyses. Every load-bearing number was "
    "verified against the primary source; the interpretation and errors are ours.",
])
story += [
    Spacer(1, 4 * mm),
    Paragraph(
        "Companion reports: The Algorithm at the Border (AI × moving abroad) and The New "
        "Ladder (jobs before and after AI) view the same wave from the migrant's side; The "
        "Uncounted Year and The Black Tax Ledger price the escape-route economics. All at "
        "africaglobalforum.com/reports. · Africa Global Forum · Research · 2026 · "
        "Free to read and share.", small),
]

doc.build(story)
print("PDF built:", OUT)
