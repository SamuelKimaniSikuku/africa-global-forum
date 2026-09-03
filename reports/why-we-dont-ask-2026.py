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
IMG = os.path.join(HERE, "why-we-dont-ask-2026", "img")
OUT = os.path.join(HERE, "why-we-dont-ask-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "Why We Don't Ask · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 3 September 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="Why We Don't Ask (2026)",
                      author="Africa Global Forum",
                      subject="Help-seeking, the burden belief, and the givers' paradox of the African diaspora")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("Why we", h1),
    Paragraph("don't ask.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "The cultures that invented the harambee — that fund a stranger's surgery in a weekend "
        "and remit billions home without a single contract — leave £24 billion in benefits "
        "unclaimed, use therapy at a fraction of need, and drive past the food bank while "
        "skipping meals. The givers' paradox: why the most generous people on earth struggle to "
        "request help from institutions, what the unasked question costs, the research showing "
        "we underestimate by half how many people would say yes — and how a community can make "
        "asking as honourable as giving.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("£24bn", big_num), Paragraph("50%", big_num),
    Paragraph("1 in 4", big_num), Paragraph("2 wks", big_num),
], [
    Paragraph("in UK benefits and support<br/>left unclaimed<br/>every single year", big_lbl),
    Paragraph("how far people underestimate<br/>others' willingness to say yes<br/>to a direct request", big_lbl),
    Paragraph("mixed-status immigrant<br/>families avoiding programs<br/>they legally qualify for", big_lbl),
    Paragraph("the rule: anything stuck two<br/>weeks — body, mind, debt,<br/>papers — has earned one ask", big_lbl),
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
    fig("givers_paradox.png",
        "Fig 1 — The same person occupies both columns. The asymmetry has a logic, and this "
        "report takes it apart.", max_h=90 * mm),
    Paragraph("Published September 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/why-we-dont-ask-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "A member of this network put it in one sentence at a meetup: “I have driven four people "
        "to the airport this month, and I have had a toothache since March.” Everyone laughed, "
        "because everyone recognised it. This report is about why the laughter was nervous.", body),
]
story += bullets([
    "<b>The paradox is real and measurable.</b> The populations that run the world's densest "
    "informal help systems — harambee, black tax, burial societies, the 3 a.m. airport run — are "
    "documented under-users of institutional help: Black adults use mental-health services at "
    "25% versus 38% for white adults, with African immigrants among the least-served groups; "
    "£24 billion in UK benefits goes unclaimed yearly; a fifth of eligible US workers never "
    "claims the EITC; one in four adults in mixed-status immigrant families avoids safety-net "
    "programs out of immigration fear.",
    "<b>The machinery is status, not ignorance.</b> Asking feels like a one-down display — the "
    "same social-rank circuitry that runs shame and envy reads a request as an announcement of "
    "falling. In the diaspora's two-mirrors world the reading doubles: asking confirms the host "
    "mirror's verdict that you are behind, and betrays the home mirror's image that you made it.",
    "<b>The burden belief is arithmetic run backwards.</b> In Flynn and Lake's studies, people "
    "underestimated by up to 50% how many others would agree to a direct request — while campus "
    "advisors <i>overestimated by 60%</i> how many students would come to them. Askers count "
    "the cost of the helper's yes; helpers feel the cost of saying no — and helping reliably "
    "<i>boosts</i> the helper's wellbeing. The help is overstocked. The asking is the shortage.",
    "<b>The communal paradox has a clean resolution: we are fluent in a different asking "
    "system.</b> Communal help runs on relationships, reciprocity ledgers and preserved "
    "dignity. Institutional help strips all three out and adds forms, records and means-testing "
    "— everything that made asking honourable removed, everything that makes it frightening "
    "added. We are not bad at asking. We are asked to ask in a foreign grammar.",
    "<b>The fix runs in both directions</b> — individuals learning to ask (specific, early, "
    "scripted, the two-week rule), and communities learning to be <i>askable</i>: leaders "
    "asking first, first asks answered fast, anonymous on-ramps, and the Forum translating "
    "communal asks into institutional resources. Asking, like confidence and voice, is built "
    "by reps.",
])
story += [
    Paragraph("We measure love in what we give and pride in what we never request. The first "
              "half built the strongest help network on earth. The second half is quietly "
              "starving inside it.", pull),
]

# ================= 02 =================
story += [
    PageBreak(),
    Paragraph("02 · The Givers' Paradox", h2),
    Paragraph(
        "African cultures are not merely willing to help; they are engineered around it. The "
        "harambee is a formal technology for aggregating help; the black tax moves tens of "
        "billions a year on nothing but obligation and love; burial societies execute "
        "international logistics that would humble a corporation; and every member of this "
        "network has housed, fed, fetched, funded or vouched for someone this year. Giving is "
        "not an act in our cultures. It is infrastructure.", body),
    Paragraph(
        "And yet: the toothache since March. The overdraft nobody knows about. The depression "
        "prayed over but never treated. The benefits never claimed by families who qualify three "
        "times over. If unwillingness to help were the cause, the first column could not exist. "
        "Something else is happening — something specific to <b>receiving</b>, and more specific "
        "still to receiving from <b>institutions</b>. That is the trail this report follows: the "
        "evidence, the cost, the machinery — status, the burden belief, the logic gap, the "
        "institutions — and then the rebuild.", body),

    Paragraph("03 · The Evidence of Not Asking", h2),
    fig("not_asked.png",
        "Fig 2 — Unclaimed help, measured. Policy in Practice names stigma as a leading cause — "
        "not just ignorance.", max_h=95 * mm),
]
story += bullets([
    "<b>Mental health:</b> US survey data puts service use at ~25% for Black adults versus ~38% "
    "for white adults, and research on African immigrants specifically finds them among the "
    "least likely of all groups to seek care — despite carrying migration stress, racism and "
    "dislocation. UK reviews list the barriers in order: stigma first.",
    "<b>Money already owed:</b> £24.1 billion in UK benefits goes unclaimed yearly — £11bn of "
    "it Universal Credit — with awareness, stigma and distrust named as the causes. In the US, "
    "roughly one in five eligible workers never claims the EITC. This is not charity being "
    "refused. It is your own tax money, budgeted for you, left on the table.",
    "<b>The chilling effect:</b> roughly one in six adults in immigrant families — one in four "
    "in mixed-status families — avoided safety-net programs for fear of green-card "
    "consequences, keeping an estimated three to four million children from help they qualify "
    "for. Fear, not eligibility, is the gatekeeper.",
    "<b>And the quiet categories:</b> legal questions DIY-ed until they become removal "
    "proceedings; food banks under-used at comparable need; fee waivers, hardship funds and "
    "extensions unrequested by exactly the students working three jobs. The pattern repeats at "
    "every desk: the help exists, the eligibility exists, and the ask never arrives.",
])

# ================= 04 =================
story += [
    Paragraph("04 · The Price of the Unasked Question", h2),
    fig("price.png",
        "Fig 3 — Pride compounds like the fees in the black tax ledger — quietly, and against "
        "you.", max_h=105 * mm),
    Paragraph(
        "Not-asking presents itself as free — that is its trick. But the unasked question "
        "compounds like the deferral ledger: the symptom Googled for two years arrives at the "
        "clinic two stages later; the visa form filled alone to save a £150 consultation "
        "returns as a refusal, an appeal, and a £5,000 lawyer; the unclaimed entitlement "
        "forfeits thousands a year from families sending 15% of income home; the uncarried "
        "load arrives all at once, as collapse, at the worst possible price. Our investment-"
        "failure research found the same signature: losses cluster where nobody asked anyone "
        "anything before wiring the money.", body),
    Paragraph(
        "And the subtler line item: <b>the isolation dividend</b>. Every ask is a relationship "
        "under construction — the person who helped you convert your licence is now invested in "
        "your career, and the Franklin effect means people who help you come to like you more. "
        "The non-asker forfeits all of it: competence private, struggles private, network "
        "exactly the size it was at the airport. In an economy where the front door discounts "
        "your name, the referral network built by asking is not a nicety. It is the side door — "
        "and pride keeps it locked from the inside.", body),
]

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("05 · What Asking Feels Like", h2),
    fig("status_math.png",
        "Fig 4 — The feelings are status machinery — honest instruments in a village "
        "hierarchy, miscalibrated in front of a benefits office."),
    Paragraph(
        "Asking is processed by the oldest accounting system we carry: <b>social rank</b>. "
        "Gilbert's research — the framework behind our shame and envy reports — shows the "
        "emotional palette evolved substantially to track standing: pride marks a rise, shame "
        "marks a fall, and <b>a request for help registers, in this ancient bookkeeping, as a "
        "voluntary one-down display</b>. The feeling is not irrational. It is a perfectly "
        "functioning instrument — calibrated for a world that no longer surrounds you.", body),
    Paragraph(
        "Migration triples the reading. In the two-mirrors economy, asking abroad confirms the "
        "host mirror's whisper that you are behind — and threatens the home mirror's portrait "
        "of the relative who made it: <i>how can the one in London be at a food bank?</i> Add "
        "the childhood training — a generation raised where questions were insolence and needs "
        "were not announced to adults — and the communal audit waiting behind any disclosure, "
        "and you get the full stack: <b>status alarm, image management in two directions, "
        "trained silence, and shame insurance, all firing over a request for a form.</b> Naming "
        "the stack is the beginning of disarming it: every layer is a feeling about asking — "
        "and not one of them is information about the actual price.", body),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · The Burden Arithmetic", h2),
    fig("underestimate.png",
        "Fig 5 — Flynn & Lake (2008): the help is overstocked; the asking is the shortage.",
        max_h=85 * mm),
    Paragraph(
        "“I don't want to be a burden” presents itself as consideration. The research says it "
        "is a calculation error — a large, systematic, replicated one. People about to ask "
        "strangers for favours <b>underestimated actual compliance by as much as 50%</b>. The "
        "mechanism is an empathy gap: <b>askers fixate on the cost of saying yes</b> (the "
        "helper's time and effort) <b>while the people asked feel the cost of saying no</b> — "
        "the social discomfort of refusing a human being to their face. You are budgeting their "
        "generosity using your anxiety as the price list.", body),
    Paragraph(
        "The companion findings complete the demolition. Campus peer advisors <b>overestimated "
        "by 60% how many students would come to them</b> — the helpers are stocked and waiting, "
        "wondering why nobody asks. Decades of research find giving help improves the helper's "
        "mood and sense of meaning — which every African knows from the giving side: think what "
        "it does for <i>you</i> to be the one who could help. Refusing to ask does not spare "
        "people that burden. <b>It denies them that gift.</b> And the Franklin effect adds the "
        "final inversion: people who have helped you like you <i>more</i> afterwards. The "
        "burden arithmetic, run correctly: a specific, honest ask is cheap for them, pleasant "
        "for them, bonding for both of you — and priceless for you.", body),
]

# ================= 07 =================
story += [
    PageBreak(),
    Paragraph("07 · The Two Logics of Help", h2),
    fig("two_logics.png",
        "Fig 6 — The communal paradox, resolved: not an inability to ask — fluency in a "
        "different asking system."),
    Paragraph(
        "African cultures ask <i>constantly</i> — through a specific technology. The communal "
        "ask travels along a <b>relationship</b>: the person asked knows your whole story. It "
        "sits in a <b>reciprocity ledger</b>: today's request is yesterday's contribution and "
        "tomorrow's repayment — receiving is not falling; it is taking your turn. It leaves "
        "<b>no record</b>. And it preserves <b>dignity by design</b>: at a harambee the "
        "recipient stands publicly, named and honoured, while the whole community gives.", body),
    Paragraph(
        "Now walk the same person to an institution. The desk is a <b>stranger</b> who needs "
        "the whole humiliating story from zero. There is <b>no ledger</b> — nothing to repay, "
        "which is precisely why it feels like begging: our cultures define begging as asking "
        "<i>outside the reciprocity system</i>. Everything is <b>written down</b>. And the "
        "means test inverts the harambee's dignity: instead of standing honoured while the "
        "community gives, you sit suspected while an official verifies you are genuinely "
        "failing. <b>Every feature that made asking honourable has been stripped out; every "
        "feature that makes it frightening has been added.</b> The under-asking is not a "
        "cultural defect meeting a neutral system. It is a sophisticated asking culture meeting "
        "a system built in a different grammar — and as with time, attention and voice, the "
        "answer is translation, not conversion.", body),
    Paragraph("In our grammar, asking a stranger with nothing to repay is begging. The system "
              "calls it “accessing services”. Nobody translated — so a generation chose hunger "
              "over what was mislabelled as shame.", pull),
]

# ================= 08 & 09 =================
story += [
    PageBreak(),
    Paragraph("08 · The Institution Gap", h2),
]
story += bullets([
    "<b>The immigration shadow is real.</b> The public-charge era taught immigrant families "
    "that using benefits could cost them status — and the chilling effect outlived the rule: "
    "one in six immigrant families still avoids programs they legally qualify for. “They will "
    "write it down” is not superstition; it is a lesson recently taught.",
    "<b>The clinical distrust has receipts</b> — from documented racial bias in treatment to "
    "the UK pattern where Black patients are over-represented in coercive psychiatry and "
    "under-represented in voluntary therapy. When the front door mistreats people, the "
    "community learns to use no door at all.",
    "<b>The church became the trusted institution for a reason</b> — it runs on the communal "
    "grammar: known faces, no files, prayer instead of paperwork, dignity intact. The honest "
    "limit: a pastor can hold your hand through depression but cannot prescribe for it. The "
    "trusted institution and the equipped institution are, too often, different buildings.",
    "<b>But note what earned distrust cannot explain:</b> the unclaimed EITC requires no "
    "interview; the untouched fee waiver carries no immigration risk. The rational distrust is "
    "real — and it has become a cover story for the status machinery. Both lists deserve "
    "respect. Only one should be getting your excuses.",
])
story += [
    Paragraph("09 · What the Successful Ask", h2),
    Paragraph(
        "The fastest way to kill a false belief is to look at who does not hold it. <b>The most "
        "successful people you can name are professional askers.</b> Executives retain coaches "
        "— paid help-asking about their own jobs. The wealthy assemble advisors and ask them "
        "constantly. Surgeons request consults as routine. Go up any hierarchy and the density "
        "of asking <i>rises</i>: the junior engineer struggles alone for a week; the principal "
        "engineer asks in the first hour, because their time is too valuable for pride.", body),
    Paragraph(
        "Read that against the status math and the inversion completes: <b>asking is not a "
        "display of low status. Hoarding problems is.</b> Edmondson's psychological-safety "
        "research found the best teams report the most problems, because surfacing them is "
        "safe and useful; the worst teams are silent. The same is true of lives. The diaspora's "
        "most quietly successful members are, look closely, its best askers — the one who asked "
        "which accountant, which broker, which school, which lawyer, and compounded every "
        "answer. They were never less proud than you. They just ran the arithmetic correctly.",
        body),
]

# ================= 10 =================
story += [
    PageBreak(),
    Paragraph("10 · How to Ask", h2),
    fig("how_to_ask.png",
        "Fig 7 — The mechanics, for people trained not to. Asking is built by reps, like "
        "confidence and voice.", max_h=105 * mm),
    Paragraph(
        "<b>Ask specific, not vague</b>: “which of these two visa routes did you take, and "
        "why?” is a two-minute yes; “any advice?” is homework nobody starts. <b>Borrow the "
        "first ask</b>: the warm referral — “my cousin said to call you” — wraps the "
        "institutional stranger in a communal relationship; use it deliberately. <b>Script "
        "it</b>: three sentences — situation, what you tried, what you need — written before "
        "courage is consulted. <b>Run the two-week rule</b>: anything you have been stuck on "
        "for two weeks — a form, a symptom, a debt, a grief — has earned one ask, to one "
        "person or one service. This single rule, kept honestly, would recover most of what "
        "Section 04 priced. And <b>ask early, while it is small</b>: questions are cheap at "
        "stage one and ruinous at stage four. Asking early is not weakness. It is arithmetic.",
        body),
]

# ================= 11 =================
story += [
    PageBreak(),
    Paragraph("11 · How to Be Askable", h2),
    fig("askable.png",
        "Fig 8 — The Forum's own playbook: designing a community where asking is as honourable "
        "as giving.", max_h=105 * mm),
    Paragraph(
        "A community's asking rate is a design outcome, not a character trait. <b>Leaders ask "
        "first</b>: nothing normalises asking like the strongest person in the room doing it "
        "publicly — one founder's visible “I need help with X” unlocks fifty private ones. "
        "<b>Answer the first ask fast</b>: someone's first request in years is a toe in the "
        "water; the speed and warmth of the response decides whether there is ever a second. "
        "<b>Build “who has done this?” channels</b>: the lowest-shame ask is procedural — not "
        "“I am struggling” but “who has converted a Kenyan licence / fought a refusal / found "
        "a therapist who understands black tax?” — it frames the asker as a navigator, not a "
        "case. <b>Keep anonymous on-ramps open</b>: our honest-questions series exists because "
        "thousands asked namelessly what they could not ask aloud; anonymity is the on-ramp, "
        "and the traffic proves the demand. And <b>translate, don't just refer</b>: the "
        "Forum's deepest job is the corridor between the two grammars — not a directory of "
        "services but a relationship that walks someone to the form, sits with them at the "
        "clinic, converts the institutional stranger into a warm ask. Every diaspora "
        "organisation says “community”. The measurable version: <b>how many unasked questions "
        "died inside it this year — and what did you build so fewer die next year?</b>", body),

    Paragraph("12 · The African Advantage", h2),
    Paragraph(
        "The harambee is not just giving technology — look again: it is <b>asking "
        "technology</b>. Someone must stand up, name the need, and put a number on it, in "
        "public — and the culture engineered that moment so thoroughly it became an honour "
        "instead of a humiliation: the announcement, the committee, the list, the celebration. "
        "Our ancestors solved the exact problem this report describes — <i>how do you make "
        "requesting help dignified?</i> — and solved it so well we forgot it was ever a "
        "problem. The shame at the benefits office is not ancestral. The <i>solution</i> is "
        "ancestral. What is missing is only the translation layer.", body),
    Paragraph(
        "That is the diaspora opportunity in one sentence: <b>we do not need to learn to ask; "
        "we need to re-house asking in structures we already trust.</b> The chama that adds a "
        "“who has done this?” round to its monthly meeting. The church that hosts the "
        "benefits-checker and the therapist alongside the prayer line. The WhatsApp group with "
        "a pinned form: <i>need something? Name it, or name it anonymously.</i> Communities "
        "that build these corridors will compound. The infrastructure took centuries to build. "
        "The retrofit takes a meeting.", body),
]

# ================= 13 =================
story += [
    Paragraph("13 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First: pride is a bill someone else pays.</b> The unasked question is billed to "
        "your children, who inherit the crisis it grew into; to your spouse, who watches the "
        "toothache-since-March and the overdraft-nobody-knows; to the friends who would have "
        "gladly helped at stage one and instead attend the emergency at stage four. Refusing "
        "to ask feels like carrying your own weight. Run the accounts honestly and it is often "
        "the opposite: quietly transferring the load, with interest, to the people you were "
        "protecting from it.", body),
    Paragraph(
        "<b>Second: we make asking hard for each other, then mourn that nobody asks.</b> The "
        "community that laments a brother who suffered in silence is often the same one that "
        "taxes disclosure — the gossip about the one who went to therapy, the “prayer request” "
        "that becomes news by Sunday, the audit waiting behind every confession. You cannot "
        "run a shame economy and a support network on the same rails. Every time we punish an "
        "honest ask, we teach ten witnesses to keep quiet — and the funeral eulogy's “he never "
        "told anyone” is, partly, a review of us.", body),
    Paragraph(
        "<b>Third: the informal network has limits, and pretending otherwise costs lives.</b> "
        "The aunty network is magnificent, and it cannot diagnose diabetes, litigate a "
        "refusal, or treat clinical depression — and saying so is not disloyalty; it is "
        "respect for the stakes. Sometimes “we take care of our own” functions as a wall that "
        "keeps members from care the community cannot actually provide, while providing the "
        "community an alibi. The mature position keeps both: the communal system for what it "
        "does better than any institution on earth — presence, dignity, belonging, the 3 a.m. "
        "pickup — and the institutional system for what love alone cannot do. Knowing which "
        "need belongs to which system, and moving between them without shame, is the whole "
        "skill this report exists to teach.", body),
]

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("14 · Method &amp; Limits", h2),
    Paragraph("This report combines help-seeking research, benefits-uptake data, "
              "immigration-policy research and social psychology, as at 3 September 2026.", body),
]
story += bullets([
    "<b>The utilisation gaps are documented but coarse.</b> The US mental-health figures "
    "(~25% vs ~38%) are national survey data for Black versus white adults broadly; African-"
    "immigrant-specific rates come from smaller studies and reviews that consistently find "
    "lower use, without one canonical percentage. Under-use relative to <i>need</i> is the "
    "consistent finding.",
    "<b>The unclaimed-benefits figures</b> (£24.1bn UK; ~20% EITC non-participation) are "
    "population-wide, not diaspora-specific — no dataset isolates African-diaspora claiming "
    "rates. The chilling-effect data (Urban Institute) is the immigrant-specific layer.",
    "<b>The Flynn &amp; Lake findings</b> come from US samples asking small favours; effect "
    "sizes for high-stakes institutional asks are plausibly different. The direction — "
    "systematic underestimation of others' willingness — is well replicated.",
    "<b>The status-machinery framing and the two-logics analysis are our syntheses</b> — "
    "established mechanisms applied to diaspora help-seeking by argument, ethnographically "
    "grounded, labelled as argument. The same holds for reading the harambee as asking "
    "technology.",
    "<b>The earned-distrust section</b> reflects documented policy history and clinical "
    "disparities; the claim that rational distrust also serves as cover story for status "
    "avoidance is our interpretation, flagged as such.",
    "<b>Part of the psychological framework reached us through a secondary source</b> — Mark "
    "Manson's <i>Social Comparison Guide</i>, shared by a member of this network. We cite the "
    "primary literature (Gilbert, Flynn &amp; Lake, Edmondson); the guide is credited as the "
    "pointer, not as evidence.",
    "<b>Nothing here is clinical advice — except this one instruction, which is:</b> if any "
    "question in your life has been unasked for more than two weeks and involves your body, "
    "your mind, your debts or your papers, the two-week rule applies today. That is the whole "
    "report in one sentence, and it is the one to act on.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "SAMHSA/NSDUH data on mental-health service use by race; Bassey et al. (2024) "
        "systematic review of barriers among African immigrants in the UK; Policy in Practice, "
        "Missing Out, on unclaimed UK benefits; IRS EITC participation data; Urban Institute "
        "chilling-effect research; Flynn &amp; Lake (2008) and Bohns' help-seeking programme; "
        "Gilbert on social rank; Vogel and Corrigan on help-seeking self-stigma; Edmondson "
        "(1999) on psychological safety. Located partly via Mark Manson's Social Comparison "
        "Guide. Full inline links in the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, "
        "sit together, and bounce ideas. This research is part of an open library, free to "
        "read and share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/why-we-dont-ask-2026<br/>"
        "Companion reports: What Will People Say? · The Black Tax Ledger · The Envy Economy · "
        "Seen and Not Heard<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
