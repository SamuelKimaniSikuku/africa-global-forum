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
IMG = os.path.join(HERE, "uncounted-year-2026", "img")
OUT = os.path.join(HERE, "uncounted-year-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Uncounted Year · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 7 September 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Uncounted Year (2026)",
                      author="Africa Global Forum",
                      subject="What one year abroad actually costs, why we refuse to add it up, and how to send with a system")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Uncounted", h1),
    Paragraph("year.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "A letter went around this network: whatever you do, don't add up what you sent home "
        "last year — you might do something reckless, like planning. This report dares the "
        "addition. The world's most expensive money corridor at 8.78% a transfer, a worked "
        "one-year ledger that lands near a fifth of a net income, the documented psychology of "
        "refusing to look, the price list of the “temporary” decade, and the €40 savings "
        "account explained at last — plus the five moves that turn a sigh into a system, none "
        "of which is “send less”.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("8.78%", big_num), Paragraph("≈ €5,160", big_num),
    Paragraph("−9.5%", big_num), Paragraph("€3,300", big_num),
], [
    Paragraph("average cost of sending to<br/>Sub-Saharan Africa — the<br/>world's most expensive", big_lbl),
    Paragraph("one ordinary year abroad,<br/>added up — a fifth of a<br/>€28,000 net income", big_lbl),
    Paragraph("drop in account logins when<br/>the news might hurt —<br/>the ostrich effect", big_lbl),
    Paragraph("what the fee leak alone,<br/>redirected, compounds to<br/>over one decade", big_lbl),
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
    fig("uncounted_year.png",
        "Fig 1 — One year, added up: the worked example. Assumptions in Method; your numbers "
        "will differ — run yours.", max_h=95 * mm),
    Paragraph("Published September 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/uncounted-year-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "The letter asked one question and this report exists to answer it: <i>have you ever "
        "dared to add up one year? Just one.</i> We ran the number, checked the psychology of "
        "why nobody runs it, and priced what counting unlocks.", body),
]
story += bullets([
    "<b>The satire understates the facts.</b> The letter joked about “8% on every transfer”. "
    "The measured figure is worse: sending to Sub-Saharan Africa costs <b>8.78% on average</b> "
    "— the most expensive corridor on earth, against a world average of 6.49% and a UN target "
    "of 3% — on $56 billion of yearly flows. The joke was documentary.",
    "<b>One year, added up, is a second rent.</b> Our worked example — the standing €250, the "
    "January school fees, the March hospital bill, the June funeral, two prayer-emoji "
    "emergencies, the fees, the visa year — lands at <b>roughly €5,160: about a fifth of a "
    "€28,000 net income</b>, paid in the dark. Your number will differ. That is the point: run "
    "yours.",
    "<b>Not counting is not carelessness — it is a documented strategy.</b> The ostrich "
    "effect: account logins fall 9.5% when markets drop; people systematically avoid free, "
    "useful information when looking would hurt. The diaspora runs the strongest version, "
    "because our number audits more than a budget: it audits the dream, and the performance of "
    "“fine” in two mirrors.",
    "<b>The uncounted year has named line items</b> — the fee leak (≈€250 a year between the "
    "corridor's price and the achievable one, €3,300 compounded over a decade), the temporary "
    "decade (the renewal loop, the pension never started, the wealth left behind), and the €40 "
    "savings account — not a mystery but a <b>queue position</b>: every enforced ledger "
    "settles before the unenforced self.",
    "<b>Counting is not the reckless act. It is the loving one.</b> One evening converts guilt "
    "into data, crisis-pricing into planning, and the sigh into a system — scheduled, "
    "fee-shopped, batched, buffered, and pointed at a destination. Nothing here says send "
    "less. It says <b>send on purpose</b> — toward being the last one paying, not the "
    "longest.",
])
story += [
    Paragraph("The letter was right about one thing: counting leads to planning, planning "
              "leads to questions, and questions change everything. That was the warning. It "
              "is also the instruction manual.", pull),
]

# ================= 02 =================
story += [
    PageBreak(),
    Paragraph("02 · The Letter", h2),
    Paragraph(
        "It arrived, as these things do, in the group chat — signed <i>from your relative in "
        "Europe, with love</i>. It deserves to be read whole:", body),
    callout(
        "<i>“Living abroad is free money. Everyone back home knows this. So please, let's keep "
        "the tradition alive. Don't add up what you sent home last year. The school fees in "
        "January, the hospital bill in March, the funeral in June, the two 'small emergencies' "
        "that arrived with a prayer emoji attached. That number is nobody's business — "
        "especially not yours. Keep paying 8% on every transfer. Africa is the most expensive "
        "place in the world to send money to, and somebody has to keep it that way. Renew the "
        "visa. Then renew it again. Twelve years in, call it 'temporary'. Keep the savings "
        "account you opened in 2019. The one with €40 in it. It's doing fine. And whatever "
        "happens, tell everyone at home you're fine. Post the picture with the snow. Because if "
        "we ever counted — the transfers, the fees, the renewals, the €40 — we might do "
        "something reckless. Like planning. Like asking questions. Like sending with a system "
        "instead of a sigh. Terrible idea. Forget I said anything.”</i>", bg=INK),
    Paragraph(
        "Satire is a diagnostic instrument: it only lands where it is true. So this report does "
        "the disobedient thing and treats every line as a claim to be fact-checked — the "
        "transfers, the addition, the not-looking, the 8%, the “temporary”, the €40, the snow "
        "picture — and then, because the sarcastic ending is actually a to-do list, the "
        "planning, the questions, and the system.", body),

    Paragraph("03 · The Most Expensive Place on Earth", h2),
    fig("most_expensive.png",
        "Fig 2 — World Bank Remittance Prices Worldwide, Q1 2025. The satire said 8%. The "
        "satire was being generous.", max_h=85 * mm),
    Paragraph(
        "The letter's most sarcastic line is its most factual: <b>Sub-Saharan Africa is the "
        "most expensive region on earth to send money to</b> — 8.78% of a $200 transfer, "
        "against a global average of 6.49% and the UN target of 3% — on roughly $56 billion of "
        "yearly inflows. Why? Thin competition, banks de-risking out of African markets, "
        "exclusive operator agreements, and captive customers who do not compare prices. Note "
        "that last clause: <b>the corridor stays expensive partly because its users send with "
        "a sigh instead of a system.</b>", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · One Year, Added Up", h2),
    Paragraph(
        "We built the year the letter describes, with deliberately ordinary numbers — a €250 "
        "standing transfer, one school-fees January, one hospital March, one funeral June, two "
        "“small emergencies”, fees at the measured 8.78%, and one visa cycle. The total (Fig "
        "1): <b>about €5,160 — roughly a fifth of a €28,000 net income.</b> A second rent in "
        "most European cities. It is also, to say it clearly, a magnificent act of love "
        "repeated monthly — our black tax research showed what these flows measurably buy.", body),
    Paragraph(
        "The problem is not the number. The problem is that <b>almost nobody who pays it knows "
        "it</b> — and an unknown number cannot be planned, negotiated, protected, or "
        "completed. Known, it invites the questions the sigh never allows: is the fee line "
        "necessary (no)? Are the emergencies really emergencies, or annual events wearing "
        "costumes — school fees come every January; a fund beats a fright. Is the sending "
        "sized to a plan, or to whoever asked loudest most recently? Unknown, the year is "
        "weather. Known, it is a budget. That single conversion is the entire report.", body),

    Paragraph("05 · Why We Don't Look", h2),
    fig("ostrich.png",
        "Fig 3 — The ostrich effect and information avoidance: not-looking is a strategy, not "
        "an accident.", max_h=95 * mm),
    Paragraph(
        "Not-looking is one of behavioural economics' best-documented moves. Karlsson, "
        "Loewenstein and Seppi named it the <b>ostrich effect</b>: investors monitor "
        "portfolios eagerly when markets rise and stop logging in when they fall — logins drop "
        "9.5% after declines, with free 24/7 access. The wider literature on <b>information "
        "avoidance</b> finds people dodging free, useful knowledge — medical tests, calorie "
        "counts, balances — whenever the information might hurt to hold.", body),
    Paragraph(
        "The diaspora's unopened statement carries more than a balance. Counting threatens "
        "<b>the dream audit</b> — if the total is huge and the savings are €40, what did the "
        "migration buy? It threatens <b>the performance</b> — the “fine” broadcast in two "
        "mirrors survives partly because nobody, including the broadcaster, has seen the "
        "books. It threatens <b>relationships</b> — a counted number demands conversations the "
        "sigh postpones. And it threatens <b>identity</b>: the provider who never checks, "
        "because providing is who they are. Every one of these is a feeling about the number. "
        "None of them changes it. The fee is charged on schedule, feelings and all.", body),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · The Fee Leak", h2),
    fig("fee_leak.png",
        "Fig 4 — What shopping the corridor is worth, on €4,350 of yearly sending.",
        max_h=95 * mm),
    Paragraph(
        "On our worked year's €4,350 of sending, the corridor's average price extracts about "
        "<b>€382 in fees</b>; the same money at the achievable 3% costs about <b>€130</b>. The "
        "difference — roughly €250 a year — is pure leak. Over a decade: <b>€2,500 spent on "
        "nothing</b>; redirected at 5%, <b>€3,300</b> — a term of university fees paid to the "
        "pipes for the convenience of never comparing. Prices on the same corridor, the same "
        "day, routinely differ by several points between operators. Fifteen minutes of "
        "comparison, twice a year, is worth more per hour than almost any overtime available "
        "to the people reading this.", body),

    PageBreak(),
    Paragraph("07 · The Temporary Decade", h2),
    fig("temporary.png",
        "Fig 5 — “Twelve years in, call it temporary” has a price list.", max_h=100 * mm),
    Paragraph(
        "The renewals are the visible cost; the expensive part of “temporary” is what it does "
        "to every other decision: the pension never started because “I'm not staying forever” "
        "— the solvent our procrastination research named; savings never invested because they "
        "might be needed “for the move”; the pensions, deposits and accounts measurably "
        "abandoned in countries people finally left; the house at home half-built by money "
        "that was also half-committed here. Twelve temporary years produce neither a settled "
        "life abroad nor a completed one at home. The fix: <b>the decision does not need to be "
        "final; it needs to be working.</b> “At least five more years” unlocks the pension. "
        "“Home in 2030” unlocks the finished house. Either beats the letter's answer — which "
        "is, cheerfully, neither.", body),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · The €40 Account", h2),
    fig("two_ledgers.png",
        "Fig 6 — The remitter's two-ledger life. The €40 is not a mystery; it is a queue "
        "position."),
    Paragraph(
        "The €40 is not evidence of indiscipline. Everything on the first ledger — rent, "
        "bills, the monthly €250, the emergencies — has an <b>enforcement mechanism</b>: a "
        "landlord, a contract, a mother, a crisis. Everything on the second — savings, "
        "pension, buffer — is enforced by nobody. The enforced ledger wins every month, and "
        "the self is paid last from what remains, which is €40. Every saving system that works "
        "— the payroll pension, the standing order, the chama — works by adding enforcement, "
        "not motivation.", body),
    Paragraph(
        "The quieter blocker: for a remitter, <b>saving can feel like withholding</b> — euros "
        "sitting idle while someone at home needs them now. The reframe that survives the "
        "culture is the black-tax report's: the emergency fund <i>is</i> for the family — it "
        "answers the 2 a.m. call without a payday loan; the pension <i>is</i> for the family — "
        "it guarantees you will not become the next generation's black tax. Paying yourself is "
        "not defection. It is the exit ramp the whole system needs one person per family to "
        "build.", body),

    Paragraph("09 · The Performance of Fine", h2),
    Paragraph(
        "“Tell everyone at home you're fine. Post the picture with the snow.” Three engines "
        "maintain the performance: the myth of abroad (your snow picture is the next cohort's "
        "evidence), the audit (“what will people say” taxes any admission), and the givers' "
        "paradox (the provider role forbids presenting a need). The uncounted year is the "
        "performance's accounting department: <b>the books must stay closed because the show "
        "must go on.</b> What counting threatens is exactly what makes it worth doing: it "
        "turns “I can't” (disbelieved, resented) into “here is what this year already "
        "carried” (a fact, discussable). Families mostly do not know what the sender's life "
        "costs — the information asymmetry runs both directions, and the sigh maintains it in "
        "both. The number, shared with one trusted person at home, is the beginning of the "
        "honest conversation this series has been circling.", body),
]

# ================= 10 =================
story += [
    PageBreak(),
    Paragraph("10 · The Reckoning, Step by Step", h2),
    fig("reckoning.png",
        "Fig 7 — One evening. It only has to be dared once.", max_h=105 * mm),
    Paragraph(
        "<b>Export, don't remember</b> — one year of statements from the bank app, the "
        "remittance apps, the mobile-money history; memory is the ostrich's accomplice, and it "
        "rounds everything down. <b>Sort into six lines</b>: routine transfers; school fees; "
        "medical; funerals and ceremonies; emergencies; fees-and-visa. <b>Write the one number "
        "down</b>, and beside it its share of your net income — no verdicts; a number is a map "
        "reference, not an accusation. <b>Show it to one person</b> — partner, sibling, chama: "
        "counted alone the number curdles into shame; counted with a witness it becomes "
        "planning. <b>Decide the next year on purpose</b>: same, more, or less — but chosen, "
        "scheduled, fee-shopped. Expect the evening to be emotional: the number is usually "
        "bigger than feared, the first reaction is often grief — and then, in nearly every "
        "account members have shared, something unexpected: <b>pride</b>. You have been "
        "running a small development agency out of a salary. Now run it with books.", body),
]

# ================= 11 & 12 =================
story += [
    PageBreak(),
    Paragraph("11 · From a Sigh to a System", h2),
    fig("system.png",
        "Fig 8 — Five moves, none of which is “send less”.", max_h=105 * mm),
    Paragraph(
        "<b>Shop the corridor</b> — Section 06's €250-a-year lever. <b>Schedule the "
        "routine</b> — a standing transfer, sized on purpose; predictable money is a gift to "
        "the family too, who can finally plan instead of petition. <b>Batch the send</b> — "
        "fewer, larger transfers beat many small ones wherever fixed fees bite, and non-urgent "
        "requests ride the next scheduled send: “I send on the 28th” converts you from an ATM "
        "into an institution. <b>Build the anti-emergency fund</b> — three months of the "
        "routine amount, held for home; most “emergencies”, counted, turn out to be Januaries. "
        "<b>Name the destination</b> — staying, returning, or both; a working answer lets the "
        "pension start, the house finish, and the temporary decade end on purpose. None of "
        "this reduces love. It removes the leak, the panic, and the dark.", body),

    Paragraph("12 · The African Advantage", h2),
    Paragraph(
        "The letter's deepest irony: <b>the culture it teases is one of the best accounting "
        "cultures on earth — communally.</b> The harambee keeps a written list of every "
        "contributor, read aloud. The chama's books balance to the cent, monthly, for decades. "
        "The wedding committee publishes its budget; the burial society audits itself. Nobody "
        "thinks counting <i>shared</i> money is unloving — counting is how the community "
        "protects what it loves. The uncounted year is the strange exception: <b>the only "
        "ledger our culture refuses to keep is the one where the self is the beneficiary.</b>", body),
    Paragraph(
        "So the fix is not imported financial literacy — the literacy is indigenous and "
        "world-class. The fix is jurisdiction: <b>move your own year into the accounting "
        "tradition you already trust.</b> Treat yourself as a one-person chama: a ten-minute "
        "monthly meeting, recorded contributions, audited books, and the agenda item the group "
        "version always has — <i>what are we building?</i> Some members have run an annual "
        "counted-year round inside their actual chamas. The room, one wrote to us, went from "
        "jokes to silence to the most useful money conversation of their lives.", body),
]

# ================= 13 =================
story += [
    PageBreak(),
    Paragraph("13 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First: the sigh has beneficiaries, and one of them is you.</b> Opacity is not only "
        "imposed by expectations; it is chosen, because the uncounted arrangement spares the "
        "sender the hardest conversations — the boundary never drawn, the “no” never "
        "practised, the plan never proposed. As long as nobody counts, nobody has to "
        "negotiate. Counting ends your innocence too: once you know the number, continuing "
        "exactly as before becomes a decision rather than a drift — and some readers will "
        "close this report rather than accept that. The letter, with love, was betting on it.", body),
    Paragraph(
        "<b>Second: the family cannot plan around a fog either.</b> The sigh reads as noble — "
        "give without counting — but from the receiving side, unpredictable money is hard to "
        "build on: nobody can commit to a school, a treatment plan, or a business on transfers "
        "that arrive by mood. The scheduled, counted, honest version is not stingier. It is "
        "the first version the family can actually use as a foundation instead of as weather.", body),
    Paragraph(
        "<b>Third: do not let the spreadsheet become the new performance.</b> There is a "
        "failure mode on the far side of counting — the convert who audits every €10, "
        "renegotiates grandmother's airtime, and confuses optimisation with wisdom. The count "
        "serves the love, not the reverse: some line items are sacred (the funeral "
        "contribution is not a leak; it is citizenship), some inefficiencies are "
        "relationships, and the correct amount of financial slack in an African family is "
        "never zero. The target: <b>not the sigh, not the audit — the system with a heart.</b> "
        "Count the year. Keep the love. Send on purpose.", body),
]

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("14 · Method &amp; Limits", h2),
    Paragraph("This report combines World Bank remittance pricing, behavioural-economics "
              "research on information avoidance, and this library's own prior arithmetic, as "
              "at 7 September 2026.", body),
]
story += bullets([
    "<b>This report began as a satirical letter</b> shared inside this network; its structure "
    "follows the letter's claims deliberately, and each was checked against data rather than "
    "assumed.",
    "<b>The 8.78% figure</b> is the World Bank Remittance Prices Worldwide average for "
    "sending $200 to Sub-Saharan Africa (Q1 2025); global average 6.49%, digital ~5%, SDG "
    "target 3%. Costs vary enormously by corridor and operator — the regional average is the "
    "honest headline, not a quote for your route. The $56bn is the 2024 SSA inflow estimate; "
    "recorded flows undercount informal channels.",
    "<b>The worked year is an illustration, not a survey finding.</b> Assumptions: €250/month "
    "routine sending; €1,350 episodic support; fees at the regional average applied to "
    "routine transfers only (episodic transfers also incur fees — the total is conservative); "
    "one visa cycle at typical European costs; €28,000 net income. No dataset measures the "
    "full annual outflow of individual African senders — that absence is itself a finding. "
    "Run your own numbers; the report exists so that you do.",
    "<b>The fee-leak decade</b> applies 8.78% versus 3% to €4,350 of yearly sending, "
    "compounded at an illustrative 5%. It is arithmetic, not a promise of investment "
    "performance.",
    "<b>The ostrich effect and information avoidance</b> are established findings (Karlsson, "
    "Loewenstein &amp; Seppi 2009; Sicherman et al.'s login data; Golman et al.'s 2017 "
    "review) from investor and general populations — no study measures remittance-statement "
    "avoidance specifically. The diaspora application is our synthesis, labelled as argument.",
    "<b>Nothing here is financial advice</b>, and the recommendations are provider-agnostic: "
    "compare corridors yourself, on your route, on the day. Where debt, tax or investment "
    "decisions follow from your counted year, a regulated adviser is the right next ask — and "
    "asking is the skill.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "World Bank Remittance Prices Worldwide and the Migration Data Portal remittance "
        "overview; Karlsson, Loewenstein &amp; Seppi (2009) on the ostrich effect; Sicherman, "
        "Loewenstein, Seppi &amp; Utkus on financial attention; Golman, Hagmann &amp; "
        "Loewenstein (2017) on information avoidance; and this library's own measurement in "
        "the black tax, visa treadmill, wealth-left-abroad, remittance-app and "
        "household-saving reports. Full inline links in the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, "
        "sit together, and bounce ideas. This research is part of an open library, free to "
        "read and share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/uncounted-year-2026<br/>"
        "Companion reports: The Black Tax Ledger · The Visa Treadmill · Why We Don't Ask · "
        "The Envy Economy<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
