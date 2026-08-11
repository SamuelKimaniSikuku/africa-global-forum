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
IMG = os.path.join(HERE, "visa-treadmill-2026", "img")
OUT = os.path.join(HERE, "visa-treadmill-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Visa Treadmill · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Fees as at 11 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Visa Treadmill — What It Costs to Stay Legal (2026)",
                      author="Africa Global Forum",
                      subject="Mandatory government fees from arrival to citizenship, 26 countries")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])

story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Visa Treadmill", h1),
    Paragraph("What It Costs to Stay Legal",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "A family of four on the UK’s 10-year route pays <b>£77,414</b> in Home Office fees "
        "before anyone holds a passport — and it does not arrive as a monthly bill. It arrives as "
        "six sudden five-figure demands. Every number here comes from a published government fee schedule.",
        lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("£77,414", big_num), Paragraph("£14,683", big_num),
    Paragraph("62%", big_num), Paragraph("26", big_num),
], [
    Paragraph("total Home Office bill,<br/>family of four, 11 years", big_lbl),
    Paragraph("due every 30 months,<br/>in one transaction", big_lbl),
    Paragraph("of each renewal is<br/>health surcharge", big_lbl),
    Paragraph("countries built on the<br/>same methodology", big_lbl),
]], colWidths=[CONTENT_W / 4] * 4)
kpi.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), INK),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 14),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story += [kpi, Spacer(1, 6 * mm)]

story += [fig("uk_milestones.png",
              "Fig 1 — The six moments the money is actually due on the UK 10-year route. "
              "The dashed line is the same total spread evenly across 11 years: mathematically "
              "correct, practically misleading.")]

story += [Paragraph(
    "Published August 2026 by Africa Global Forum · africaglobalforum.com/reports/visa-treadmill-2026",
    small), PageBreak()]

# ================= 01 =================
story += [
    Paragraph("01 · The Number to Pin", h2),
    Paragraph(
        "A family of four working through the UK’s 10-year family and private life route to British "
        "citizenship — two adults, two children, starting from an initial 30-month grant and renewing "
        "every 2.5 years until settlement, then naturalising — faces a total Home Office bill of "
        "<b>£77,414</b> across the full 11-year journey, using fees published on GOV.UK under the "
        "8 April 2026 schedule.", body),
    Paragraph(
        "That figure covers government fees only: application charges, the Immigration Health Surcharge "
        "(IHS), Indefinite Leave to Remain (ILR), and naturalisation. It excludes legal fees, translation "
        "costs, English-language certification, and priority-service upgrades — all of which push the "
        "real-world total meaningfully higher.", body),
    Paragraph("Every fee cited here is a published government rate. The build is fully auditable "
              "— and it runs for 25 other countries too.", pull),
    Paragraph(
        "Across all 26 countries in this report, the all-in family-of-four total ranges from roughly "
        "<b>$510 (Morocco)</b> to <b>$122,000 (Nigeria)</b>, with the UK near the top of that global "
        "range at approximately <b>$104,509</b>.", body),
]

# ================= 02 =================
story += [
    Paragraph("02 · Why the 10-Year Route, Specifically", h2),
    Paragraph(
        "Most diaspora families outside the UK’s five-year “straightforward” spousal or work "
        "routes end up here by default — not by choice. The 10-year family and private life route exists "
        "for people who do not meet the strict financial or English-language thresholds of the 5-year route, "
        "or who have had a visa refusal, a relationship breakdown, or a gap in lawful residence.", body),
    Paragraph(
        "Instead of two 30-month grants totalling 5 years, applicants are placed on repeat 30-month grants "
        "for a full decade before they can even apply for ILR. That means <b>four separate fee-paying events "
        "before settlement, then a fifth (ILR) and a sixth (naturalisation)</b> — each one a full-price, "
        "non-refundable government transaction.", body),
    Paragraph(
        "This structural detail is the whole story. The 10-year route isn’t merely slower in years "
        "— it doubles the number of times a family must pay Home Office fees and surcharges, while "
        "offering no fee discount for repeat applicants.", body),
]

# ================= 03 =================
story += [
    Paragraph("03 · The Fee Build, Step by Step", h2),
    Paragraph("Step 1 — Initial application (2 adults + 2 children, 30 months)", h3),
    table([
        [Paragraph("Item", th), Paragraph("Rate (per person)", th), Paragraph("Family of 4", th)],
        [Paragraph("Leave to remain — family/private life application fee", cell),
         Paragraph("£1,407", cell), Paragraph("£5,628", cell)],
        [Paragraph("Immigration Health Surcharge — adults, £1,035/yr × 2.5 yrs", cell),
         Paragraph("£2,587.50", cell), Paragraph("£5,175", cell)],
        [Paragraph("Immigration Health Surcharge — children, £776/yr × 2.5 yrs", cell),
         Paragraph("£1,940", cell), Paragraph("£3,880", cell)],
        [Paragraph("Subtotal, initial application", cell_b), Paragraph("", cell),
         Paragraph("£14,683", cell_b)],
    ], [95 * mm, 40 * mm, 35 * mm]),
    Spacer(1, 3 * mm),
    Paragraph(
        "The IHS annual rates (£1,035 standard, £776 reduced for under-18s and students) come "
        "directly from the Home Office’s published surcharge guidance, current since February 2024 and "
        "left unchanged by the April 2026 fee uplift. Both the application fee and the surcharge are paid in "
        "one transaction at the point of submission — there is no instalment option.", body),

    Paragraph("Step 2 — Extensions 2, 3 and 4 (every 2.5 years)", h3),
    Paragraph(
        "Assuming the family composition and fee schedule stay flat — a conservative assumption, since "
        "fees have risen almost every year — each of the three remaining 30-month extensions repeats the "
        "same £14,683 charge. <b>Running total after four grants of leave (10 years of temporary status): "
        "£58,732.</b>", body),

    Paragraph("Step 3 — Indefinite Leave to Remain, year 10", h3),
    table([
        [Paragraph("Item", th), Paragraph("Rate (per person)", th), Paragraph("Family of 4", th)],
        [Paragraph("ILR application fee (up from £3,029 in April 2026)", cell),
         Paragraph("£3,226", cell), Paragraph("£12,904", cell)],
        [Paragraph("Life in the UK Test (2 adults only)", cell),
         Paragraph("£50", cell), Paragraph("£100", cell)],
        [Paragraph("Subtotal, ILR", cell_b), Paragraph("", cell), Paragraph("£13,004", cell_b)],
    ], [95 * mm, 40 * mm, 35 * mm]),
    Spacer(1, 3 * mm),
    Paragraph(
        "ILR applicants are exempt from the IHS — settlement is the one point in the process where that "
        "charge disappears, and the only relief point in an otherwise unbroken run of full-price applications. "
        "The exemption is conditional: if the settlement application fails and limited leave is granted "
        "instead, the surcharge becomes payable for that grant.", body),

    Paragraph("Step 4 — Naturalisation and child registration", h3),
    table([
        [Paragraph("Item", th), Paragraph("Rate", th), Paragraph("Family of 4", th)],
        [Paragraph("Naturalisation, adult: £1,709 + £130 citizenship ceremony", cell),
         Paragraph("£1,839", cell), Paragraph("£3,678", cell)],
        [Paragraph("Child registration as British citizen (if not automatically British)", cell),
         Paragraph("£1,000", cell), Paragraph("£2,000", cell)],
        [Paragraph("Subtotal, citizenship stage", cell_b), Paragraph("", cell),
         Paragraph("£5,678", cell_b)],
    ], [95 * mm, 40 * mm, 35 * mm]),
    Spacer(1, 3 * mm),
    Paragraph(
        "A rare piece of good news: the child registration fee <i>fell</i> in April 2026, from £1,214 to "
        "£1,000 — the only line in this entire build that moved in the family’s favour. And "
        "children born in the UK <i>after</i> a parent is granted ILR are automatically British and need no "
        "registration at all, so a family whose children qualify that way shaves £2,000 off the total.", body),

    Paragraph("The full 11-year total", h3),
    table([
        [Paragraph("Stage", th), Paragraph("Timing", th), Paragraph("Family-of-4 cost", th)],
        [Paragraph("Initial application", cell), Paragraph("Year 0", cell), Paragraph("£14,683", cell)],
        [Paragraph("Extension 1", cell), Paragraph("Year 2.5", cell), Paragraph("£14,683", cell)],
        [Paragraph("Extension 2", cell), Paragraph("Year 5", cell), Paragraph("£14,683", cell)],
        [Paragraph("Extension 3", cell), Paragraph("Year 7.5", cell), Paragraph("£14,683", cell)],
        [Paragraph("ILR (settlement)", cell), Paragraph("Year 10", cell), Paragraph("£13,004", cell)],
        [Paragraph("Citizenship", cell), Paragraph("~Year 11", cell), Paragraph("£5,678", cell)],
        [Paragraph("Grand total", cell_b), Paragraph("", cell), Paragraph("£77,414", cell_b)],
    ], [95 * mm, 40 * mm, 35 * mm]),
    Spacer(1, 3 * mm),
    Paragraph(
        "This excludes legal or immigration adviser fees (commonly £1,500–£4,000 per application "
        "if used), English-language testing (£150–£200 per adult), certified translations, "
        "biometric enrolment, and optional priority processing. A family using a solicitor at each of the six "
        "fee-paying stages could realistically add another <b>£15,000–£25,000</b> on top of the "
        "£77,414 government baseline.", body),
]

# ================= 04 =================
story += [
    Paragraph("04 · The Cash-Flow Shock", h2),
    Paragraph(
        "The headline £77,414 already sounds large. What it hides is <i>timing</i>. The Immigration Health "
        "Surcharge is not billed annually like a subscription — it is calculated for the entire length of "
        "leave being applied for and charged as a single lump sum at the point of submission.", body),
    fig("renewal_split.png",
        "Fig 2 — Inside each renewal. Nearly two-thirds is health surcharge, paid in full on day one "
        "for coverage stretching 30 months into the future.", max_w=125 * mm),
    Paragraph(
        "A family renewing a 30-month grant does not pay the bill as it accrues. The whole £14,683 "
        "— which would be about <b>£490 a month</b> if it were spread across the 30 months it covers "
        "— falls due in a single transaction, on a single day, before they can submit the application at "
        "all. If that family’s take-home income is, say, £3,500 a month, the £14,683 represents "
        "<b>over four months of net income, extracted in one payment, once every 2.5 years</b>, with no "
        "government financing option.", body),
]
story += bullets([
    "<b>Liquidity risk at a fixed, non-negotiable date.</b> Unlike a mortgage or a tax bill, there is no "
    "partial payment, deferral or instalment plan for Home Office fees. Missing the payment or filing late "
    "risks falling out of lawful status entirely.",
    "<b>The application fee is forfeited even if the visa is refused.</b> Only the IHS portion is refunded "
    "on refusal — the application fee itself is not, regardless of outcome.",
    "<b>The lump-sum design front-loads a service not yet consumed.</b> A family granted 30 months of leave "
    "pays for 30 months of NHS access on day one. If circumstances later shorten the stay, they have already "
    "paid for healthcare they will not use.",
])
story += [callout(
    "Framing this as “£7,038 a year” is mathematically correct and practically misleading. "
    "The real experience is six sudden five-figure cash demands, each capable of derailing a family’s "
    "savings in the month it hits.")]

# ================= 05 =================
story += [
    Paragraph("05 · The £29,366 Route Penalty", h2),
    Paragraph(
        "The single most useful comparison in the UK build is not against other countries. It is against the "
        "other UK route. A family on the 5-year route pays for two grants of leave instead of four, then the "
        "same ILR and citizenship stages. Using identical fee lines, that comes to <b>£48,048</b>.", body),
    fig("route_comparison.png",
        "Fig 3 — Same country, same fee schedule, same passport at the end. Modelled on two grants "
        "of leave versus four.", max_w=140 * mm),
    Paragraph(
        "The gap is <b>£29,366</b> — exactly two extra renewal cycles. It is not a penalty for doing "
        "anything wrong. It is the price of having failed a financial threshold, had a refusal, or carried a "
        "gap in lawful residence at some point in the past. <b>The system charges most to the families with "
        "the least margin</b>, which is the closest thing this report has to a thesis.", body),
    Paragraph(
        "It also matters for how you read every chart that follows: the UK figure used in the international "
        "comparison is the <i>10-year</i> route. A UK family on the 5-year route sits at roughly $64,900 "
        "— still high, still second only to Nigeria, but not the same number.", body),
]

# ================= 06 =================
story += [
    Paragraph("06 · Europe &amp; North America", h2),
    Paragraph(
        "The same “stack every mandatory government fee across the full path to citizenship” "
        "methodology applies cleanly to other major destinations, because each publishes exact, verifiable "
        "fee schedules.", body),

    Paragraph("Ireland", h3),
    Paragraph(
        "Irish Residence Permit registration/renewal is €300 per adult per year, with under-18s exempt. "
        "Naturalisation costs €175 to apply (non-refundable) plus a certification fee on approval of "
        "€950 for adults and €200 for minors. There is no health-surcharge equivalent — Ireland "
        "concentrates cost in annual renewals rather than an upfront multi-year charge, which materially "
        "changes the cash-flow profile even where totals are comparable. <b>Family of 4 over 5 years: "
        "≈€5,650 (≈$6,526).</b>", body),

    Paragraph("Canada", h3),
    Paragraph(
        "Following the 30 April 2026 fee increase: economic-class permanent residence processing is CAD 990 "
        "for the principal applicant, CAD 990 for an accompanying spouse and CAD 270 per dependent child, plus "
        "a Right of Permanent Residence Fee of CAD 600 each for the principal applicant and spouse. Citizenship "
        "is CAD 653 per adult (including the CAD 123 right-of-citizenship fee) and CAD 100 per minor. "
        "<b>Family of 4: ≈CAD 5,396 (≈$3,873)</b> — dramatically lower than the UK, because "
        "Canada charges once for permanent status rather than four times for temporary leave.", body),

    Paragraph("Germany", h3),
    Paragraph(
        "Residence permit issuance €100, renewals roughly €93–96, settlement permit €113, "
        "naturalisation €255 per adult and €51 per minor naturalising alongside a parent. "
        "Germany’s 2024 citizenship reform also cut the standard residence requirement from 8 years to 5 "
        "(3 with strong integration), shortening the treadmill itself and not just the fee stack. "
        "<b>Family of 4 over 5 years: ≈€1,652 (≈$1,906)</b> — the cheapest of the European "
        "and North American builds.", body),

    Paragraph("France", h3),
    Paragraph(
        "Under Article 128 of the Loi de finances pour 2026 (Law 2026-103 of 19 February 2026), effective for "
        "all decisions from 1 May 2026, France sharply raised its residence-permit and naturalisation duties. "
        "A first <i>carte de séjour</i> now costs €350 (€300 tax + €50 stamp, up from "
        "€225 combined); renewal €250; and the naturalisation <i>droit de timbre</i> jumped from "
        "€55 to <b>€255 — a 364% increase in a single reform</b>. <b>Family of 4 over roughly "
        "5 years: ≈€2,410 (≈$2,782).</b> Children in France do not generally need their own "
        "<i>carte de séjour</i> before 18, which keeps the family multiplier lower than in the UK or US.", body),

    Paragraph("United States", h3),
    Paragraph(
        "The comparable US route is H-1B specialty-occupation status leading to an employer-sponsored green "
        "card (I-140/I-485) and then naturalisation (N-400). There is no annual health-surcharge equivalent; "
        "health coverage runs through the private insurance market and is not part of the visa-fee treadmill.", body),
]
story += bullets([
    "<b>Employer-borne</b> (legally cannot be shifted to the worker): H-1B registration $215; I-129 base $780 "
    "for employers with 26+ full-time US staff, or $460 for smaller employers and nonprofits; fraud prevention "
    "$500; ACWIA training $750–$1,500 by employer size; asylum program fee up to $600; I-140 $715. "
    "<b>≈$2,940–$4,310</b>, excluding optional premium processing ($2,965, which can more than "
    "double this).",
    "<b>Family-borne:</b> I-485 adjustment of status $1,440 per adult and $950 per child under 14; N-400 "
    "naturalisation $760 per adult (biometrics included). For two adults and two children: <b>$6,300</b>. "
    "Children generally acquire citizenship automatically and free of charge under the Child Citizenship Act "
    "once a parent naturalises — a structural difference from every other country in this build.",
    "<b>Combined mandatory government fees: ≈$10,610</b>, of which the family directly pays about 59%.",
])
story += [Paragraph(
    "Two contingent charges are excluded from that total. A <b>$250 “Visa Integrity Fee”</b> was "
    "enacted in July 2025 but, as of mid-2026, is still not being collected pending inter-agency "
    "implementation. And the <b>$100,000 H-1B payment</b> under Presidential Proclamation 10973 was vacated by "
    "the District of Massachusetts in June 2026; on <b>24 July 2026 the First Circuit denied the "
    "government’s motion for a stay</b>, so the fee remains blocked while the appeal proceeds. If it ever "
    "takes effect it would eclipse every other line in this report combined.", body)]

# ================= 07 =================
story += [
    PageBreak(),
    Paragraph("07 · Asia’s Top 10 Destinations", h2),
    fig("asia_ten.png",
        "Fig 4 — Asia’s top 10 migration destinations. Asterisked bars have no realistic "
        "citizenship pathway — the figure shown is indefinite residency renewal cost only."),
    Paragraph(
        "The Gulf states — Saudi Arabia, Kuwait and the UAE — sit at or near the top of the Asian "
        "cost ranking despite offering <i>no realistic citizenship pathway at all</i>. Families pay Gulf-scale "
        "annual residency and dependent fees indefinitely, with naturalisation reserved for exceptional, "
        "discretionary cases. That makes them structurally different from every other country here: the "
        "treadmill never ends in a finish line.", body),
    Paragraph(
        "Japan inverts the usual pattern: naturalisation itself is entirely free, and nearly all of a "
        "family’s cost is absorbed earlier, in residence-status maintenance. Malaysia is cheap per "
        "transaction but requires 10 of the preceding 12 years of residence before eligibility. "
        "Thailand’s cost concentrates in a single THB 191,400 Certificate of Residence.", body),

    PageBreak(),
    Paragraph("08 · Africa’s Top 10 Destinations", h2),
    fig("africa_ten.png",
        "Fig 5 — Africa’s top 10 migration destinations — the widest spread of any region "
        "in this report."),
    Paragraph(
        "Africa produces a roughly <b>240-fold gap</b> between Nigeria (≈$122,000) and Morocco "
        "(≈$510), despite both being top-10 destinations on the continent. The driver is not "
        "renewal-cycle count or health surcharges as in the UK, but <b>per-person, per-year work-permit levies "
        "with no family discount</b>. Nigeria’s CERPAC alone doubled from $1,000 to $2,000 per person per "
        "year, and the Constitution requires 15 years of residence before naturalisation eligibility — so "
        "a family of four’s permit costs alone compound into six figures well before any citizenship "
        "application is filed.", body),
    Paragraph(
        "Kenya sits second after raising the Class D work permit fee to KES 500,000 per year, a 150% increase. "
        "Ghana operates an explicitly tiered schedule: ECOWAS citizens pay GHS 15,000, Africans and the "
        "diaspora GHS 25,000, and non-Africans the cedi equivalent of US$25,000 — one of the few places "
        "on earth where being African is priced into the fee schedule in your favour. The chart uses "
        "Ghana’s diaspora rate.", body),
    Paragraph(
        "Rwanda sits at the opposite extreme on fees but the opposite extreme on time: the cheapest total in "
        "the region pairs with roughly a 15-year path — the joint-longest in this entire dataset. "
        "Tanzania is the only country here that requires renunciation of prior nationality.", body),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("09 · All 26 Countries on One Scale", h2),
    fig("global_comparison.png",
        "Fig 6 — All 26 countries, log scale. Asterisked bars have no realistic citizenship pathway "
        "— the low number is misleading, because it buys only indefinite renewable residency.",
        max_w=150 * mm, max_h=185 * mm),
]

story += [
    PageBreak(),
    Paragraph("Three patterns stand out.", body),
    Paragraph(
        "<b>First, the most expensive totals are not concentrated in any one region.</b> Nigeria, the UK and "
        "Saudi Arabia top the list for three structurally different reasons: uncapped per-person annual "
        "work-permit levies, a health surcharge billed as a multi-year lump sum, and Gulf-style residency with "
        "no citizenship exit at all.", body),
    Paragraph(
        "<b>Second, a large cluster sits under $3,000 all-in</b> — Germany, France, Rwanda, Morocco, "
        "South Africa, Egypt, Singapore, South Korea, Côte d’Ivoire. A full family’s path to "
        "citizenship does not have to cost five or six figures. It is a policy choice, not an inherent cost of "
        "processing paperwork.", body),
    Paragraph(
        "<b>Third, three of the “cheapest” countries by fee are flagged</b> because the low number is "
        "misleading. Saudi Arabia, Kuwait and the UAE sell renewable residency, not a destination.", body),

    Paragraph("10 · What Actually Drives the Bill", h2),
    Paragraph(
        "It is tempting to say the UK is expensive because it makes families pay so many times. That is only "
        "half true — and the other half is more damning.", body),
    fig("cost_per_event.png",
        "Fig 7 — Average cost per mandatory payment event. Ireland and Germany make families pay "
        "just as many times as the UK does."),
    Paragraph(
        "Ireland and Germany both require six separate government payments on the path to citizenship — "
        "the same number as the UK’s 10-year route. Yet Germany’s average payment is <b>$318</b> and "
        "the UK’s is <b>$17,418</b>: a 55-fold difference in the price of the same bureaucratic act.", body),
    Paragraph(
        "The number of times you pay is not what makes the UK expensive. It is the number of times you pay "
        "<i>multiplied by</i> a per-event price nobody else charges — and most of that price is a "
        "healthcare bill in a trench coat.", pull),
    Paragraph(
        "Canada demonstrates the opposite design: two payment events, moderate in size, because the country "
        "charges once for durable status rather than repeatedly for temporary permission. The cost of staying "
        "legal is not a function of how rich the destination country is, or how bureaucratically complex its "
        "system looks on paper. It is a direct, traceable product of specific policy choices.", body),
]

# ================= 11 =================
story += [
    Paragraph("11 · What To Do About It", h2),
    Paragraph(
        "None of this is advice on immigration law — get that from a regulated adviser. It is advice on "
        "the money, which is the part most families plan for worst.", body),
]
story += bullets([
    "<b>Save toward the date, not the year.</b> The single most useful reframe in this report: budget for "
    "£14,683 landing on a known date every 30 months, not £7,038 a year. A standing order into a "
    "separate, untouchable account, sized to the renewal — roughly £490 a month for a family of four "
    "— turns a crisis into a bill.",
    "<b>Know which route you are on, and whether you can move.</b> The gap between the 5-year and 10-year "
    "routes is £29,366. If a change in circumstances (income, English certification, relationship status) "
    "makes the 5-year route reachable, that is the highest-return paperwork in your life.",
    "<b>Check whether your children need registering at all.</b> A child born in the UK after a parent holds "
    "ILR is automatically British. Sequencing a birth after settlement, where that is a real choice, saves "
    "£1,000 per child.",
    "<b>Apply for a fee waiver if you genuinely cannot pay.</b> The Home Office operates fee waivers on the "
    "family and private life routes for applicants who cannot afford the fee. Waivers are widely under-claimed, "
    "and being refused costs nothing but time.",
    "<b>Budget the surcharge separately from the fee.</b> They are refunded on completely different terms: if "
    "the application is refused, the IHS comes back and the application fee does not.",
    "<b>If you are comparing destinations, compare cost <i>and</i> time <i>and</i> whether a path exists.</b> "
    "A cheap fee schedule attached to a 15-year wait (Rwanda) or no citizenship pathway whatsoever "
    "(Saudi Arabia, Kuwait, the UAE) tells a very different financial-planning story from the same figure "
    "attached to a fast, certain path (Japan, Germany, Canada).",
])

# ================= 12 =================
story += [
    Paragraph("12 · Method &amp; Limits", h2),
    Paragraph(
        "<b>What is counted:</b> mandatory government fees only, for a family of two adults and two children, "
        "from first grant of status to citizenship. Fees are as published at 11 August 2026.", body),
    Paragraph(
        "<b>What is not counted:</b> legal and adviser fees, language testing, translations, optional priority "
        "processing, private health insurance, travel, and the income thresholds that gate many of these "
        "routes.", body),
    Paragraph("<b>Assumptions that could move the numbers:</b>", body),
]
story += bullets([
    "Fees are held flat across the whole journey. They are not flat in reality — UK fees rose 6–7% in "
    "April 2026 alone — so the real 11-year total is almost certainly higher than £77,414, not lower.",
    "The UK figure is the <b>10-year</b> route, the more expensive of two UK paths. The 5-year route is "
    "£48,048. This is stated wherever the UK appears in a comparison.",
    "The UK total bundles a healthcare prepayment (the IHS) that most other countries in this build do not "
    "charge at all. The US figure explicitly excludes health insurance, which runs through the private market. "
    "The chart totals are therefore not measuring identical baskets.",
    "Nigeria’s ≈$122,000 is an <i>expatriate work-permit</i> stack; the UK’s is a "
    "family/private-life route. Both are “the cost of staying legal for a family of four,” but the "
    "underlying migrant profiles differ substantially.",
    "African, Gulf and Asian totals are <i>models</i> built on current fee levels held constant across long "
    "residence periods — not observed costs paid by real families.",
    "Currency conversions use approximate mid-August 2026 rates (GBP 1.35, EUR 1.155, CAD 0.718 to the "
    "dollar). Totals move with the rate.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "GOV.UK Home Office immigration and nationality fees, 8 April 2026; GOV.UK healthcare surcharge "
        "guidance; Free Movement on the April 2026 uplift; IRCC fee changes effective 30 April 2026; USCIS "
        "Form G-1055 fee schedule; Irish Citizens Information and the Irish Immigration Service; BAMF and "
        "German federal fee guidance; the French Loi de finances 2026 (Art. 128) as published by the "
        "Préfecture de l’Oise; BAL on Nigeria’s CERPAC; Newland Chase on Kenya; Citizenship "
        "Rights in Africa Initiative on Ghana; Clark Hill and Littler on the H-1B litigation; UN DESA "
        "International Migrant Stock 2024 and the Henley &amp; Partners Africa Wealth Report 2025 for "
        "destination rankings. Full inline links in the web edition.", small),
    Paragraph(
        "Figures for Asia, Africa and the Gulf are drawn from national immigration-authority schedules and are "
        "marked as approximate. Where a figure could not be confirmed from a primary source it is excluded "
        "rather than estimated.", small),
    Spacer(1, 6 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=8),
]
story += [callout(
    "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit together, "
    "and bounce ideas. This research is part of an open library, free to read and share. The Forum itself is "
    "by application.<br/><br/>"
    "Read the web edition with live source links: africaglobalforum.com/reports/visa-treadmill-2026<br/>"
    "Apply to join: africaglobalforum.com", bg=INK)]

doc.build(story)
print("wrote", OUT)
