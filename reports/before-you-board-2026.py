#!/usr/bin/env python3
"""Generate the AGF report PDF: Before You Board — Studying Abroad in the AI Era (2026)."""

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
IMG = os.path.join(HERE, "before-you-board-2026", "img")
OUT = os.path.join(HERE, "before-you-board-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "Before You Board · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 15 September 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="Before You Board (2026)",
                      author="Africa Global Forum",
                      subject="The international student's guide to studying abroad in the AI era: how graduate recruitment changed, and the playbooks for new and experienced students")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("Before You", h1),
    Paragraph("board.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "The report we wish someone handed out at every education fair. 7.3 million "
        "students now study abroad — and the deal most are buying quietly changed while "
        "the brochures stayed the same: UK graduate postings down 45% in a year, ~140 "
        "applications per vacancy, 73% of employers screening with AI, post-study visas "
        "shortening everywhere. Not a report telling you to stay home — a pre-departure "
        "briefing: how the AI squeeze happened, what it means at each gate, and two "
        "complete playbooks — one for the student going fresh, one for the professional "
        "going after years of Kenyan experience.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("7.3m", big_num), Paragraph("~140", big_num),
    Paragraph("92% vs 65%", big_num), Paragraph("24→18", big_num),
], [
    Paragraph("students studying abroad<br/>worldwide — 15,526 of them<br/>Kenyan (UNESCO)", big_lbl),
    Paragraph("applications per UK grad<br/>vacancy, up from 86 —<br/>73% AI-screened first", big_lbl),
    Paragraph("employed within 6 months,<br/>with vs without co-op —<br/>the loudest number here", big_lbl),
    Paragraph("post-study months in the<br/>UK from January 2027 —<br/>the clock shrinks", big_lbl),
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
    fig("squeeze.png",
        "Fig 1 — How the recruitment machine broke, 2022–2026. Not a crash: a repricing "
        "of the bottom rung.", max_h=78 * mm),
    Paragraph("Published September 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/before-you-board-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "If you are planning to study abroad — or funding someone who is — here is the "
        "whole report in five findings:", body),
]
story += bullets([
    "<b>The product changed; the marketing did not.</b> A foreign degree really sold a "
    "SEQUENCE: degree → graduate job → sponsorship → career. AI broke the second link. UK "
    "graduate postings fell 45% in a year; large employers report ~140 applications per "
    "vacancy (up from 86); 73% of employers screen with AI. The degree still teaches. It "
    "no longer converts on its own.",
    "<b>The squeeze is specific, dated and measurable</b> — not a mood. Since ChatGPT "
    "(Nov 2022): entry vacancies down ~1/3; US 22–25s in AI-exposed occupations ~19% "
    "below trend while experienced workers hold (Stanford); policy tightening stacked on "
    "top in all four destinations.",
    "<b>The visa clock makes it your problem more than your classmates'.</b> Two gates on "
    "one fixed clock: a shrunken market, and sponsorship thresholds (UK £41,700) priced "
    "above junior pay — inside a window the UK cuts from 24 to 18 months in January 2027.",
    "<b>It is still worth going — for the right plan.</b> The strongest number here: "
    "Canadian international students with co-op experience are 92% employed within six "
    "months; without, 65%. Value moved from the degree to what surrounds it. HESA still "
    "finds 78% of international graduates employed at 15 months — narrower, not shut.",
    "<b>Experience at home is now a visa strategy.</b> Two to five Kenyan years before a "
    "targeted one-year master's lands you above the entry squeeze, at salaries that clear "
    "the thresholds. Section 09 is that playbook.",
])
story += [
    Paragraph(
        "Nobody at the education fair is paid to tell you the exit changed. This report "
        "is the missing page in the brochure.", pull),
]

# ================= 02 =================
story += [
    Paragraph("02 · The Seven-Million Question", h2),
    fig("lecture_hall.png",
        "Fig 2 — The scale of the journey (UNESCO; Kenya sector reporting).", max_h=105 * mm),
    Paragraph(
        "About 7.3 million students are enrolled in higher education outside their own "
        "country — up from 2.1 million in 2000: mobility tripled in a generation. Roughly "
        "430,000 come from Sub-Saharan Africa, with Nigeria, Ghana and Kenya the dominant "
        "senders; UNESCO counted 15,526 Kenyan students abroad in 2023 (Australia, the US "
        "and the UK the top hosts), and around 44% of surveyed Kenyan students say they "
        "want to study overseas. The queue behind the queue is enormous.", body),
    Paragraph(
        "Two consequences. First, you compete against seven million mobile peers aimed at "
        "the same four Anglophone destinations and the same “safe” courses — so "
        "differentiation beats credentials. Second, host politics noticed the scale: every "
        "major destination spent 2024–2026 tightening the student-to-work pipeline. The "
        "tightening is not aimed at you. It will hit you anyway — unless you route around "
        "it.", body),
]

# ================= 03 =================
story += [
    Paragraph("03 · The Deal You Were Sold", h2),
    fig("old_deal.png",
        "Fig 3 — The bargain, before and after. The degree still teaches; it no longer "
        "converts on its own.", max_h=110 * mm),
    Paragraph(
        "The sequence that worked for two decades — degree → graduate job in the "
        "post-study window → sponsorship → the life — ran on a bargain: employers bought "
        "graduates in bulk and paid for training with two years of supervised routine "
        "work, because someone had to do the routine work. The post-study visa was "
        "generous runway; junior sponsorship was routine; almost any recognised degree "
        "was the ticket. Relatives who travelled in 2010 or 2015 are not lying when they "
        "describe this world. They are describing a discontinued product.", body),
    Paragraph(
        "Hold the load-bearing detail: the entry job existed because the routine work "
        "existed. Nobody hired juniors out of kindness. Then a machine arrived that does "
        "routine work.", body),
]

# ================= 04 =================
story += [
    Paragraph("04 · How the Machine Broke: The Squeeze, Dated", h2),
    Paragraph(
        "November 2022: generative AI ships; its first proven competence is exactly the "
        "routine information work entry jobs were made of. 2023–2024: employers do not "
        "fire juniors — they quietly stop replacing them; entry vacancies drift down "
        "roughly a third while total employment stays healthy, so nothing makes "
        "headlines. 2025: the squeeze becomes measurable — UK graduate postings drop 45% "
        "in a year to their lowest since 2018; Stanford's payroll research shows 22–25s "
        "in AI-exposed occupations ~19% below trend while experienced workers in the "
        "same occupations hold or gain. 2025–2026: both doors narrow at once — 73% of "
        "employers screen with AI, applications explode to ~140 per vacancy (AI made "
        "applying effortless too, clogging the funnel), and all four destination "
        "governments tighten student routes. 2026: the new bar settles — surviving entry "
        "roles demand AI-fluency plus evidence of real work, and bulk hirers run "
        "calendar-locked pipelines: miss the autumn window, wait a year.", body),
    Paragraph(
        "Two honesty notes. The attribution is contested — LinkedIn's data blames rates "
        "more than AI; a Danish study found no average effect in its window — but the "
        "door is narrower under every explanation. And it is a squeeze, not a wall: HESA "
        "still finds 78% of international graduates in work at 15 months, and some "
        "employers are expanding entry hiring (IBM says it is tripling US entry intake "
        "in 2026). People get through. The question is which people, and how.", body),
]
story += [
    Paragraph(
        "The evidence base has thickened, in both directions. Stanford's number read as "
        "an index: both groups at 100 in November 2022; by June 2026 the most-exposed "
        "young workers sit at 89 while less-exposed peers sit at 110 — a ~19% RELATIVE "
        "gap, hiring-driven, not firings. A US Census working paper corroborates it "
        "(22–24s ~12% lower in the most-exposed industry groups through mid-2025). And "
        "on the other side, a Federal Reserve study found NO association between firms' "
        "AI adoption and fewer total postings (Sept 2023–Nov 2025): total vacancies "
        "hold while opportunity shifts away from particular junior roles. Together: not "
        "fewer jobs overall — a different door. The New York Fed adds the widest "
        "context: recent-graduate unemployment ~5.6%, and 42% of employed recent US "
        "graduates in occupations that do not typically require a degree — "
        "employed-and-stuck, measured at national scale.", body),
]

# ================= 05 =================
story += [
    Paragraph("05 · Two Gates, One Clock", h2),
    fig("two_clocks.png",
        "Fig 4 — The structural asymmetry every international student inherits.", max_h=112 * mm),
    Paragraph(
        "The local graduate who cannot find work moves home, temps, retries next cycle. "
        "You cannot: your post-study permission is a fixed clock — two years in the UK "
        "today, 18 months under the post-January-2027 rules, one to three elsewhere — "
        "and it starts at graduation, the precise moment the market gate is narrowest. "
        "Behind it stands the visa gate: the UK threshold at £41,700, above most junior "
        "pay, so even a graduate who wins a rare entry seat may find it cannot legally "
        "sponsor them. Add the employer's calculus — why pay visa fees for a junior when "
        "AI plus abundant local applicants exist? Sponsorship did not vanish; it migrated "
        "UP the ladder and OUT to the shortage lists.", body),
    Paragraph(
        "The door abroad is open at the top of the ladder and at the hands-and-heart "
        "occupations — and nearly shut at the generic junior office rung in between. "
        "Every move in this report is a way of arriving at an open door.", pull),
]

# ================= 06 =================
story += [
    Paragraph("06 · The Numbers the Education Fair Skips", h2),
]
story += bullets([
    "<b>78% — and its shadow.</b> HESA: 78% of international graduates employed at 15 "
    "months. But “employed” includes any work — Eurostat finds 41.4% of employed "
    "tertiary-educated non-EU citizens working below their qualification, versus 20% of "
    "nationals. Employed-and-stuck is the modal bad outcome, not jobless.",
    "<b>92% versus 65%.</b> Statistics Canada: co-op students 92% employed within six "
    "months; without co-op, 65%. A 27-point gap from one design choice made before "
    "enrolment. Choose the placement, not the prestige.",
    "<b>~140 applications per vacancy</b> — so rejection counts carry almost no "
    "information about you. Budget for volume, design for referrals: the side door beats "
    "the front portal, where AI reads applications AI wrote. And detectors false-flag "
    "non-native English at up to 61.3% — keep your own voice, keep drafts.",
    "<b>24 → 18 months.</b> The UK Graduate Route shrinks for post-January-2027 "
    "applicants. An 18-month clock means job-hunting starts in final year, not after it.",
    "<b>The gap narrows with time — and the language trap is real.</b> OECD: "
    "international graduates have weaker EARLY outcomes than domestic peers, the gap "
    "narrowing over years — the first eighteen months are the hard part by design. And "
    "an English-taught course is not an English-speaking labour market: if the jobs "
    "are advertised in French or German, start the language before you fly.",
])
story += [
    Paragraph("The fair sells the entrance. Buy the exit.", pull),
]

# ================= 07 =================
story += [
    Paragraph("07 · Still Worth Going?", h2),
    fig("fork.png",
        "Fig 5 — Not a verdict — a fork. Run your own plan down both columns before "
        "anyone pays anything.", max_h=112 * mm),
    Paragraph(
        "Green lights: a licensed or shortage-list field (health, care, teaching, "
        "engineering, trades — the occupations that keep dedicated visa routes); a FUNDED "
        "postgraduate offer, which caps the downside; a degree with co-op or placement "
        "built in (the 92/65 split is the loudest signal in this report); or experience "
        "already banked at home. Re-think first: a generic business or general-IT degree "
        "on loans with no placement and no shortage link — the exact profile the squeeze "
        "targets; a plan whose second step is “figure it out there”; choosing a "
        "university for its name rather than its route; and any plan where failure sinks "
        "the family.", body),
    Paragraph(
        "The fork is not STEM-versus-arts and not stay-home. A literature student with a "
        "placement year, a portfolio and a teaching pathway out-positions a "
        "computer-science student with none of the three. It is routine-versus-judgement "
        "and generic-versus-evidenced — applied to the biggest purchase your family may "
        "ever make.", body),
]

# ================= 08 =================
story += [
    Paragraph("08 · The New Student's Playbook", h2),
    Paragraph(
        "Coming fresh — straight from KCSE or a first degree, no professional experience "
        "yet. You have the hardest version of the problem, so your playbook starts "
        "earliest:", body),
]
story += bullets([
    "<b>Pick the course for the exit, not the entrance.</b> Which occupation, on which "
    "visa list, at what salary? Read thirty current postings in your intended field and "
    "destination, and check the official sponsor register — not the agent's assurance.",
    "<b>Make placement the tie-breaker.</b> Between two offers, take the co-op year, "
    "sandwich placement or clinical hours — even at the lower-ranked institution. 92/65 "
    "is the closest thing to a cheat code this market offers.",
    "<b>Treat year one as job-search year one.</b> The 18-month clock kills final-year "
    "job-hunting. Societies immediately; field-relevant part-time work where visa hours "
    "allow; one real, clickable project shipped per year.",
    "<b>Build the referral network before you need it.</b> At 140-to-1 the portal is a "
    "lottery; the side doors are not. Professors, placement supervisors, alumni — "
    "infrastructure, not networking theatre.",
    "<b>Use AI like a professional, not a student.</b> Tool-fluency is the new baseline "
    "— but keep unaided practice (students who let the chatbot think scored 17% worse "
    "without it), and keep applications in your own voice.",
    "<b>Know your fallback rung before the clock starts.</b> Price the home option in "
    "year one, not month seventeen. A fallback priced early is a strategy; priced late, "
    "a defeat.",
])
story += [
    Paragraph(
        "Before anyone pays a deposit, sit the plan for the seven-question exam: which "
        "jobs am I targeting and who recruits my profile; what does THIS course add; "
        "can I verify the qualification and get real supervised practice; what happened "
        "to recent international graduates, including those still searching; what "
        "language and permit conditions apply in MY graduation year; can I afford the "
        "course AND a slower search without unconfirmed earnings; and what will I do — "
        "on what date — if the job does not arrive? Proceed when every answer is "
        "concrete; reconsider when the plan rests on a promised job, an unverified visa "
        "claim, or the idea that one more qualification fixes every gap. And one habit "
        "that doubles as career insurance: learn each subject well enough to recognise "
        "a wrong answer — practise without AI first, then compare. A polished "
        "submission is weak evidence of learning if you cannot explain it, and "
        "interviewers now check exactly that.", body),
]

# ================= 09 =================
story += [
    Paragraph("09 · Coming With Experience: The Kenyan Professional's Playbook", h2),
    fig("personas.png",
        "Fig 6 — Same destination, different games. The experienced applicant plays the "
        "stronger hand — if they refuse to play it as a fresh graduate.", max_h=112 * mm),
    Paragraph(
        "You have three, five, eight years of real Kenyan work and are considering a "
        "master's abroad. Your position inverted: in the old market, going late felt "
        "like going behind; in this market you are the strong applicant. The squeeze ate "
        "the entry rung, not the middle; thresholds that block juniors are trivial for "
        "mid-level roles; and the mid-level premium — firms that stopped training "
        "juniors still need tomorrow's seniors — is bidding up exactly your profile. "
        "Your experience is not a footnote on the CV. It is the visa strategy.", body),
]
story += bullets([
    "<b>Go for conversion, not repetition.</b> A one-year master's that renames what you "
    "already do for the new market — finance to fintech, nursing to specialist practice "
    "— not a from-scratch pivot that resets you to the squeezed rung.",
    "<b>Apply at your level, ruthlessly.</b> A professional with six Kenyan years in a "
    "graduate-scheme queue has entered the 140-to-1 lottery with the weakest cohort. The "
    "same person at mid-level is scarce, sponsorable and above the threshold.",
    "<b>Sell the Africa premium, not around it.</b> You managed through failing "
    "infrastructure, cash customers and shifting regulation — capability every "
    "multinational building African expertise wants. Frame it as capability, not "
    "geography.",
    "<b>Time the master's to the clock.</b> Mid-level hiring runs year-round, unlike "
    "graduate schemes — so post-study months are genuinely usable runway, if the search "
    "starts at enrolment.",
    "<b>Keep the Kenya door open on purpose.</b> Network, track record, re-entry value: "
    "run home-first sequencing in both directions and price both doors every six months. "
    "The option itself is worth money.",
    "<b>First, define what the degree must change.</b> Continuing in your field "
    "(which local tools or rules are missing?); specialising (does the course teach a "
    "capability employers request, with practice?); changing careers (how much "
    "transfers, how much beginner training?); or mainly wanting the overseas move — "
    "then ask whether a direct search, internal transfer or shorter qualification "
    "reaches the goal at a fraction of the cost.",
    "<b>Titles are not levels — make the work easy to assess.</b> A Kenyan manager "
    "may fit an analyst, specialist or manager role abroad depending on the actual "
    "work. Write problem → action → measured result (\u201cled eight warehouse staff "
    "handling ~600 orders weekly; late dispatches fell 18% to 11% in 12 weeks\u201d — "
    "your own verified numbers), keep contactable references.",
    "<b>Mind the permit small print on survival jobs.</b> An unrelated job may not "
    "satisfy your NEXT residence permit's conditions (US OPT even caps unemployment "
    "days). Verify before relying on it; keep a dated plan for entering your "
    "profession alongside the job that funds the search.",
    "<b>If you have not left yet: bank the years first.</b> Two or three more Kenyan "
    "years convert you from the hard game to the strong one. The cousin who flew at 22 "
    "and the one who flew at 27 with a CV are playing different sports.",
])

# ================= 10 =================
story += [
    Paragraph("10 · The Six Destinations, Compared", h2),
    fig("destinations.png",
        "Fig 7 — Post-study routes per destination, from official guidance reviewed 15 "
        "September 2026 (gov.uk, IRCC, USCIS/DHS, German federal and French "
        "Service-Public pages, Australian Home Affairs). Re-read the official page "
        "before paying anything.", max_h=175 * mm),
    Paragraph(
        "The fine print that decides plans: the UK Graduate visa runs two years if "
        "applied for by 31 December 2026, 18 months from January 2027 — and THREE "
        "years for doctoral graduates. Canada's 3-year PGWP needs an eligible master's "
        "of at least eight months (a postgraduate certificate does not qualify), "
        "normally comes once per lifetime, and even passport validity can shorten it. "
        "The US OPT gives 12 months plus 24 for eligible STEM — but with only 90 days "
        "of permitted unemployment (150 total with STEM) it is not three years of open "
        "searching: go funded, go STEM, count the days. Germany offers the most "
        "generous search terms — 18 months, any work allowed meanwhile — but "
        "non-renewable, in a labour market that runs in German. France gives master's "
        "graduates 12 non-renewable months, with French-language hiring to match. Both "
        "continental routes carry the OECD warning: the course may be in English; the "
        "jobs are not.", body),
    Paragraph(
        "One line per country, for the family group chat: UK for licensed and "
        "mid-level; Canada for co-op undergraduates (degree, not certificate); US for "
        "funded STEM specialists who count their 90 days; Germany for engineers "
        "willing to learn German; France for francophone-ready master's graduates; "
        "Australia for young shortage-field applicants who read the age rule first.", body),
]

# ================= 11 =================
story += [
    Paragraph("11 · Ten Moves Before You Board", h2),
    fig("moves.png",
        "Fig 8 — The first five moves; the second five below. Print this page for the "
        "family meeting.", max_h=145 * mm),
]
story += bullets([
    "<b>1. Choose the exit before the entrance.</b> Occupation → visa route → course, in "
    "that order.",
    "<b>2. Put co-op or placement above ranking.</b> 92% versus 65%. A work term beats "
    "twenty league-table places.",
    "<b>3. Aim at shortage lists, not brochures.</b> Health, care, teaching, "
    "engineering, trades — the doors ageing countries cannot afford to close.",
    "<b>4. Bank experience at home first if you can.</b> Kenyan years + one-year "
    "master's = mid-level entry above the squeeze.",
    "<b>5. Stress-test the money for a slow start.</b> Twelve months without a graduate "
    "job, at local starting pay. If the plan only survives the best case, it is not a "
    "plan.",
    "<b>6. Verify sponsorship, not vibes.</b> The official register and current "
    "thresholds, checked yourself. Agents sell entrances; registers describe exits.",
    "<b>7. Run the 30-vacancy test.</b> Thirty real postings in your field and city: "
    "demands, pay, and whether the pay clears the threshold.",
    "<b>8. Start the job search at enrolment.</b> From month one, not month eighteen.",
    "<b>9. Keep your own voice in every application.</b> 61.3% detector false-positives "
    "on non-native writing, and a funnel full of identical AI letters: sounding like "
    "yourself is an advantage twice over.",
    "<b>10. Price the return option annually.</b> Portfolio management, not "
    "failure-planning. An option priced is an option owned.",
])
story += [
    Paragraph(
        "As a calendar: run the 30-day test before committing. Week 1 — pick two or "
        "three target roles, compare recent adverts in two destinations, map every "
        "requirement. Week 2 — talk to recent international graduates from your "
        "shortlisted courses, INCLUDING someone still searching or back home. Week 3 — "
        "demand course-specific outcomes and placement terms, check recognition and "
        "the work rules for your graduation year, write full cost against secured "
        "funding. Week 4 — finish a small project, have a professional review it, and "
        "compare proceeding now against a cheaper course, more Kenyan experience, or a "
        "deliberate delay. Thirty days of testing before three years of paying. Then in "
        "the first 90 days after landing: careers service, one professional "
        "association, employer deadlines mapped, the language routine started.", body),
]

# ================= 12 =================
story += [
    Paragraph("12 · The Family Briefing", h2),
    Paragraph(
        "Most study-abroad decisions in our community are family investments, so this "
        "section is for the funders. First: the investment case changed shape, not died "
        "— the fork in Section 07 is the underwriting checklist, and a green-light plan "
        "still carries strong odds. Second: run the stress test before the harambee — "
        "twelve months post-graduation without a professional job, at survival pay, with "
        "the clock running: can the family carry it without selling what cannot be "
        "re-bought? If not, change the plan, not the test. Third: measure the right "
        "thing — the first year abroad now normally contains rejection at industrial "
        "volume (140-to-1 is the market, not the child); judge placements won, projects "
        "shipped and referrals built, not speed to first job. Fourth: fund the things "
        "that compound — the laptop, the course, the certification — in both "
        "directions.", body),
    Paragraph(
        "The stress test with numbers on it — an illustrative one-year master's "
        "(replace every line with verified local figures): tuition €12,000 + twelve "
        "months' living at €1,000 + travel, visas, insurance and setup €2,000 = "
        "€26,000 — then add €6,000 for six months of post-graduation living without "
        "earnings: an honest total of €32,000 before contingency. The last line is the "
        "one families skip, and it decides whether the graduate can hold out for the "
        "right job or must grab the survival job that eats the visa clock. Treat "
        "permitted part-time hours as uncertain income, not budget; count deposits, "
        "borrowing costs and exchange-rate slippage; for the experienced applicant, "
        "add the Kenyan salary and progression forgone.", body),
]

# ================= 13 =================
story += [
    Paragraph("13 · The Uncomfortable Part", h2),
]
story += bullets([
    "<b>This network profits from the journey it is warning you about.</b> A diaspora "
    "forum writing a pre-departure briefing has an interest in departures. Our "
    "resolution: the question was never whether to go but when, at what rung, with what "
    "plan — and for some readers the honest answer is “later” or "
    "“differently,” which is advice against our own romance.",
    "<b>The squeeze's cause is contested even where its existence is not.</b> If rates, "
    "not AI, drove most of the freeze, a rate cycle could reopen doors faster than this "
    "report implies. The strategies survive either way; the urgency may not.",
    "<b>The destination frame still leans Anglophone-plus.</b> This update added "
    "France and Germany from official guidance — closing part of the first edition's "
    "admitted gap — but the Netherlands, the Gulf, China and intra-African routes "
    "remain outside the evidence base, and for some readers those doors are wider.",
    "<b>Playbooks are probabilities, not promises.</b> A student can make all ten moves "
    "and still lose the lottery year; another can wing it and land. Every claim is sized "
    "to its evidence; extrapolations are flagged in Section 14.",
])

# ================= 14 =================
story += [
    Paragraph("14 · Method & Limits", h2),
]
story += bullets([
    "<b>Student flows:</b> UNESCO (7.3M mobile students, 2025 report; 2.1M in 2000; "
    "15,526 Kenyans abroad, 2023) with SSA totals (~430,000) from sector analyses; the "
    "44% Kenyan aspiration figure is survey sentiment, not intent.",
    "<b>The squeeze:</b> UK postings (−45% YoY) and application volumes (~140 per "
    "vacancy, from 86) from 2026 UK graduate-market reporting; 73% AI-screening from "
    "employer surveys; Stanford payroll research (22–25s ~19% below trend — a relative "
    "shortfall, caveats in our New Ladder report); the attribution debate held open.",
    "<b>Outcomes:</b> HESA Graduate Outcomes (78% at 15 months — includes any work); "
    "Eurostat overqualification (41.4% vs 20%); Statistics Canada co-op split (92%/65% — "
    "strong signal, not pure causation: co-op students may differ in unobserved ways).",
    "<b>Policy (as at 15 Sep 2026):</b> UK Home Office (−36% YoY Skilled Worker grants; "
    "£41,700; Graduate Route 24→18 from 1 Jan 2027); IRCC caps and PGWP field rules; "
    "USCIS FY2026 (85k cap, registrations −27%) and the vacated-but-appealed $100k fee; "
    "Australian 485 rules. Policy is the fastest-moving layer — verify on official "
    "sites before acting; nothing here is immigration advice.",
    "<b>Corroborating and route evidence</b>, added from a member-shared dossier "
    "whose primary citations we verified and cite: the Stanford Aug 2026 revision read "
    "as an index (89 vs 110 from a common 100 — relative, hiring-driven, not causal); "
    "US Census CES WP 26-27 (~12% lower, 22–24s, through 2025 Q2); the Federal Reserve "
    "adoption-vs-postings null (2023–25); NY Fed dashboard (5.6% unemployment, 42% "
    "underemployment, 2026 Q2); OECD International Students in Higher Education (2026); "
    "and France/Germany/US route fine print from Service-Public, the German federal "
    "government, USCIS and DHS (12- and 18-month search permits; OPT's 90/150 "
    "unemployment days), reviewed 15 Sep 2026.",
    "<b>What is extrapolation:</b> the Section 04 timeline connects measured points into "
    "a narrative; the playbooks and destination one-liners are strategy synthesis; the "
    "experience-first thesis rests on the level-split evidence plus threshold arithmetic "
    "— an inference, flagged as such.",
    "<b>AI use in production:</b> drafted, charted and fact-checked with AI assistance "
    "under editorial control; every load-bearing number verified against the primary "
    "source. Flagged for revisit by mid-2027 — this market is moving.",
])
story += [
    Paragraph(
        "Companion reports — the AI quartet: The Algorithm at the Border, The New Ladder, "
        "The Leapfrog Test. All at africaglobalforum.com/reports. · Africa Global Forum · "
        "Research · 2026 · Free to read and share.", small),
]

doc.build(story)
print("PDF built:", OUT)
