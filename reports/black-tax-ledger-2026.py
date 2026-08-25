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
IMG = os.path.join(HERE, "black-tax-ledger-2026", "img")
OUT = os.path.join(HERE, "black-tax-ledger-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Black Tax Ledger · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 24 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Black Tax Ledger (2026)",
                      author="Africa Global Forum",
                      subject="What supporting home actually costs a sender, over a working life")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Black Tax Ledger.", h1),
    Paragraph("What supporting home actually costs.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Every business keeps a ledger. The single largest recurring payment in millions of "
        "diaspora lives — the money that goes home — is the one nobody writes down. This report "
        "writes it down: <b>what it costs over a working life, what it measurably buys, and how to "
        "run it on purpose</b> instead of by guilt and drift.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("1 : 4", big_num), Paragraph("15→60", big_num),
    Paragraph("$90k", big_num), Paragraph("$305k", big_num),
], [
    Paragraph("one sender abroad,<br/>four people supported", big_lbl),
    Paragraph("% of your income that is<br/>% of their household income", big_lbl),
    Paragraph("cash sent — $250/month<br/>over a 30-year career", big_lbl),
    Paragraph("what the same payments<br/>would have compounded to", big_lbl),
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
    fig("the_ledger.png",
        "Fig 3 — The lifetime account. Our own arithmetic, stated in full in Method &amp; Limits; "
        "illustrative, not a prediction.", max_h=100 * mm),
    Paragraph("Published August 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/black-tax-ledger-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Somewhere between a duty, a tax and a love language sits the money that goes home. It is "
        "the payment that never appears in a budget spreadsheet, is never discussed at the salary "
        "negotiation it silently halves, and never stops. This report treats it the way the "
        "sender's bank does: as a series of transactions with a lifetime total.", body),
]
story += bullets([
    "<b>The ratio is one to four.</b> Roughly <b>200 million migrant workers</b> send money home, "
    "and about <b>800 million people live on it</b> (IFAD). The average sender is a small pension "
    "system with no actuary.",
    "<b>The leverage is 15 to 60.</b> Migrants send about <b>15% of their income</b> — typically "
    "<b>$200–$300 every month or two</b> — and that money makes up about <b>60% of the receiving "
    "household's income</b>. The same transfer is a line item to you and the roof to them.",
    "<b>The lifetime bill is paid twice.</b> Our worked example: <b>$250 a month for a 30-year "
    "working life is $90,000 in cash</b> — and about <b>$305,000</b> if the same payments had "
    "compounded at 7%. The black tax is paid once in money and once in the <b>~$215,000 of "
    "compounding the money never did</b>.",
    "<b>Plus a third payment to the pipes.</b> At the <b>8.78%</b> average cost of sending to "
    "sub-Saharan Africa, roughly <b>$7,900</b> of that lifetime total goes to transfer fees.",
    "<b>And it is levied on a discounted salary.</b> Paid from pay packets already carrying a "
    "<b>26.1% earnings gap</b>, after host-country rent — while the sender's own retirement is, in "
    "account after account, the line that goes unfunded.",
    "<b>The credit side is real and measurable.</b> Across 122 developing countries, remittances "
    "raise school enrolment (girls' most of all), cut child mortality and stunting, and lift "
    "health spending. This is the most effective development programme Africa has — run out of the "
    "diaspora's payslips.",
    "<b>South Africa named it, and measured it:</b> around <b>70%</b> of working Black South "
    "Africans experience or expect the black tax, and <b>44%</b> of households support multiple "
    "generations.",
])
story += [
    Paragraph("The goal of this report is not to talk anyone out of paying. It is to move the "
              "black tax from the part of your life run by guilt to the part run by arithmetic — "
              "because only one of those two managers ever lets it end.", pull),
]

# ================= 02 & 03 =================
story += [
    PageBreak(),
    Paragraph("02 · The Word Itself", h2),
    Paragraph(
        "The term <i>black tax</i> comes from South Africa, where it names what the first "
        "generation of Black professionals discovered on payday: a salary that arrives "
        "pre-committed. Support for parents whose pensions apartheid never allowed to exist, "
        "siblings' school fees, a cousin's rent — obligations that white colleagues on identical "
        "salaries simply did not carry. The average Black household supports more people on the "
        "same income, and <b>one salary routinely carries four lives</b>.", body),
    Paragraph(
        "The word is contested, and the contest is worth keeping. Critics say <i>tax</i> poisons "
        "something that is actually <i>ubuntu</i> — mutual care, the thing that raised the sender "
        "in the first place. Defenders answer that refusing to name a cost does not remove it; it "
        "just removes it from view. This report holds both positions at once, deliberately. The "
        "money is love, and it is also money. The second fact does not dishonour the first — but "
        "only the second one compounds.", body),

    Paragraph("03 · One Sender, Four People", h2),
    fig("one_to_four.png",
        "Fig 1 — The global ratio, from IFAD: 200 million senders, 800 million supported."),
    Paragraph(
        "Globally, about <b>200 million migrant workers</b> send money home, and an estimated "
        "<b>800 million family members</b> depend on what arrives. For Africa, the flow reached "
        "about <b>$124 billion in 2025</b> — roughly double all official development aid — with "
        "about <b>75% funding immediate consumption</b>.", body),
    Paragraph(
        "Two things follow. First, <b>the average sender is running a miniature welfare state</b> — "
        "pension, health insurance, education grants and emergency fund for four people — without "
        "any of a welfare state's tools: no contributions, no actuarial tables, no retirement age, "
        "no way to decline a claim. Second, development economists have measured what remittances "
        "do for recipients for decades. Almost nobody measures what forty years of remitting does "
        "to the remitter. This report is about that missing column.", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · The Leverage", h2),
    fig("leverage.png",
        "Fig 2 — The same transfer, measured twice. IFAD figures; global averages, not "
        "Africa-specific."),
    Paragraph(
        "The money migrants send is, on average, about <b>15% of what they earn</b>. The same "
        "money makes up about <b>60% of the receiving household's income</b>. Sit with the "
        "asymmetry, because it explains the entire emotional economy of the black tax.", body),
]
story += bullets([
    "<b>It is why you cannot say no.</b> To you, skipping a month is an inconvenience. To them, it "
    "is the majority of household income not arriving. This is the arithmetic underneath the "
    "loyalty tax our investment research described: refusal is not read as budgeting. It is read "
    "as abandonment, because functionally it is closer to abandonment than either side wants to "
    "say.",
    "<b>It is why the requests seem endless.</b> A household 60% funded by transfers is not saving "
    "its way out of needing them. The transfer holds the floor; it rarely builds the stairs.",
    "<b>And it is why the money is genuinely irreplaceable.</b> No programme, charity or "
    "government delivers 60% of household income to 800 million people. The leverage that traps "
    "the sender is the same leverage that makes the money the most effective poverty instrument "
    "Africa has.",
])
story += [
    Paragraph("The black tax is hard to escape for the same reason it is worth paying: a dollar "
              "crosses the border and triples in meaning. The trap and the miracle are one "
              "mechanism.", pull),
]

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("05 · The Ledger", h2),
    Paragraph(
        "Now the number nobody writes down — Fig 3, on the cover. Take a representative obligation "
        "— <b>$250 a month</b>, inside IFAD's $200–300 range — and run it over a <b>30-year "
        "working life</b>.", body),
    Paragraph(
        "The cash column is simple: <b>360 transfers, $90,000</b>. Most senders have never seen "
        "that figure, because no one adds up a payment that arrives as an emergency, a school "
        "term, a funeral, a roof — $250 at a time.", body),
    Paragraph(
        "The second column changes how you see the first. Retirement arithmetic is boring and "
        "merciless: <b>$250 a month invested at 7% for 30 years grows to roughly $305,000</b> — "
        "the ordinary index-fund mathematics our savings report showed African households are "
        "locked out of. The gap between the columns — about <b>$215,000</b> — is the part of the "
        "black tax no one discusses, because it is paid in a currency that appears in no account: "
        "<b>compounding that never happened.</b>", body),
]
story += bullets([
    "<b>This is an illustration, not your statement.</b> Change the amount, the years or the "
    "return and the figures move — proportionally, which is the point. At $150 a month the "
    "foregone total is still six figures.",
    "<b>The comparison is not “family versus index fund.”</b> Nobody sends $250 into the void; it "
    "buys the outcomes in Section 07, some of which — a sibling's degree — compound in their own "
    "way. The ledger's job is to make the trade <i>visible</i>, not to declare it wrong.",
    "<b>But the invisibility is not neutral.</b> A cost that is never totalled can never be "
    "planned, capped, shared among siblings, or ended. The people who quietly reach sixty abroad "
    "with nothing did not decide to spend $305,000. They decided, 360 separate times, to send "
    "$250.",
])

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · The Double Bill", h2),
    fig("double_bill.png",
        "Fig 4 — Why the same obligation costs the diaspora more, assembled from findings across "
        "this library."),
    Paragraph(
        "The salary it comes from is already discounted — a <b>26.1% pay gap</b> for sub-Saharan "
        "African workers in Europe. The cost of living it competes with is the host country's: "
        "London rent and Lagos school fees from one payslip. The corridor takes <b>8.78%</b> in "
        "motion. And the shock absorber, in account after account, is the sender's own future: the "
        "pension contribution skipped, the retirement planned as “the house back home” — an asset "
        "our investment research showed is itself exposed to title fraud, abandonment and currency "
        "collapse.", body),
    Paragraph("The family's insurance policy is a person — and nobody is insuring the person. The "
              "most dangerous line in the ledger is not what you send. It is what you are not "
              "setting aside because you send.", pull),

    PageBreak(),
    Paragraph("07 · The Credit Side", h2),
    fig("credit_side.png",
        "Fig 5 — The credit side, from studies across 122 developing countries and the "
        "sub-Saharan literature."),
    Paragraph(
        "A ledger with only a cost column is propaganda. <b>Children go to school and stay "
        "there</b> — enrolment, completion and girls' education all rise. <b>Children survive and "
        "grow</b> — child mortality, stunting and undernourishment fall; a 10% rise in per-capita "
        "remittances lifts household health spending measurably. <b>Households stand upright</b> — "
        "the money arrives <i>more</i> reliably in crises, when everything else flees.", body),
    Paragraph(
        "Set that against the moral-hazard finding our investment report documented — remittances "
        "letting weak states spend less on health and education — and you get the honest, "
        "double-entry truth: the same transfer educates your niece <i>and</i> quietly subsidises "
        "the ministry that failed to. Both entries are real. Neither cancels the other. Count "
        "anyway: the credit side survives the counting. What does not survive counting is waste, "
        "duplication, and the fifth cousin's third business idea. Arithmetic is not the enemy of "
        "generosity. It is the enemy of leakage.", body),
]

# ================= 08 & 09 =================
story += [
    PageBreak(),
    Paragraph("08 · The Debit Nobody Prices", h2),
]
story += bullets([
    "<b>The escalation mechanism.</b> The transfer does not close the request; it opens an "
    "account. The washing machine becomes the generator becomes the subscription. Unmanaged, the "
    "ledger's trend line is up — not because anyone is greedy, but because a 60%-funded household "
    "reorganises itself around the funding.",
    "<b>The information asymmetry, both ways.</b> People at home convert your salary at the "
    "exchange rate and see wealth; they have never met your rent. You, four thousand miles away, "
    "cannot tell performed need from desperate need. The ledger cannot fix this. Only structure — "
    "and visits — can.",
    "<b>The sibling subsidy.</b> Where one child went abroad and four did not, the black tax "
    "quietly becomes a one-person levy: the sender covers not a fair share but the whole bill, "
    "plus the resentment of being seen as the lucky one. Ledgers shared among siblings — even "
    "unequally — recur in the accounts of families that stayed intact.",
])
story += [
    Paragraph("09 · The Country That Named It", h2),
    fig("south_africa.png",
        "Fig 6 — South African survey and NIDS figures. Different studies, different definitions."),
    Paragraph(
        "South Africa coined the term — and because the phenomenon there is domestic, it has been "
        "<i>measured</i>: around <b>70% of working Black South Africans</b> experience or expect "
        "the black tax; <b>44% of households</b> support multiple generations.", body),
    Paragraph(
        "The South African literature also supplies this report's sharpest structural insight: the "
        "black tax is what happens when <b>one generation is asked to be the pension system that "
        "history denied the generation before it</b>. Apartheid built the South African version; "
        "colonial wage economies and absent welfare states built the continental one; migration "
        "merely stretched it across borders and multiplied it by an exchange rate. You are not "
        "carrying a personal failing of your family. You are a private citizen performing an "
        "unfunded state function — and the exhaustion you feel is what unfunded state functions do "
        "to the person performing them.", body),
]

# ================= 10 & 11 =================
story += [
    PageBreak(),
    Paragraph("10 · Running Your Own Ledger", h2),
    fig("own_ledger.png",
        "Fig 7 — The practices, drawn from the community evidence and the structure of the "
        "problem. Not financial advice — a way of deciding on purpose."),
    Paragraph(
        "This obligation is too large to run on drift. What follows is not a way to pay less. It "
        "is a way to <i>decide</i>: write the number down once a year. Set the ceiling out loud — "
        "a rule refuses on your behalf, so no individual request is ever personally refused. Pay "
        "your pension first, and say why: you are the family's entire insurance stack, and the "
        "single worst outcome on the whole ledger — for <i>them</i> — is the sender reaching old "
        "age broke. Buy off-ramps, not subscriptions: one cousin taken from first year to "
        "graduation ends a branch of the ledger; five drip-feeds never end. And route it through "
        "structure — gatekeeper, evidence rule, fees paid directly to the school.", body),

    Paragraph("11 · The Off-Ramp", h2),
    Paragraph(
        "One reframe, and it is the most important paragraph in this report. The question senders "
        "ask is <i>“how do I manage this burden?”</i> The better question is generational: <b>“how "
        "do I make sure my children are not having this conversation?”</b> The black tax exists "
        "because the previous generation had no pension, no assets and no state behind it. It ends "
        "only when some generation converts support into <i>capacity</i>: educations completed, "
        "incomes established at home, one funded retirement (yours) that never becomes a claim on "
        "the next generation.", body),
    Paragraph(
        "That is what the ledger is <i>for</i>. Not to shame the spending, but to steer it: away "
        "from indefinite floor-holding, toward the specific, finishable purchases that close "
        "accounts. Every dependency you convert into an income is a payment your children will "
        "never make.", body),
    Paragraph("You cannot refuse to pay the black tax — the leverage saw to that. What you can "
              "refuse is to pass it on unamortised. The goal is not to be free of it. The goal is "
              "to be the last one paying.", pull),
]

# ================= 12 =================
story += [
    PageBreak(),
    Paragraph("12 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First, this report has priced something many readers believe should never be "
        "priced.</b> Putting $305,000 next to your mother's upkeep can read as an accusation, and "
        "it is not one. The accounting does not say the money was wasted; the credit side says the "
        "opposite. But refusing to count has a documented body count of its own — the senders who "
        "arrive at sixty with nothing were protected from the arithmetic, not by it.", body),
    Paragraph(
        "<b>Second, the ledger is not symmetrical, and honesty requires saying so.</b> The parent "
        "it supports spent unpriced decades raising the sender; the village schooled them; the "
        "family often funded the very migration the salary comes from. The black tax is, in part, "
        "a repayment schedule on real capital invested. What makes it corrosive is not the "
        "existence of the debt — it is that the schedule has no number, no term and no end, which "
        "no legitimate debt is allowed to lack.", body),
    Paragraph(
        "<b>Third, the exhaustion is allowed to be real at the same time as the love.</b> The "
        "dominant public scripts are gratitude (“family is everything”) and grievance (“they are "
        "bleeding me dry”), and most senders live in both at once, and say so nowhere — because "
        "our shame research applies with full force: the sender who admits strain looks like a "
        "failure abroad <i>and</i> a miser at home. The ledger gives you a way to talk about the "
        "money that is neither of those scripts — just arithmetic, said out loud, with love "
        "intact.", body),
]

# ================= 13 =================
story += [
    PageBreak(),
    Paragraph("13 · Method &amp; Limits", h2),
    Paragraph("This report combines published remittance and survey data with our own "
              "clearly-labelled arithmetic, as at 24 August 2026.", body),
]
story += bullets([
    "<b>Fig 3 is our own construction, and its assumptions are choices.</b> $250/month sits in "
    "IFAD's $200–300 global range; 30 years is a stylised working life; 7% is a conventional "
    "long-run nominal equity return, not a guarantee; fees apply the Q1-2025 sub-Saharan average "
    "(8.78%) flatly across three decades. The output is an <i>illustration of magnitude</i>. "
    "Inflation means the real foregone sum is smaller than the nominal $305,000, though still "
    "transformative at any plausible deflator.",
    "<b>The 15%/60% figures are IFAD global averages</b>, not Africa-specific, and both vary "
    "enormously by corridor, income and household. They are used for the asymmetry they "
    "demonstrate, which is robust, rather than their decimals, which are not.",
    "<b>The 1:4 ratio</b> divides IFAD's 800 million supported by 200 million senders; it is an "
    "aggregate, not a typical family.",
    "<b>The South African figures come from different instruments</b> with different definitions "
    "of support. They triangulate a phenomenon; they are not one dataset. And South Africa's "
    "domestic black tax is an analogue for the diaspora's cross-border version, not the same "
    "measured object.",
    "<b>No study measures the lifetime cost to diaspora senders.</b> That absence — decades of "
    "research on what remittances do <i>for recipients</i>, near-silence on what remitting does "
    "<i>to remitters</i> — is itself a finding of this report, and the reason Fig 3 had to be "
    "built rather than cited.",
    "<b>The credit-side effects are associations at national scale</b>, with the usual causal "
    "identification challenges; the enrolment and mortality findings replicate widely.",
    "<b>Escalation, sibling asymmetry and sender-retirement failure are qualitative patterns</b> "
    "from self-reported community accounts, with all the limits stated in our earlier research.",
    "<b>Nothing here is financial advice.</b> The ledger is a way of seeing; what any family does "
    "with it is theirs.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "IFAD, 15 Reasons Remittances Matter, and UN/IFAD remittance facts on sender ratios, "
        "amounts and shares; World Bank data on African remittance volumes and transfer costs; "
        "research on Black middle-class financial transfers in South Africa, the JEF exploratory "
        "study of black tax, and NIDS-based analyses; research on remittances, education and "
        "health in sub-Saharan Africa and the 122-country literature; the African Development "
        "Bank/IFAD consumption split. Full inline links in the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/black-tax-ledger-2026<br/>"
        "Companion reports: You Sent the Money. Did You Buy Anything? · Africa Saves. It Just "
        "Doesn't Compound. · What Will People Say?<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
