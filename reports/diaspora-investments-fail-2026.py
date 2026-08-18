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
IMG = os.path.join(HERE, "diaspora-investments-fail-2026", "img")
OUT = os.path.join(HERE, "diaspora-investments-fail-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "Why Diaspora Investments Fail · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 18 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="You Sent the Money. Did You Buy Anything? (2026)",
                      author="Africa Global Forum",
                      subject="Why diaspora investments in Africa fail, and the safeguards that work")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("You Sent the Money.", h1),
    Paragraph("Did you buy anything?",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Africans abroad send home <b>$124 billion a year</b> — about twice what the continent "
        "receives in foreign aid. Roughly a quarter of it is meant to build something. This is an "
        "account of the six ways that money stops being an asset somewhere between the transfer and "
        "the title, and what the evidence says actually prevents it.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("$31bn", big_num), Paragraph("10%", big_num),
    Paragraph("56,000", big_num), Paragraph("$32,900", big_num),
], [
    Paragraph("of remittances a year is<br/>actually available to invest", big_lbl),
    Paragraph("of rural African land<br/>is formally documented", big_lbl),
    Paragraph("abandoned public projects<br/>in Nigeria alone", big_lbl),
    Paragraph("what a $100,000 Lagos<br/>house from 2022 is worth<br/>in dollars today", big_lbl),
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
    fig("house_in_dollars.png",
        "The currency tax, in one picture — see Section 05. Our own arithmetic at NGN 460 and "
        "NGN 1,400 to the dollar; illustrative, not a valuation.", max_h=95 * mm),
    Paragraph("Published August 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/diaspora-investments-fail-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Almost everyone in this network knows someone it happened to. The land that turned out to "
        "belong to someone else. The house that reached lintel level in 2019 and is still at lintel "
        "level. The scheme that paid out beautifully for eight months. The plot bought for a "
        "brother-in-law to supervise, never seen since.", body),
    Paragraph(
        "These are not bad luck and they are not, mostly, bad judgement. They are <b>six specific, "
        "documented mechanisms</b>, and each one has a countermeasure.", body),
]
story += bullets([
    "<b>The money is enormous.</b> Remittances to Africa reached about <b>$124 billion in 2025</b> — "
    "roughly twice all official development aid. About <b>75% goes to consumption</b>. That leaves "
    "roughly <b>$31 billion a year</b> genuinely available to invest.",
    "<b>Failure one — the land has no paperwork.</b> Only about <b>10% of rural land in Africa is "
    "formally documented</b>, and roughly <b>15% of households hold a formal title</b>. If there is "
    "no title, you did not buy land. You bought a claim, and claims can be sold twice.",
    "<b>Failure two — the build stops.</b> Nigeria alone carries <b>over 56,000 abandoned public "
    "projects</b> worth <b>NGN 12–17 trillion</b>. Nobody counts the private, diaspora-funded ones, "
    "but the mechanism is identical.",
    "<b>Failure three — the currency eats it.</b> The naira went from about <b>NGN 460 to the dollar "
    "to about NGN 1,400</b>. A Lagos house bought for <b>$100,000</b> in 2022 is worth <b>$32,900</b> "
    "today if its naira price never moved. Its naira price has to <b>triple</b> to get you back to "
    "even.",
    "<b>Failure four — the return was never real.</b> Nigeria's SEC puts cumulative Ponzi losses at "
    "<b>NGN 316 billion</b> before counting <b>CBEX</b>, which took an estimated <b>NGN 1.3 "
    "trillion</b> from around <b>300,000 people</b> in 2025. Ghana's Menzgold took <b>GHS 340m+</b>; "
    "over <b>240 customers have since died</b>, some by suicide.",
    "<b>Failure five — nobody was actually watching.</b> Family supervision is unpaid, unqualified "
    "and unaccountable, and it is the default arrangement for most diaspora building.",
    "<b>Failure six — the transfer itself.</b> Sending $200 to sub-Saharan Africa cost <b>8.78%</b> "
    "in early 2025 against a global average of 6.49% and a UN target of 3%.",
    "<b>And the thing that demonstrably works is boring.</b> Nigeria's 2017 diaspora bond was "
    "<b>oversubscribed by 130%</b>. Ethiopia's 2011 bond was <b>forced to repay $6.5m</b> for "
    "breaching US securities law. The difference was registration and disclosure — paperwork, not "
    "patriotism.",
])
story += [
    Paragraph("The pattern across all six is the same: diaspora money is highly trusting and very "
              "poorly documented. Almost every safeguard in this report is a way of converting trust "
              "into paper.", pull),
]

# ================= 02 =================
story += [
    PageBreak(),
    Paragraph("02 · What Is Actually at Stake", h2),
    fig("the_funnel.png",
        "Fig 1 — Remittance flows to Africa and the share available for investment. Total from World "
        "Bank; the consumption split is IFAD data cited by the African Development Bank."),
    Paragraph(
        "<b>$124 billion</b> flowed into Africa in remittances in 2025 — about <b>twice the level of "
        "overseas development assistance</b>. Nigeria alone takes over $20 billion a year, more than "
        "its foreign direct investment inflows.", body),
    Paragraph(
        "But most of that is not investment. Around <b>75% goes to immediate support</b> — food, "
        "housing, education, health. That is not a failure; it is the point of it. What is left is "
        "roughly <b>$31 billion a year</b> genuinely available for saving or capital formation.", body),
    Paragraph(
        "Thirty-one billion dollars a year is larger than the annual GDP of most African countries. "
        "How much of it survives contact with the ground is therefore not a private matter about your "
        "uncle's plot. It is one of the larger capital-allocation questions on the continent, and it "
        "is almost entirely unmeasured.", body),
    Paragraph(
        "That absence of measurement is itself the first finding. <b>Nobody publishes a diaspora "
        "investment failure rate.</b> Everything in this report is assembled from adjacent evidence "
        "— land registration statistics, public project abandonment, regulator prosecutions, "
        "currency data. Treat the mechanisms as well documented and the aggregate loss as unknown.",
        body),
]

# ================= 03 =================
story += [
    PageBreak(),
    Paragraph("03 · Failure One: The Title That Isn't", h2),
    fig("the_title_gap.png",
        "Fig 2 — Formal land documentation in Africa. Figures via the Atlantic Council and World "
        "Bank land research."),
    Paragraph(
        "Only about <b>10% of rural land in Africa is formally documented</b>. Roughly <b>15% of "
        "households hold a formal title</b> to the farmland they occupy. Only about 4% of countries "
        "have documented the land in their own capital cities.", body),
    Paragraph(
        "This single fact generates most of the land horror stories in the diaspora. Where there is "
        "no register, the thing that proves ownership is a chain of local knowledge — who the family "
        "is, who farmed it, who the chief recognised. That chain works reasonably well for people who "
        "are physically present and catastrophically badly for people who are not.", body),
]
story += bullets([
    "<b>The same plot sold to several buyers.</b> Nothing prevents it if there is no central register "
    "to check against. In 2025 Nigeria's EFCC charged an Abuja developer and his spouse over land "
    "fraud involving forged documents and sales worth hundreds of millions of naira.",
    "<b>Forged or defective documents.</b> A receipt, a survey plan and a photograph of a signpost "
    "are not title. Many diaspora buyers have never seen the actual instrument.",
    "<b>Land subject to government acquisition</b>, under an existing right of occupancy, or facing "
    "compulsory purchase — all discoverable by a search, none visible from a photograph.",
    "<b>Family land sold by one member</b> without the consent of the others, which is a live dispute "
    "waiting for you rather than a purchase.",
])
story += [
    Paragraph("If your evidence of ownership is a receipt and a relationship, you have not bought "
              "land. You have bought a position in a future argument.", pull),
    Paragraph(
        "The countermeasure is unglamorous and cheap relative to the sums involved: <b>an independent "
        "title search at the relevant land registry, commissioned by a lawyer you retained, before "
        "any money moves.</b> Not the seller's lawyer. Not the agent's. Not a family friend who knows "
        "someone at the registry.", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · Failure Two: The Build That Stops", h2),
    fig("abandoned.png",
        "Fig 3 — Uncompleted public projects in Nigeria. Count and NGN 12tn valuation from the "
        "Nigerian Institute of Quantity Surveyors; the NGN 17tn figure is the Chartered Institute of "
        "Project Managers of Nigeria's."),
    Paragraph(
        "Nigeria carries <b>more than 56,000 abandoned government projects</b>, valued at somewhere "
        "between <b>NGN 12 and NGN 17 trillion</b>. Warehouses, half-built roads, dilapidated "
        "bridges, deserted housing estates, non-functional airports.", body),
    Paragraph(
        "That is the public sector, with budgets, procurement rules, quantity surveyors and "
        "parliamentary oversight. If projects fail at that scale <i>with</i> institutional "
        "supervision, the base rate for an unsupervised private build funded in instalments from four "
        "thousand miles away is not going to be better.", body),
]
story += bullets([
    "<b>Cost escalation.</b> A build quoted in 2022 naira and funded through 2026 has been hit by "
    "both inflation and devaluation. The quote was never a price; it was an opening position.",
    "<b>Funding in instalments with no schedule.</b> Money arrives when the sender has it rather than "
    "when the stage requires it, so work stops and restarts, and each restart costs money.",
    "<b>No written contract</b>, or one that does not tie payment to completed stages.",
    "<b>No independent supervision.</b> Nobody with professional liability ever inspects the work.",
    "<b>Diversion.</b> Material money spent on something else, with the build used as the explanation "
    "for the next request.",
])
story += [
    Paragraph(
        "The countermeasure is the single highest-value thing in this report and it is standard "
        "practice everywhere else in the world: <b>stage payments against verified completion.</b> "
        "Money is released when the foundation is signed off, then when the walls are up, then at "
        "roofing — each stage certified by an independent professional you are paying, who carries a "
        "licence they could lose.", body),
    Paragraph(
        "Escrow arrangements that hold funds until milestones are met are now offered by a number of "
        "platforms and banks. In 2026 UBA launched a diaspora-focused investment platform aimed at "
        "exactly this problem, and the Federal Mortgage Bank of Nigeria has introduced diaspora "
        "financing products. Whether any given one is good is a separate question; the structure is "
        "the right structure.", body),
]

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("05 · Failure Three: The Currency Tax", h2),
    Paragraph("This is the failure almost nobody prices, and on the numbers it is larger than fraud.",
              body),
    fig("currency_hurdle.png",
        "Fig 4 — The devaluation hurdle. Naira and cedi movements from central bank and market data; "
        "the break-even percentages are our own arithmetic."),
    Paragraph(
        "The naira lost <b>51.5% of its value in 2023</b> and a further <b>40.9% in 2024</b>, moving "
        "from around NGN 460 to the dollar to about NGN 1,400–1,500. Ghana's cedi has depreciated "
        "about <b>166% since 2020</b>.", body),
    Paragraph(
        "Here is what that means for an asset. If you hold something whose value is denominated in "
        "naira, and the naira has fallen by two-thirds against the dollar, then <b>the naira price of "
        "your asset must roughly triple just to leave you where you started</b> in the currency you "
        "actually earn and spend.", body),
    fig("house_in_dollars.png",
        "Fig 5 — A worked example. Our own arithmetic at NGN 460 and NGN 1,400 to the dollar; "
        "illustrative, not a valuation.", max_h=95 * mm),
    Paragraph(
        "A $100,000 house bought in Lagos in 2022, whose naira price has not moved, is worth about "
        "<b>$32,900</b> today. If its naira price <i>doubled</i> — which most "
        "people would describe as a very good investment — it is worth <b>$65,700</b>. You would need "
        "the naira price to <b>triple</b> to approximately break even.", body),
    Paragraph("Nobody in the diaspora tells this story, because in naira the house went up. In the "
              "currency your mortgage, your pension and your children's school fees are denominated "
              "in, it went down by two-thirds.", pull),
    Paragraph("Three honest qualifications, because this argument can be pushed too far.", body),
]
story += bullets([
    "<b>Prime urban property in Lagos, Accra and Nairobi has in many cases risen faster than the "
    "currency fell</b>, particularly where it is priced in dollars to begin with. The point is not "
    "that it always loses — it is that the currency move is the dominant term in the equation and is "
    "almost never in the spreadsheet.",
    "<b>If you intend to retire there, dollars are the wrong measure.</b> An asset that houses you in "
    "Enugu should be valued in what it costs to live in Enugu. Currency risk only bites if you need "
    "to convert back.",
    "<b>Rental income is hit twice</b> — the rent is in local currency and it usually lags inflation, "
    "so real yields compress exactly when the currency is falling fastest.",
])

# ================= 06 =================
story += [
    Paragraph("06 · Failure Four: The Return That Was Never Real", h2),
    fig("the_schemes.png",
        "Fig 6 — Documented losses to collapsed investment schemes. Bar lengths are our own "
        "US-dollar conversions at prevailing rates and are indicative only; the local-currency "
        "figures beside each bar are the reported ones."),
    Paragraph(
        "Nigeria's Securities and Exchange Commission estimates that Nigerians have lost about "
        "<b>NGN 316 billion</b> to Ponzi schemes and illegal fund managers over the years — a figure "
        "that <i>excludes</i> CBEX. <b>CBEX</b>, which promised up to 100% in 30 days and claimed to "
        "trade using AI, collapsed in April 2025 having taken an estimated <b>NGN 1.3 trillion</b> "
        "from around <b>300,000 investors</b> across Nigeria and Kenya. Nigeria's EFCC separately "
        "warned the public about <b>58 illegal schemes</b> operating in 2025 alone.", body),
    Paragraph(
        "Ghana's <b>Menzgold</b> promised 7–10% <i>monthly</i> and defrauded customers of more than "
        "<b>GHS 340 million</b> when it collapsed in 2018. Reporting indicates <b>more than 240 "
        "customers have died</b> in the years since, some by suicide. Kenya's <b>Ekeza Sacco</b>, "
        "tied to a well-known televangelist and promising affordable housing, collapsed with around "
        "<b>8,000 members</b> affected; its founder was charged over roughly <b>KES 1 billion</b>.",
        body),
    Paragraph("Diaspora investors are structurally attractive targets, and it is worth being clear "
              "about why:", body),
]
story += bullets([
    "<b>You have hard currency</b> and the returns are quoted in a currency that is depreciating, "
    "which makes the promised numbers look plausible against local inflation.",
    "<b>You cannot visit the office</b>, so the ordinary physical checks are unavailable.",
    "<b>Recruitment runs through community and church networks</b>, where the introduction comes from "
    "someone you trust rather than someone selling.",
    "<b>The real alternative looks bad.</b> When your savings account pays 1% and the naira falls "
    "40%, a scheme offering 10% a month is answering a genuine problem — badly.",
])
story += [
    Paragraph(
        "The rule that would have prevented every case above is a single question: <b>is this entity "
        "licensed by the securities regulator of the country it operates in, and can you find it on "
        "the regulator's own register?</b> Not its website. The regulator's register. Nigeria's SEC, "
        "Ghana's SEC, Kenya's CMA and the equivalent bodies all publish lists, and all of them "
        "publish warnings about unlicensed operators.", body),
    Paragraph(
        "The second rule: <b>a return that is high, fixed, and guaranteed is a contradiction in "
        "terms.</b> Real returns vary. Anything paying a fixed 10% monthly is paying you with the "
        "next person's deposit.", body),
]

# ================= 07 =================
story += [
    PageBreak(),
    Paragraph("07 · Failure Five: The Agent Problem", h2),
    Paragraph(
        "Every failure above is made worse by the same structural arrangement: <b>the person "
        "supervising your money on the ground is a relative, is unpaid, is not a professional, and "
        "cannot be fired.</b>", body),
    Paragraph(
        "We want to be careful here, because there is no data on this and it would be easy to slide "
        "into a slander on African families. Most people supervising a sibling's build are doing "
        "their honest best, for free, at real personal cost, and are frequently the reason anything "
        "got built at all.", body),
    Paragraph("But the arrangement itself is badly designed, and it would be badly designed anywhere:",
              body),
]
story += bullets([
    "<b>No expertise.</b> Your cousin cannot tell whether the concrete mix is right or the block-work "
    "is plumb, and neither can you over WhatsApp.",
    "<b>No liability.</b> A licensed surveyor who signs off bad work can be sued or struck off. A "
    "relative faces no consequence but a family argument.",
    "<b>No exit.</b> If the arrangement is failing, the cost of ending it is a permanent rupture with "
    "your family. So people continue funding projects they have privately stopped believing in.",
    "<b>Unpaid work invites informal compensation.</b> If someone spends two years of Saturdays "
    "managing your site for nothing, the temptation to take a margin on materials is a predictable "
    "feature of the design, not a moral failing unique to anyone.",
])
story += [
    Paragraph("Pay a professional. It is cheaper than what unpaid supervision actually costs, and it "
              "converts a family relationship into a contract that can be enforced without ending the "
              "relationship.", pull),
    Paragraph(
        "Concretely: engage a licensed quantity surveyor or project manager on a fee, have them "
        "certify each stage, and let your relative be your relative rather than your unpaid clerk of "
        "works. Budget 3–6% of build cost for supervision. Against a 56,000-project abandonment base "
        "rate, that is the cheapest insurance available.", body),
]

# ================= 08 (community evidence) =================
story += [
    PageBreak(),
    Paragraph("08 · What the Diaspora Says Happens", h2),
    Paragraph(
        "<i>A note on what this section is.</i> Everything above rests on published statistics. This "
        "section does not. It is drawn from what Africans abroad say publicly, at length and in large "
        "numbers, on open discussion forums — Nigerians, Ghanaians, Zimbabweans, Cameroonians and "
        "Kenyans, comparing notes about money sent home. These accounts are <b>self-reported, "
        "self-selected and unverifiable</b>. People who have been burned post more than people who "
        "have not. Nothing here should be read as a measured rate of anything.", body),
    Paragraph(
        "We include it anyway, for three reasons. It is the only description we have of the "
        "<i>mechanism</i> the statistics leave blank — particularly Section 07, where we said plainly "
        "that the agent problem had no supporting evidence. The accounts are strikingly consistent "
        "across countries that have no contact with each other. And one of the theories that emerges "
        "from them turns out to be confirmed by peer-reviewed research.", body),

    Paragraph("It is not a request, it is a subscription", h3),
    Paragraph(
        "The single most repeated pattern is escalation. A relative asks for a specific thing — a "
        "washing machine, a phone, school fees. The money is sent, often with something extra added "
        "out of affection. The specific need is then immediately replaced by a new one: no money for "
        "food, then a generator to run the washing machine.", body),
    Paragraph(
        "The structural point is that <b>the transfer does not close the request; it opens an "
        "account.</b> The same dynamic is described in nearly identical terms by people who have "
        "never met, in five different countries. And it propagates: send to one person and the number "
        "circulates.", body),
    Paragraph(
        "This matters for the rest of this report because <b>it is the same failure mode as an "
        "unstaged construction payment.</b> Money released against a relationship rather than against "
        "a defined, completed deliverable does not terminate the obligation. It establishes a rate.",
        body),

    Paragraph("The information asymmetry runs both ways", h3),
]
story += bullets([
    "<b>People at home frequently cannot see the cost of living abroad.</b> $100 converted mentally "
    "into local currency reads as a month of living, so a refusal reads as hoarding. Several posters "
    "from the continent made this point themselves, and framed it as inexperience rather than malice.",
    "<b>People abroad frequently cannot see the need at home either.</b> The most useful single "
    "account describes a man who argued with his mother for years about her requests, then visited, "
    "saw how she was actually living — and voluntarily increased what he sent. Some need is "
    "performance and some is severe, and <b>from four thousand miles away the two are "
    "indistinguishable.</b> That is the real problem: not the asking, but the impossibility of "
    "verification.",
    "<b>The senders are often not wealthy.</b> Recurring accounts describe people funding relatives "
    "while living on savings, borrowing from their own children to cover rent, or reaching sixty in "
    "an expensive country with no retirement provision because home always came first.",
])
story += [
    Paragraph("The whole system runs on an unverifiable claim made to someone who cannot check it and "
              "cannot say no. That is not a family problem. It is a design problem, and it is the "
              "same one that loses people their building money.", pull),

    Paragraph("The loyalty tax", h3),
    Paragraph(
        "One contributor, writing about Cameroon, gave the mechanism a name that we think is the "
        "sharpest framing in the entire body of material: <b>the loyalty tax</b>.", body),
    Paragraph(
        "The argument runs like this. Where contracts are weakly enforced and the future is uncertain, "
        "extracting value from you <i>today</i> is the rational strategy, because the long game does "
        "not reliably pay. The contractor who overbills is not stupid; he has correctly read his own "
        "environment. And the diaspora member is the ideal counterparty, because <b>they cannot "
        "credibly walk away.</b> Everyone involved understands that guilt is the enforcement "
        "mechanism, and that it points in only one direction.", body),
    Paragraph(
        "This is a better explanation of the pattern than dishonesty is. It also predicts the "
        "countermeasure correctly: what protects you is not finding more trustworthy people, but "
        "<b>arrangements in which walking away is possible</b> — a defined ceiling, a defined rule, a "
        "third party holding the funds. Every safeguard in Section 10 is, in this light, a way of "
        "restoring the ability to say no.", body),

    Paragraph("The claim we could check — and it holds", h3),
    Paragraph(
        "One assertion in this material is strong enough that it should not be repeated without "
        "verification: that <b>the more diaspora money privately funds schools and clinics, the less "
        "the state bothers to.</b>", body),
    Paragraph(
        "It is supported by peer-reviewed research. A study of <b>86 developing countries over "
        "1996–2007</b>, published in the <i>Journal of Development Studies</i>, found that remittance "
        "inflows <b>reduce public spending on education and health where governance is weak</b> — the "
        "“public moral hazard” effect. Later work in <i>Health Policy and Planning</i> examines the "
        "same effect on public health expenditure in Africa specifically. Related findings associate "
        "higher remittance receipts with weaker control of corruption and rule of law.", body),
    Paragraph(
        "Two cautions. This is a macroeconomic finding about national aggregates and weak-governance "
        "settings, not a verdict on any individual family — nobody's school fees caused a ministry to "
        "cut its budget. And the direction of causation in this literature is genuinely contested. "
        "But the mechanism the poster described is real and it is measured: <b>private diaspora "
        "provision can reduce the political cost of public non-provision.</b> The money that fixes "
        "the immediate problem can help sustain the conditions that produced it.", body),

    Paragraph("Why the businesses die", h3),
]
story += bullets([
    "<b>Pricing in dollars for customers earning cedis or naira.</b> The resulting market is other "
    "diaspora members, who buy once out of solidarity and then return to the cheaper local option.",
    "<b>Two weeks at Christmas is not market research.</b> Neither is a childhood memory. The strong "
    "recommendation from people who survived is to <b>live there for a full year first</b> — through "
    "every season, every festival and every fuel shortage — ideally while employed by someone else.",
    "<b>Distribution decides everything, and the diaspora consistently underestimates it.</b> "
    "Multiple accounts describe informal retail networks — market traders and street hawkers — as the "
    "actual gatekeepers of what sells, responsive to margin rather than branding.",
    "<b>The costs no spreadsheet included:</b> power and water interruptions, foreigner pricing, "
    "informal payments stacked on official fees, and employee theft.",
    "<b>“Invest in the motherland” events are described as a business in themselves</b> — paid rooms "
    "full of diaspora members with no local operating experience, advising one another.",
])
story += [
    PageBreak(),
    Paragraph("What the people with peace actually did", h3),
    fig("structures.png",
        "Fig 8 — Recurring arrangements described by people who reported the situation becoming "
        "manageable. Self-reported; presented as patterns, not as a tested method."),
    Paragraph(
        "The consistency here is the most useful thing in the section. Almost nobody who described "
        "reaching a stable position did it by giving less to the same people in the same way. They "
        "did it by <b>changing the structure of the transaction</b>, and they arrived at four "
        "arrangements independently.", body),
    Paragraph(
        "Note what all four have in common with the rest of this report: they replace a relationship "
        "with a rule. A gatekeeper is an escrow agent. An evidence requirement is a milestone "
        "certificate. A ceiling is a fixed-price contract. Turning relatives into employees is the "
        "same move as hiring a licensed supervisor instead of asking a cousin — it converts an "
        "unenforceable bond into an enforceable one, and, on these accounts, it tends to preserve the "
        "relationship rather than destroy it.", body),
    Paragraph(
        "Two honest closing notes. Several accounts describe cutting family off entirely and then "
        "hearing nothing for years — which they read as proof the relationship was only ever the "
        "transfer. That reading may be right; it may also be what estrangement looks like from one "
        "side. We do not know. And the most quietly devastating theme across all of it is not fraud "
        "or entitlement at all: it is people who left in order to help, and who wanted the "
        "relationships far more than they minded the money, discovering that <b>affection began "
        "arriving with an invoice attached and neither side could remember who sent the first "
        "one.</b>", body),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("09 · Failure Six: The Cost of Getting It There", h2),
    fig("remittance_cost.png",
        "Fig 9 — Remittance costs, Q1 2025, from the World Bank's Remittance Prices Worldwide."),
    Paragraph(
        "Before a single naira reaches a plot, the transfer takes its cut. Sending $200 to "
        "sub-Saharan Africa cost an average of <b>8.78%</b> in the first quarter of 2025 — up from "
        "7.7% a year earlier, against a global average of <b>6.49%</b> and a UN Sustainable "
        "Development Goal target of <b>3%</b>.", body),
    Paragraph(
        "Africa is the most expensive destination on earth to send money to. On a $50,000 build "
        "funded in twenty transfers, the difference between 8.78% and 3% is roughly <b>$2,900</b> — "
        "which is a supervising surveyor for the whole project, paid for out of nothing but choosing "
        "a better rail.", body),
    Paragraph(
        "Two practical notes. Costs vary enormously <i>within</i> the average — digital-first "
        "providers and mobile-money corridors are often well below it while cash-to-cash agents are "
        "well above. And for large capital transfers the percentage headline matters less than the "
        "exchange rate spread, which is where most of the real cost sits and which is rarely quoted "
        "as a fee at all. Compare the total amount that lands, not the advertised fee.", body),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("10 · What the Evidence Says Works", h2),
    Paragraph("There is one natural experiment in the record that isolates what actually protects "
              "diaspora money, and it is worth studying closely.", body),
    fig("two_bonds.png",
        "Fig 10 — Two diaspora bonds and one difference. Nigeria's 2017 issue and Ethiopia's 2011 "
        "issue, per ODI and contemporaneous reporting."),
    Paragraph(
        "<b>Nigeria, 2017.</b> A $300 million diaspora bond at 5.625%, registered with the <b>US "
        "Securities and Exchange Commission</b>, the <b>UK Listing Authority</b> and the <b>London "
        "Stock Exchange</b>. It was <b>oversubscribed by 130%</b>.", body),
    Paragraph(
        "<b>Ethiopia, 2011.</b> A diaspora bond sold to Ethiopians in the United States <i>without</i> "
        "registering with the SEC. Ethiopia was ultimately <b>forced to repay $6.5 million</b> for "
        "violating US securities law, and the programme is generally judged a failure.", body),
    Paragraph(
        "Same continent, same instrument, same emotional pitch to the same kind of buyer. The "
        "difference was that one submitted to a disclosure regime with teeth and the other did not. "
        "Diaspora investors are not irrationally distrustful — they respond, and in size, to "
        "<b>enforceable protection</b>.", body),
]
story += bullets([
    "<b>Regulated instruments over informal ones.</b> If a product is registered with a securities "
    "regulator, there is a disclosure document, an auditor and a body you can complain to.",
    "<b>Independent title search before payment</b>, at the registry, by your own lawyer.",
    "<b>Escrow with milestone release.</b> Funds held by a third party and released against certified "
    "completion.",
    "<b>Independent professional supervision</b>, paid, licensed, and reporting to you.",
    "<b>Verify the counterparty exists as a company.</b> In Nigeria that means a CAC registration "
    "check; equivalent registries exist in every market. It takes minutes.",
    "<b>A written contract reviewed by counsel you retained</b> — not the developer's standard form, "
    "reviewed by the developer's lawyer.",
    "<b>Physical inspection by an independent third party</b> before purchase. Not a photograph. Not "
    "a video call conducted by the seller.",
    "<b>Digitised registries where they exist.</b> Blockchain-based and digital land-title pilots are "
    "running in Lagos and Oyo among others. These are early and should not be trusted blindly, but "
    "where a state registry is searchable online, search it.",
])

# ================= 10 =================
story += [
    PageBreak(),
    Paragraph("11 · The Checklist", h2),
    Paragraph("If you take one thing from this report, take this. Nothing here is expensive relative "
              "to the sums at risk, and the whole list can be done from abroad.", body),
    table([
        [Paragraph("Before you send anything", th), Paragraph("Why", th),
         Paragraph("Rough cost", th)],
        [Paragraph("<b>Retain your own lawyer</b> in the country — not the seller's, not a "
                   "relative's friend", cell),
         Paragraph("Every other step depends on having someone whose duty is to you", cell),
         Paragraph("Modest fixed fee", cell)],
        [Paragraph("<b>Independent title search</b> at the land registry", cell),
         Paragraph("Catches double sales, forged documents, government acquisition, existing "
                   "encumbrances", cell),
         Paragraph("Small, often under $200", cell)],
        [Paragraph("<b>Company registration check</b> on the developer or agent", cell),
         Paragraph("Confirms the counterparty legally exists and who controls it", cell),
         Paragraph("Near zero, minutes online", cell)],
        [Paragraph("<b>Regulator register check</b> for any investment product", cell),
         Paragraph("The single test that would have caught CBEX, Menzgold, MMM and Ekeza", cell),
         Paragraph("Free", cell)],
        [Paragraph("<b>Independent physical inspection</b> by someone you pay", cell),
         Paragraph("Confirms the land exists, is where they said, and is not occupied", cell),
         Paragraph("Small", cell)],
        [Paragraph("<b>Written contract reviewed by your counsel</b>", cell),
         Paragraph("Turns promises into obligations that survive a fallout", cell),
         Paragraph("Modest", cell)],
        [Paragraph("<b>Escrow or staged payment against certified milestones</b>", cell),
         Paragraph("The single most effective control against abandonment and diversion", cell),
         Paragraph("Small % of transaction", cell)],
        [Paragraph("<b>Licensed supervisor on a fee</b> for anything being built", cell),
         Paragraph("Creates expertise, liability and an exit that does not end a family", cell),
         Paragraph("3–6% of build cost", cell)],
        [Paragraph("<b>Compare what lands, not the advertised fee</b>, on every transfer", cell),
         Paragraph("The exchange-rate spread usually costs more than the stated fee", cell),
         Paragraph("Free; saves ~6%", cell)],
    ], [58 * mm, 74 * mm, 38 * mm]),
    Paragraph(
        "Total cost of the whole list on a $50,000 project: comfortably under $3,000, much of it "
        "one-off. Set that against a base rate of abandonment that runs into tens of thousands of "
        "projects in one country alone.", body),
]

# ================= 11 & 12 =================
story += [
    PageBreak(),
    Paragraph("12 · How to Think About Currency", h2),
]
story += bullets([
    "<b>Ask what currency you will need the money in.</b> If you will spend it where you live now, "
    "you are a dollar, euro or pound investor and local-currency assets carry a large hidden risk. If "
    "you will retire there, you are a local-currency investor and the risk mostly disappears.",
    "<b>Price the hurdle explicitly.</b> Before buying, write down what the local-currency price has "
    "to do over your holding period just to break even in your home currency. If that number is "
    "200%, say so out loud.",
    "<b>Prefer assets that earn hard currency</b> where you can find them — export businesses, "
    "dollar-denominated commercial leases, tourism.",
    "<b>Do not treat local-currency cash as savings.</b> Money sitting in a naira or cedi account "
    "waiting for the next construction stage is losing value the entire time. Send it when it is "
    "needed, not before.",
    "<b>Beware of returns quoted in local currency.</b> A 25% annual return in a currency falling 40% "
    "a year is a 15% loss wearing a good suit.",
])
story += [
    Paragraph("13 · If You Are Building for the Diaspora", h2),
    Paragraph("For members of this network building products, funds or developments aimed at Africans "
              "abroad, the evidence points at something specific: the market is not short of demand "
              "or of capital. It is short of <b>enforceable structure</b>.", body),
]
story += bullets([
    "<b>Register where your buyers live, not only where you operate.</b> That is the entire lesson of "
    "Nigeria 2017 versus Ethiopia 2011. It is expensive and it is the product.",
    "<b>Sell the escrow, not the yield.</b> Every competitor is promising returns. Almost none are "
    "promising a structure in which failure is recoverable.",
    "<b>Third-party verification beats your own transparency.</b> Your video walkthrough is your "
    "video. An independent surveyor's certificate is evidence.",
    "<b>Assume your buyer has been burned</b>, or knows someone who has. The trust deficit is earned, "
    "and it is documented: Nigerian real-estate professionals themselves name it as the single "
    "biggest deterrent to diaspora buyers.",
    "<b>The unserved segment is small tickets with real protection.</b> Structured products exist for "
    "the $500,000 buyer. The $15,000 buyer — which is most of the diaspora — gets an agent and a "
    "prayer.",
])

# ================= 13 =================
story += [
    PageBreak(),
    Paragraph("14 · The Uncomfortable Part", h2),
    Paragraph("Three things worth saying plainly.", body),
    Paragraph(
        "<b>First, some of this is our own doing.</b> Diaspora buyers routinely skip checks they "
        "would never skip at home. Nobody buys a house in Manchester or Maryland without a solicitor "
        "and a survey. The same person will wire $40,000 for land in a village on the strength of a "
        "phone call, because it is home and home does not feel like a transaction. That instinct is "
        "decent and it is exactly what the fraud is built to exploit.", body),
    Paragraph(
        "<b>Second, the emotional pressure is real and it should be named.</b> Building at home is "
        "not only an investment; it is proof that the migration was worth something, and there is "
        "family expectation attached to it. That makes it very hard to stop funding a failing "
        "project, or to ask a relative for receipts. The checklist above is partly a way of moving "
        "those decisions out of the emotional register and into a document, before the pressure "
        "arrives.", body),
    Paragraph(
        "<b>Third, the structural fix is not the diaspora's job.</b> Ninety percent of African land "
        "being undocumented is a state failure, not a consumer one. So is a 56,000-project "
        "abandonment backlog, and so is an 8.78% remittance cost. Individuals can protect themselves "
        "with lawyers and escrow, and they should. But the reason this report exists at all is that "
        "the infrastructure a Danish or Canadian investor takes for granted — a searchable register, "
        "an enforced contract, a functioning regulator — is what is actually missing.", body),
    Paragraph("You cannot fix the land registry from Houston. You can refuse to buy anything that is "
              "not in it.", pull),
]

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("15 · Method &amp; Limits", h2),
    Paragraph("This report assembles published figures as at 18 August 2026, read for what they say "
              "about why diaspora capital fails to become diaspora assets.", body),
]
story += bullets([
    "<b>There is no diaspora investment failure rate, and we have not invented one.</b> No registry "
    "tracks diaspora-funded projects to completion. Every mechanism in this report is documented; the "
    "aggregate loss is genuinely unknown. Anyone quoting you a headline percentage for how many "
    "diaspora investments fail is estimating.",
    "<b>Fig 3 is public projects, not diaspora ones.</b> Nigeria's 56,000 abandoned projects are "
    "government contracts. We use them as evidence that construction abandonment is systemic rather "
    "than as a measure of diaspora outcomes, and the two are not the same thing.",
    "<b>Fig 4 and Fig 5 are our own arithmetic</b>, at NGN 460 and NGN 1,400 to the dollar. They are "
    "illustrations of a mechanism, not valuations. Real Lagos property prices have in many cases "
    "risen substantially in naira, and dollar-priced prime property behaves differently again.",
    "<b>Fig 6 mixes currencies, years and definitions.</b> Bar lengths are our own dollar conversions "
    "at prevailing rates; the reported local-currency figures are shown beside each bar and should be "
    "treated as the primary numbers. The CBEX figure in particular is an early estimate from a 2025 "
    "collapse and may be revised substantially.",
    "<b>The NGN 12tn and NGN 17tn abandonment valuations come from two different professional "
    "bodies</b> and we have quoted the range rather than pick one.",
    "<b>The 75/25 consumption-investment split is a survey-derived estimate</b> from IFAD, applied "
    "continent-wide. Real splits vary enormously by country, corridor and household income.",
    "<b>Section 07 has no quantitative support</b>, and we have flagged it as structural reasoning "
    "rather than evidence. The mechanism is well understood in every other context where principals "
    "delegate to unmonitored agents; Section 08 gives it qualitative support, but nobody has "
    "measured it.",
    "<b>Section 08 is not evidence of the same kind as the rest of this report</b>, and is labelled "
    "as such where it appears. It draws on self-reported accounts posted publicly on open diaspora "
    "forums. That material is self-selected — people who lost money post more than people who did "
    "not — unverifiable, and impossible to weight. We use it to describe mechanisms and to record "
    "the arrangements people say worked, never to establish how often anything happens. Individual "
    "accounts are paraphrased rather than quoted, and we have not attempted to identify or contact "
    "anyone involved.",
    "<b>The public moral hazard finding is contested.</b> The <i>Journal of Development Studies</i> "
    "result holds for weak-governance settings across 86 countries; the direction of causation in "
    "this literature is genuinely debated, and it describes national aggregates, not households. We "
    "have stated it as a measured macroeconomic effect and nothing more.",
    "<b>Nothing here is financial or legal advice.</b> We are not licensed to give either. The "
    "checklist is a list of ordinary due-diligence steps, not a recommendation about any product, "
    "country or asset.",
    "<b>Country coverage is uneven.</b> Nigeria, Ghana and Kenya are heavily represented because they "
    "publish and prosecute; Francophone and Lusophone Africa are under-represented here for lack of "
    "comparable public data, not because the problems are absent.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "World Bank on remittance volumes and costs; African Development Bank and IFAD on the "
        "consumption-investment split; Atlantic Council and World Bank land research on documentation "
        "rates; the Nigerian Institute of Quantity Surveyors and Chartered Institute of Project "
        "Managers of Nigeria via Vanguard and TheCable on abandoned projects; Nairametrics on naira "
        "depreciation; Nigeria's SEC via Technext and Pulse on Ponzi losses; reporting on Menzgold "
        "and Business Daily on Ekeza Sacco; ODI on diaspora bonds; The Guardian Nigeria on the trust "
        "deficit; Journal of Development Studies and Health Policy and Planning on the public moral "
        "hazard effect of remittances. Section 08 draws on publicly posted accounts across open "
        "diaspora discussion forums. Full inline links in the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/diaspora-investments-fail-2026<br/>"
        "Companion reports: Africa Saves. It Just Doesn't Compound. · How Long Until It Was Worth "
        "It?<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
