#!/usr/bin/env python3
"""Generate the AGF report PDF: How Long Until It Was Worth It? (2026)."""

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
IMG = os.path.join(HERE, "succeeding-abroad-2026", "img")
OUT = os.path.join(HERE, "succeeding-abroad-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "How Long Until It Was Worth It? · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 12 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="How Long Until It Was Worth It? (2026)",
                      author="Africa Global Forum",
                      subject="How hard it really is for Africans to succeed abroad, and how long it takes")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])

story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("How Long Until It Was Worth It?", h1),
    Paragraph("How hard it really is for Africans to succeed abroad",
              S("sub", fontName="Helvetica-Oblique", fontSize=16, leading=20,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Getting a job abroad is easy. Getting <i>your</i> job is not. Four rungs, a measured timeline "
        "for each, and an honest read on which countries actually let an African arrival climb them.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("70.9%", big_num), Paragraph("41.4%", big_num),
    Paragraph("17%", big_num), Paragraph("1 in 5", big_num),
], [
    Paragraph("of immigrants are<br/>employed — getting a<br/>job is not the problem", big_lbl),
    Paragraph("work below the level<br/>they are qualified for", big_lbl),
    Paragraph("pay gap remaining<br/>after ten years", big_lbl),
    Paragraph("of their children reach a<br/>higher-skilled job than<br/>their father", big_lbl),
]], colWidths=[CONTENT_W / 4] * 4)
kpi.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), INK),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 14),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story += [kpi, Spacer(1, 6 * mm)]
story += [fig("rungs.png",
              "The four rungs of succeeding abroad, with the measured outcome on each "
              "(OECD; Eurostat; OECD Catching Up?).")]
story += [Paragraph(
    "Published August 2026 by Africa Global Forum · "
    "africaglobalforum.com/reports/succeeding-abroad-2026", small), PageBreak()]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "“Will I succeed abroad?” is the question underneath every migration decision, and it is "
        "almost never answered with numbers. It can be. The research measures four separate things, and "
        "they have very different answers.", body),
]
story += bullets([
    "<b>Getting a job is easy.</b> Across the OECD, <b>70.9% of immigrants are employed</b> against 72.1% "
    "of the native-born — and immigrants actually <i>participate</i> in the labour force at a slightly "
    "<i>higher</i> rate, 77% against 76%.",
    "<b>Getting the job you trained for is hard.</b> <b>41.4% of non-EU citizens in the EU work below the "
    "level they are qualified for</b> — the highest rate of any group.",
    "<b>Getting paid like a local is harder still, and never finishes.</b> Immigrants earn <b>34% less</b> "
    "than native-born workers of the same age and sex on arrival, <b>21% less at five years</b>, <b>17% "
    "less at ten</b> — and there the curve flattens.",
    "<b>The biggest return lands on your children, but it is not automatic.</b> Children of immigrants gain "
    "<b>1.3 more years of schooling than their own parents</b> against 0.7 for children of the native-born "
    "— yet <b>only 1 in 5</b> of those with non-EU-born parents ends up in a higher-skilled occupation than "
    "their father held.",
    "<b>Which country you choose changes the answer more than anything you personally do.</b> Five-year "
    "exit rates run from <b>15% in the United States to 75% in the Netherlands</b>; the government fee bill "
    "for a family of four runs from <b>$510 to $122,000</b>; time to citizenship from <b>3 years to 11</b>.",
])
story += [Paragraph(
    "Succeeding abroad is not one achievement. It is four, they take different amounts of time, and "
    "most people only plan for the first one.", pull)]

# ================= 02 =================
story += [
    Paragraph("02 · The Four Rungs", h2),
    Paragraph(
        "The cover chart is the whole report in one image. Most migration advice, and almost all "
        "recruitment marketing, is about rung one. That is the rung that is <i>already easy</i>. The "
        "difficulty is concentrated in rungs two and three, and the payoff is concentrated in rung four — "
        "which arrives twenty years after the decision that caused it.", body),

    PageBreak(),
    Paragraph("03 · Rung 1 — A Job", h2),
    fig("job_vs_right_job.png",
        "Fig 2 — Employment against skill match (OECD; Eurostat). The two numbers describe "
        "different regions and cannot be combined — but they describe the same experience.",
        max_w=150 * mm),
    Paragraph(
        "The employment gap between immigrants and the native-born across the OECD is <b>1.2 percentage "
        "points</b>. That is very close to nothing. And on labour force participation — working or actively "
        "looking — immigrants come out <i>ahead</i>: 77% against 76%.", body),
    Paragraph(
        "This deserves stating plainly because it contradicts the political narrative in most destination "
        "countries. <b>Immigrants are not failing to work. They work at essentially the same rate as "
        "everybody else, and they look for work harder.</b> There is also genuine progress: in the EU, the "
        "employment rate of non-EU immigrants rose <b>6.6 points in eight years</b>, from 59.4% in 2017 to "
        "66.0% in 2025.", body),
    fig("eu_progress.png",
        "Fig 3 — Employment rate of non-EU immigrants in the EU (CReAM/RFBerlin).", max_w=145 * mm),
    Paragraph(
        "<b>Verdict on rung one: easy, and getting easier.</b> If your fear about moving is that you will "
        "not find work, the data says that is the wrong thing to be afraid of.", body),
]

# ================= 04 =================
story += [
    Paragraph("04 · Rung 2 — The Right Job", h2),
    Paragraph(
        "Here is where it breaks. <b>41.4% of non-EU citizens in the EU are over-qualified for the job they "
        "hold.</b> Highest of any group, and highest of all among non-EU-born women. It has improved slowly "
        "— from 45.9% in 2014 to 39.6% in 2024 for the non-EU-born — but it remains the defining feature of "
        "migrant employment in Europe.", body),
    Paragraph(
        "Now put that beside who Africans abroad actually are: <b>46% of sub-Saharan African immigrants in "
        "the US hold a bachelor's degree or higher, and about 61% of Nigerian-born immigrants</b> — well "
        "above both the foreign-born and native-born averages.", body),
    Paragraph(
        "The people most likely to be working below their training are the people who arrived with the "
        "most training. That is the whole difficulty of succeeding abroad, in one sentence.", pull),
    Paragraph(
        "The mechanism is not mysterious. Qualifications earned in Africa are frequently not recognised, "
        "not understood, or not trusted by employers who have no way to benchmark them. A Nigerian pharmacy "
        "degree and a British one are not treated as interchangeable, and the process for converting one "
        "into the other is slow, expensive and administratively brutal. Meanwhile rent is due.", body),
    Paragraph(
        "<b>Verdict on rung two: hard, and it is the rung that decides everything above it.</b> Credential "
        "conversion is the single highest-return administrative act available to an African professional "
        "abroad, and it is boring enough that most people postpone it until the first job has already set "
        "their trajectory.", body),

    Paragraph("05 · Rung 3 — Equal Pay", h2),
    fig("earnings_clock.png",
        "Fig 4 — The immigrant earnings gap over time, across the 15 OECD countries with comparable "
        "data (OECD International Migration Outlook 2025)."),
    Paragraph(
        "On arrival, an immigrant earns <b>34% less</b> than a native-born worker of the same age and sex. "
        "After five years, <b>21% less</b>. After ten, <b>17% less</b>. And then the line flattens.", body),
    Paragraph(
        "<b>First, most of the closing happens early.</b> Thirteen of the seventeen points close in the "
        "first five years; only four more close in the next five. The window in which your position "
        "improves fastest is the window in which you are newest, least settled and most likely to accept "
        "whatever is offered.", body),
    Paragraph(
        "<b>Second, and more importantly: two-thirds of the gap is not direct discrimination.</b> The OECD "
        "finds it is composition — immigrants are concentrated in lower-paying <i>sectors</i> and "
        "lower-paying <i>firms</i>. And the gap narrows mainly because immigrants move to better-paying "
        "firms and sectors over time.", body),
    Paragraph(
        "The gap does not close because employers eventually decide to pay you fairly. It closes because "
        "you leave.", pull),
]

# ================= 06 =================
story += [
    Paragraph("06 · Rung 4 — Your Children", h2),
    fig("next_generation.png",
        "Fig 5 — Intergenerational mobility, European OECD countries (OECD, Catching Up? "
        "Intergenerational Mobility and Children of Immigrants)."),
    Paragraph(
        "The honest answer to “was it worth it?” is frequently: <b>not for you — for them.</b> "
        "Children of immigrant parents gain <b>1.3 more years of schooling than their own parents</b>, "
        "nearly double the 0.7-year gain among children of the native-born. In every country studied, "
        "children of low-educated immigrants do better than their parents.", body),
    Paragraph(
        "But it is not a guarantee. <b>Only about 1 in 5 people with non-EU-born parents ends up in an "
        "occupation requiring a higher skill level than their father's.</b> Children of immigrants also "
        "show lower attainment and weaker learning outcomes than children of native-born parents in most "
        "European OECD countries.", body),
    Paragraph(
        "For African families specifically there is a complication worth naming: <b>the first generation "
        "often arrives highly educated and lands in a job below its level.</b> When the comparison for the "
        "second generation is the parent's <i>job</i> rather than the parent's <i>qualification</i>, "
        "mobility looks stronger than it is. When it is measured against the qualification, some second "
        "generations are running to stand still.", body),

    PageBreak(),
    Paragraph("07 · The Timeline", h2),
    fig("timeline.png",
        "Fig 6 — The measured milestones. Sources as cited throughout; the line between them is drawn, "
        "the points are published."),
]
story += bullets([
    "<b>Years 0–2, the shock.</b> Worst pay, worst job match, highest costs, thinnest network. Nearly "
    "everything people describe as “failing abroad” is this phase being mistaken for the destination.",
    "<b>Years 0–5, the sorting.</b> Between 15% and 75% of all arrivals leave, depending overwhelmingly on "
    "the country. This is also when the earnings gap closes fastest.",
    "<b>Year 5, the first real gate.</b> Permanent residence becomes possible in Germany, Ireland, France "
    "and the Netherlands. The pay gap is down to 21%.",
    "<b>Year 8, convergence.</b> Study-route and work-route migrants stop looking different. Most "
    "settlement clocks have matured.",
    "<b>Year 10 and beyond, the plateau.</b> The gap settles near 17% and stops moving. Whatever return is "
    "left belongs to the next generation.",
])
story += [Paragraph(
    "<b>So: roughly five years to security, ten years to your economic ceiling, and one generation to the "
    "full return.</b> Anyone selling a faster version of this is selling something.", body)]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · Which Countries Deliver", h2),
    fig("scorecard.png",
        "Fig 7 — AGF's scorecard, built from the sourced figures across this report and its "
        "companions. A judgement, not a measured index — the underlying data is cited, the weighting "
        "is ours.", max_w=150 * mm),
    Paragraph(
        "<b>Germany is the best place to arrive and one of the worst places to stay.</b> It scores top on "
        "entry (the Opportunity Card lets you come without a job offer), top on cost (€0 tuition, low fees) "
        "and top on speed to permanence (citizenship in five years, three with strong integration). And "
        "then <b>67% of arrivals leave within five years</b>. Whatever Germany is doing to attract people, "
        "it is not converting them.", body),
    Paragraph(
        "<b>France quietly outperforms its reputation.</b> Cheap degrees, moderate fees, five-year "
        "citizenship, and a <b>26% five-year exit rate</b> — the lowest in Europe. People who go to France "
        "stay in France.", body),
    Paragraph(
        "<b>The Netherlands is the sharpest warning on this chart.</b> High salary thresholds, a hard age "
        "cliff at 30 — and a <b>75% five-year exit rate</b>, the highest in the OECD. Three out of four "
        "people who move there are gone within five years.", body),
    Paragraph(
        "And the UK, still the default in most African family conversations, scores worst overall — driven "
        "by a fee burden of £77,414 for a family of four on the 10-year route and the longest settlement "
        "clock on the list. What it still has is language, degree recognition across Anglophone Africa, and "
        "the densest African professional networks anywhere. Those are real. Just price them.", body),
]

# ================= 09 =================
story += [
    Paragraph("09 · What Actually Moves It", h2),
    Paragraph("Sorted by how much difference each makes, based on the effect sizes in the data:", body),
]
story += bullets([
    "<b>Which country you pick.</b> Larger than any personal factor measured here. A 60-point spread in "
    "five-year retention, a 240-fold spread in fee burden, an eight-year spread in time to citizenship.",
    "<b>Whether your qualification is recognised.</b> This is the difference between rung one and rung two, "
    "and it is where 41.4% of people get stuck.",
    "<b>Which sector and firm you land in first.</b> Two-thirds of the pay gap. And it compounds: the first "
    "job sets the second.",
    "<b>Whether you move employers deliberately.</b> The gap closes because people switch, not because they "
    "wait.",
    "<b>How long you stay.</b> The curve rewards years — up to about ten, after which it stops.",
    "<b>Language.</b> Not measured directly here, but it gates entry to the higher-paying sectors in every "
    "non-anglophone country on the scorecard. Germany is the clearest case: admitted in English, employed "
    "in German.",
])
story += [Paragraph(
    "Notice what is not on that list: working harder. Every immigrant group in this data already "
    "participates in the labour market at above-native rates. Effort is not the binding constraint, and "
    "telling people otherwise is one of the more damaging things the diaspora tells itself.", body)]

# ================= 10 =================
story += [
    Paragraph("10 · Who Has It Hardest", h2),
]
story += bullets([
    "<b>Women.</b> Over-qualification is highest of all among non-EU-born women. They carry the skills "
    "penalty and the caring load simultaneously.",
    "<b>Mid-career arrivals.</b> Arriving at 35 with fifteen years of experience means having the most to "
    "convert and the least time to convert it.",
    "<b>Regulated professions.</b> Doctors, nurses, lawyers, engineers, accountants, teachers — the harder "
    "the licence, the longer the detour. A software engineer can be hired on a portfolio; a pharmacist "
    "cannot.",
    "<b>People in small communities.</b> Networks do a large share of the hiring in every country. A "
    "Malawian in a small European city has thinner support than a Nigerian in Houston, and it shows up in "
    "outcomes.",
    "<b>Those in the Gulf.</b> Nearly 7 million Africans live in Asia, largely in states with no realistic "
    "citizenship pathway at all. Rungs three and four are not available at any price there — the ladder "
    "simply ends at two.",
])

# ================= 11 =================
story += [
    Paragraph("11 · The Playbook", h2),
]
story += bullets([
    "<b>Choose the country for retention and permanence, not prestige.</b> This is the biggest lever you "
    "have and you only get to pull it once. A country where 75% leave in five years is telling you "
    "something.",
    "<b>Start credential conversion before you move, or in month one.</b> Not year three. The 41.4% figure "
    "is people who postponed it and then could not afford to stop working.",
    "<b>Treat the first job as a five-year decision, not a survival decision.</b> Two-thirds of the pay gap "
    "is sector and firm. Where a choice exists, take the lower-paying job in the higher-paying sector.",
    "<b>Plan to switch employers at least twice in the first five years.</b> That is the documented "
    "mechanism by which the gap closes. Loyalty to your first employer abroad is expensive.",
    "<b>Learn the language to working level, not conversational.</b> In Germany, the Netherlands and "
    "France, this is the gate to the sectors that pay.",
    "<b>Judge yourself against year five, not year one.</b> The shock phase is the phase, not the outcome. "
    "And if you do leave, half of Europe's arrivals do the same — that is the statistically ordinary "
    "choice, not a failure.",
    "<b>Be explicit with yourself about rung four.</b> If the real return is your children, then school "
    "choice, language and network matter more than your own promotion. Many families discover this after "
    "optimising for the wrong rung for a decade.",
])

# ================= 12 =================
story += [
    Paragraph("12 · Method &amp; Limits", h2),
    Paragraph(
        "<b>What this report is:</b> a synthesis of OECD, Eurostat and national data on immigrant "
        "labour-market outcomes, assembled into a four-rung model and a timeline. Data as at "
        "12 August 2026.", body),
]
story += bullets([
    "<b>Almost none of this data is Africa-specific.</b> The OECD and Eurostat series cover all immigrants "
    "or all non-EU citizens. African migrants are inside those numbers, not separated out. Where "
    "African-specific data exists — education levels, diaspora size — we say so and cite it.",
    "<b>“Success” here is economic.</b> Nothing on this ladder measures safety, belonging, dignity, family "
    "closeness or whether people are glad they went. Those matter at least as much and this report is "
    "silent on them.",
    "<b>The earnings curve interpolates.</b> The published points are arrival, five years and ten years — "
    "34%, 21% and 17%. The years between are drawn. <i>(Our earlier report quoted roughly 23% at five years "
    "from a proportional description; the directly published figure is 21%, used here.)</i>",
    "<b>The Fig 7 scorecard is AGF's judgement</b>, not a measured index. The inputs are cited; the 1–5 "
    "weighting is editorial and reasonable people would score it differently.",
    "<b>Exit rates cover different cohorts</b> — European figures for 2010–14 arrivals, US and Canadian for "
    "2010–19 — and “exit” conflates returning home with moving to a third country.",
    "<b>Intergenerational figures are European OECD averages</b> and mask enormous country variation. The "
    "“1 in 5” occupational-mobility figure compares to the <i>father's</i> occupation specifically.",
    "<b>Selection effects run through everything.</b> People who stay are not a random sample of people who "
    "arrived, so ten-year outcomes describe survivors.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "OECD International Migration Outlook 2025, including Immigrant integration: the role of firms; "
        "OECD, Catching Up? Intergenerational Mobility and Children of Immigrants; Eurostat migrant "
        "integration statistics; CReAM/RFBerlin on EU migrant employment; OECD on return migration. "
        "Full inline links in the web edition.", small),
    Spacer(1, 6 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=8),
]
story += [callout(
    "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit together, "
    "and bounce ideas. This research is part of an open library, free to read and share. The Forum itself "
    "is by application.<br/><br/>"
    "Read the web edition with live source links: africaglobalforum.com/reports/succeeding-abroad-2026<br/>"
    "Built on: The Diaspora, Counted · Where the Door Is Actually Open · The Visa Treadmill<br/>"
    "Apply to join: africaglobalforum.com", bg=INK)]

doc.build(story)
print("wrote", OUT)
