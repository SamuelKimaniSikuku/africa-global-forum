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
IMG = os.path.join(HERE, "cost-of-later-2026", "img")
OUT = os.path.join(HERE, "cost-of-later-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Cost of Later · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 27 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Cost of Later (2026)",
                      author="Africa Global Forum",
                      subject="Procrastination, African time, and what delay really costs Africans abroad")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Cost of", h1),
    Paragraph("later.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Africans abroad carry a double accusation about time: the “African time” stereotype from "
        "outside, and a private guilt about the unsent application from inside. The data separates "
        "them cleanly. Lateness norms vary enormously by culture. Procrastination does not — "
        "chronic delay runs at roughly 14% in every country ever measured. This report is about "
        "the difference, what deferral actually costs the diaspora, and what gets the envelope "
        "opened.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("~14%", big_num), Paragraph("0", big_num),
    Paragraph("9.2m", big_num), Paragraph("8–11%", big_num),
], [
    Paragraph("of adults are chronic<br/>procrastinators — in every<br/>country ever measured", big_lbl),
    Paragraph("significant national<br/>differences found in the<br/>six-nation study", big_lbl),
    Paragraph("US green-card holders<br/>eligible for citizenship<br/>who have not applied", big_lbl),
    Paragraph("higher earnings for those<br/>who stopped deferring<br/>and naturalised", big_lbl),
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
    fig("same_everywhere.png",
        "Fig 1 — Chronic procrastination across six nations on three continents: roughly 14% "
        "everywhere, with no significant national differences (Ferrari et al., 2007).",
        max_h=90 * mm),
    Paragraph("Published August 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/cost-of-later-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "There is a joke every African abroad has heard twice — once from a colleague, once from a "
        "relative. The colleague makes it about the wedding that started three hours late. The "
        "relative makes it about you: <i>so you have been there five years and you still have not "
        "sorted your papers?</i> Two different accusations, one word — time — and almost "
        "everything written for our community treats them as the same failing. They are not, and "
        "the confusion is expensive.", body),
]
story += bullets([
    "<b>Procrastination is culture-blind.</b> Across nearly 1,400 adults in six nations on three "
    "continents, chronic procrastination ran at <b>roughly 14% everywhere — with no significant "
    "national differences at all</b>. African campuses tell the same story: ~80% of Ethiopian "
    "students and 87% of Tunisian medical students procrastinate — exactly the world student band "
    "of 80–95%.",
    "<b>What varies is time culture, not self-control.</b> Clock-time cultures let the schedule "
    "rule the event; event-time cultures let the event rule the schedule. Lateness norms differ "
    "hugely across that line. Private delay of important tasks does not. “African time” describes "
    "a lateness norm; the guilt you carry abroad is usually about something else entirely.",
    "<b>The real cost of later is not the party that starts at nine.</b> It is the deferral "
    "ledger: 9.2 million US green-card holders eligible for citizenship who have not applied — "
    "while naturalised citizens out-earn eligible non-applicants by 8–11%. The licence never "
    "converted, the screening never booked, the pension form in the drawer. Delay abroad "
    "compounds like the fees in our black tax ledger — quietly, and against you.",
    "<b>Procrastination is an emotional strategy, not a character flaw.</b> The research "
    "consensus is that procrastination is short-term mood repair: escaping the bad feeling a task "
    "carries by escaping the task. Migration loads tasks with heavier feelings — precarity, "
    "identity threat, shame with an audience back home — which is why capable people delay more "
    "abroad, not less.",
    "<b>What works is structural, not motivational:</b> visible stakes, tiny first moves, paid "
    "deposits, named feelings, borrowed witnesses. The communal accountability that ships African "
    "weddings on time — late start and all — is the machinery the research prescribes for the "
    "unsent form.",
])
story += [
    Paragraph("Nobody on earth procrastinates more than anyone else on earth. But some of us pay "
              "more per day of delay — and the diaspora pays the highest rate of all.", pull),
]

# ================= 02 & 03 =================
story += [
    PageBreak(),
    Paragraph("02 · The Double Accusation", h2),
    Paragraph(
        "At home, you were the person who made things happen — the one who organised the "
        "harambee, hit the deadline, ran the side hustle before lectures. Abroad, there is a form "
        "on your table that would change your legal life, and it has been there since March. You "
        "are not lazy; you work more hours than anyone you know. And still the envelope sits. Then "
        "add the outside voice: the “African time” joke follows you into rooms where you are the "
        "only African, so you overcorrect — first at every meeting, punctuality as armour — and "
        "the private form still sits. The stereotype polices the clock you share with others while "
        "the real damage happens on the clock nobody sees.", body),
    Paragraph(
        "This report takes the two accusations apart. One is a claim about <b>culture</b> — that "
        "Africans hold looser norms about shared schedules. It has real history and real content, "
        "and we treat it honestly. The other is a claim about <b>character</b> — that the delay on "
        "your table is a personal failing, perhaps a cultural inheritance. That claim is "
        "measurably false, and the demolition takes one chart.", body),

    Paragraph("03 · What Procrastination Actually Is", h2),
    Paragraph(
        "The standard research definition, from Steel’s landmark 2007 meta-analysis: "
        "<b>voluntarily delaying an intended action despite expecting to be worse off for the "
        "delay.</b> The delay must be unnecessary — triage under load is not procrastination, and "
        "much of what the diaspora calls laziness in itself is prioritisation that would break the "
        "people doing the judging. It must be against your own judgment — the Greeks called this "
        "<i>akrasia</i>. And it is ancient and universal: the oldest known complaint is an "
        "Egyptian hieroglyphic from ~1400 BC — an African document — “Friend, stop putting off "
        "work and allow us to go home in good time.” Roughly 95% of adults procrastinate at least "
        "occasionally; 15–20% chronically.", body),
    Paragraph(
        "One piece of history our community inherited twice: the Greeks saw akrasia as a mistake, "
        "not a sin. It was St. Augustine — a North African wrestling with his own delays ("
        "“Lord, make me pure… but not yet”) — whose theology turned failure-to-act into a "
        "<b>moral</b> failing, and the church built a thousand years of shame on it. African "
        "Christianity inherited the shame frame from the missionaries; the diaspora then "
        "inherited the secular version from hustle culture. The research verdict on both is the "
        "same: <b>shame does not cure procrastination; shame fuels it.</b>", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · The Numbers Nobody Separates", h2),
    Paragraph(
        "In 2007, Ferrari and colleagues measured chronic procrastination with the same "
        "instruments across six countries — rich and poor, clock-obsessed and famously relaxed. "
        "If procrastination were cultural, Spain and Venezuela should have differed from the "
        "United Kingdom. They did not. <b>Roughly 13.5% of adults everywhere were chronic arousal "
        "procrastinators</b> (the deadline-thrill type) <b>and about 14.6% chronic avoidant "
        "procrastinators</b> (the fear type) — in every country, with the researchers openly "
        "surprised by how flat the landscape was.", body),
    fig("students.png",
        "Fig 2 — African campuses sit exactly where the world’s campuses sit. There is no "
        "continent of delay and no continent of discipline."),
    Paragraph(
        "The African data lands in the same place: nearly 80% of students in Ethiopia’s Amhara "
        "region procrastinate to some degree; 87.2% of Tunisian medical students on the Tuckman "
        "scale; Sudanese and Nigerian campus studies report the same band. Steel’s worldwide "
        "figure is 80–95%. <b>African students procrastinate at precisely the world rate.</b> "
        "Not more, as the stereotype implies. Not less, as the counter-myth of the iron-"
        "disciplined immigrant implies. The same. Whatever “African time” is, it is not showing "
        "up in the procrastination instruments — and whatever is stopping you sending the form, "
        "it did not come from your grandmother.", body),
]

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("05 · Time Is a Dialect", h2),
    fig("two_columns.png",
        "Fig 3 — The distinction the whole report turns on. Lateness is a shared norm about "
        "clocks; procrastination is a private failure to act, constant across cultures."),
    Paragraph(
        "What does vary is time norms — enormously and measurably. <b>Clock-time cultures</b> "
        "(Germany, Switzerland, Japan, the urban Anglosphere) start events because the clock says "
        "so. <b>Event-time cultures</b> (much of Latin America, South Asia, the Middle East and "
        "Africa historically) start events when the participants and the moment are ready. In the "
        "classic 31-country pace-of-life study — walking speed, postal speed, clock accuracy — "
        "the fastest places were Switzerland, Ireland, Germany and Japan; the slowest measured "
        "were Brazil, Indonesia and Mexico. Pace tracked wealth, cold climates and individualism, "
        "not virtue — and the fast places paid for it in heart disease and smoking. <b>The clock "
        "is a technology with a price, not a moral standard.</b>", body),
]
story += bullets([
    "<b>“African time” is partly a colonial artefact.</b> The rigid clock arrived with the "
    "coloniser’s railway, factory and mission school, imposed on societies that ran sophisticated "
    "seasonal, agricultural and ritual calendars. Pre-colonial African life was not timeless; it "
    "kept time by different instruments. The stereotype measures distance from Greenwich "
    "discipline and calls the distance a defect.",
    "<b>Africa is not one time culture.</b> In a 2020 lateness-norms study, South African "
    "respondents patterned with the Dutch as a clock-time culture; it was Pakistani respondents "
    "who accepted longer delays. Lagos banking runs on a harder clock than rural Provence.",
    "<b>Event-time is a value system, not an absence of one.</b> <i>Haraka haraka haina "
    "baraka</i> — hurry, hurry has no blessing. In event-time logic, ending a conversation with "
    "your elder because a clock instructed you to is the rude act. What event-time optimises — "
    "presence, relationships, completion — is what clock-time cultures now pay mindfulness apps "
    "to retrieve.",
])
story += [
    Paragraph("A culture’s clock is a dialect. It says nothing about capability — but migration "
              "means being graded, permanently, in a dialect you did not grow up speaking.", pull),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · How Cultures Delay Abroad", h2),
    Paragraph(
        "Do different cultures procrastinate differently once they are living abroad? Three "
        "layers. <b>The core rate does not move:</b> put a German, a Nigerian, a Brazilian and a "
        "Korean in the same visa queue and roughly one in seven of each is a chronic "
        "procrastinator. <b>What differs is which delays are visible, and which are "
        "forgiven:</b>", body),
]
story += bullets([
    "<b>Clock-time arrivals get charged for the wrong thing too</b> — their cultures grade "
    "lateness so harshly that private procrastination hides behind immaculate punctuality. The "
    "man who has never missed a meeting has not seen a doctor in six years.",
    "<b>Event-time arrivals — many African, Latin American, South Asian and Arab backgrounds — "
    "get charged twice.</b> Their shared-clock norms read as unprofessionalism in clock-time job "
    "markets, and then the stereotype is extended, falsely, to their private reliability. The "
    "engineer twenty minutes late to the barbecue is assumed late on the project. The data says "
    "the two have nothing to do with each other.",
    "<b>East Asian arrivals carry the mirror burden</b> — a punctuality reputation so strong "
    "that their genuine procrastination (student studies find the usual 80–95%) is disbelieved, "
    "which makes it harder to seek help for.",
    "<b>And the Anglo-American host culture procrastinates identically</b> while running the "
    "world’s largest anti-procrastination industry. The people judging your time dialect are, at "
    "~14% chronic rates, delaying their own tax filings as they judge.",
])
story += [
    Paragraph(
        "<b>The third layer is the one that matters: migration itself raises everyone’s delay on "
        "high-stakes tasks.</b> Not because any culture procrastinates more, but because "
        "migration loads the tasks that matter most — immigration paperwork, credential "
        "recognition, health screening, retirement planning in a country you may not stay in — "
        "with exactly the emotional weight that produces avoidance. First, the bill.", body),
]

# ================= 07 =================
story += [
    PageBreak(),
    Paragraph("07 · The Deferral Ledger", h2),
    fig("deferral_ledger.png",
        "Fig 4 — What “later” adds up to at population scale. The naturalisation gap is the best-"
        "documented case of high-stakes deferral in migrant life."),
    Paragraph(
        "In the United States alone, <b>9.2 million lawful permanent residents are eligible for "
        "citizenship and have not applied</b> — many eligible for years. Naturalised citizens "
        "earn <b>8–11% more</b> than eligible non-applicants, vote, and hold the passport that "
        "ends the visa treadmill. Every year of delay is a year of that gap, compounding the way "
        "money compounds in our black tax ledger.", body),
    Paragraph(
        "The honest caveat, and it is a big one: the naturalisation gap is <b>not mostly "
        "procrastination</b>. The fee runs to hundreds of dollars; <b>61% of eligible immigrants "
        "never received information about how to naturalise</b>; the tests frighten people with "
        "every reason to fear official examinations. Those are structural barriers, and calling a "
        "fee a character flaw is exactly the trick this report exists to refuse. But inside those "
        "9.2 million are enormous numbers who can afford the fee, speak the language, would pass "
        "the test in their sleep — and have simply not done it. Structure explains the "
        "population; it does not always explain <i>you</i>.", body),
]
story += bullets([
    "<b>Health, deferred.</b> Trait procrastination is associated with higher rates of "
    "hypertension and cardiovascular disease even after controlling for age, education and "
    "personality — partly through stress, partly through exactly the delayed check-ups a "
    "confusing foreign health system makes easiest to defer.",
    "<b>Credentials, unconverted.</b> The nurse working as a care assistant “until I do my "
    "conversion exams”, year six. The market already discounts your record unfairly — which makes "
    "the conversion you control doubly precious, and its deferral doubly expensive.",
    "<b>Money, unplanned.</b> The pension forms unfilled because “I’m not staying here forever” — "
    "a sentence the diaspora says, on average, for a decade at a time. The panicked April tax "
    "night. The plot at home bought quickly, then the title deed unregistered for years.",
    "<b>The relationships and the returns.</b> The call home not made until the news is too big "
    "to deliver. The visit deferred until it becomes a funeral. Ask anyone who has buried a "
    "parent from abroad what “later” cost them, and the ledger stops being financial.",
])
story += [
    Paragraph("The stereotype worries about the party that starts late. The ledger shows the real "
              "losses happen in perfect silence, on time-stamped forms, with no music playing at "
              "all.", pull),
]

# ================= 08 =================
story += [
    Paragraph("08 · The Emotional Engine", h2),
    fig("mood_repair.png",
        "Fig 5 — The loop that runs the whole phenomenon. The relief is real — which is exactly "
        "why the loop holds (Sirois & Pychyl, 2013)."),
    Paragraph(
        "Why does a capable adult leave a life-changing form unopened for a year? The moral "
        "answer (weak character), the managerial answer (poor time management) and the "
        "motivational answer (not wanting it enough) all failed, because all three miss what the "
        "delay is <b>for</b>. The modern consensus: <b>procrastination is emotion regulation — "
        "short-term mood repair.</b> The task carries a bad feeling; avoiding the task removes "
        "the feeling, instantly and reliably. Procrastination is not a failure of your "
        "discipline. It is a success of your relief-seeking, billed to your future self.", body),
    Paragraph(
        "This is why the diaspora’s hardest tasks are the most avoided. Nobody procrastinates on "
        "eating jollof; people procrastinate on tasks that are boring, ambiguous — or "
        "threatening. And migration is a machine for loading threat onto paperwork. <b>The "
        "immigration form is not a form</b> — it is a document that can say no to your entire "
        "life; leaving it closed means not feeling your precarity tonight. <b>The credential exam "
        "is not an exam</b> — failing it would confirm the discount the market already applied, "
        "so the psyche protects itself by never sitting it; unattempted is undefeated. <b>The "
        "unfinished business plan is not unfinished — it is unfalsifiable</b>; the day you launch, "
        "you become someone who might fail with witnesses back home watching.", body),
    Paragraph(
        "Then the loop closes with the cruellest gear: guilt. Avoidance brings relief, relief "
        "breeds guilt, guilt makes the task feel worse, and a worse-feeling task is avoided "
        "harder. The finding that undoes it is almost embarrassing in its gentleness: students "
        "who <b>forgave themselves</b> for procrastinating on one exam procrastinated <i>less</i> "
        "on the next. Self-compassion, not self-flagellation, breaks the loop. Your grandmother’s "
        "theology had a word for this too, and it was not sloth. It was grace.", body),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("09 · What Migration Does to the Equation", h2),
    fig("tmt_migration.png",
        "Fig 6 — Temporal Motivation Theory’s terms, plus the witness term our own research adds "
        "— and what crossing a border does to each.", max_h=110 * mm),
    Paragraph(
        "Temporal Motivation Theory compresses the research into one expression: motivation = "
        "(expectancy × value) ÷ (impulsiveness × delay). You act when you believe the attempt "
        "will work, care about the payoff, can resist nearer pleasures, and the reward is close. "
        "Migration rewrites every term. <b>Expectancy falls</b> — every unexplained rejection "
        "teaches you that trying does not work here; low expectancy is not laziness, it is "
        "learned arithmetic. <b>Value blurs</b> — half the diaspora’s big tasks are borrowed: the "
        "degree the family expects, the house built for an audience; motivation sustained by "
        "other people’s goals leaks. <b>Delay stretches</b> — citizenship pays off in year six, "
        "the pension at sixty-seven, and distant rewards weigh almost nothing against tonight’s "
        "relief. <b>The future self becomes a stranger</b> — on a renewable permit, ten-year-you "
        "has no fixed country; it is very hard to do paperwork for a stranger whose city you "
        "cannot name. “I’m not staying forever” is not a plan; it is a solvent. <b>And the "
        "witnesses vanish</b> — at home your commitments had an audience with opinions; abroad, "
        "nobody sees the unopened envelope, so the deadline dies in private.", body),
    Paragraph("The confident hustler who becomes a hesitant deferrer abroad has not changed "
              "character. Every variable in their motivation equation was rewritten by the "
              "border. Variables can be rewritten back.", pull),

    Paragraph("10 · The Six Types, Diaspora Edition", h2),
]
story += bullets([
    "<b>The Perfectionist</b> cannot submit until it is unrejectable — “twice as good” was "
    "survival advice. Fix: ship at good-enough; the market rewards submitted over immaculate.",
    "<b>The Dreamer</b> lives in the someday-return, vivid enough to feel like progress. Fix: "
    "one small falsifiable step; a dream with a deadline becomes a project.",
    "<b>The Worrier</b> avoids the form because the form can say no. Fix: name the fear and "
    "price the alternative — the no is survivable; the decade of limbo is not.",
    "<b>The Crisis-Maker</b> works best at the last minute — but visa windows have no mercy for "
    "the late surge. Fix: artificial earlier deadlines with real stakes attached.",
    "<b>The Defier</b> delays as quiet rebellion against the boss, the system, or the family "
    "whose expectations wrote the to-do list. Fix: re-choose the task as yours, or honestly drop "
    "it. Resentment is not a schedule.",
    "<b>The Overdoer</b> — the diaspora’s signature type — is not avoiding work but drowning in "
    "it: two jobs, remittances, everyone’s emergencies, so their <i>own</i> file sits eternally "
    "last. Fix: black-tax boundaries. You cannot to-do-list your way out of being everyone’s "
    "infrastructure.",
])

# ================= 11 & 12 =================
story += [
    Paragraph("11 · What Actually Works", h2),
    fig("toolbox.png",
        "Fig 7 — The rebuild. Every item is boring, structural, and works better than "
        "motivation.", max_h=110 * mm),
    Paragraph(
        "The research is unanimous on what does not work: willpower, self-shaming, waiting for "
        "motivation, elaborate plans. What works attacks the equation directly. <b>Shrink the "
        "first move</b> until it is too small to dread — not “apply for citizenship” but “find my "
        "alien number”. <b>Design the environment, not the mood</b> — the form on the kitchen "
        "table gets filled; the form in the drawer does not. <b>Buy deadlines with money and "
        "appointments</b> — book the biometrics before you feel ready; paid deadlines do not "
        "negotiate. <b>Treat the feeling, not the flaw</b> — recognise the dread, allow it, "
        "investigate it, and refuse to identify with it; then forgive the years already lost. "
        "<b>And make it communal again</b> — fill the forms in company, tell one person the "
        "deadline and ask them to ask. Body-doubling, the productivity industry calls it now, "
        "selling back to us at $30 a month what the harambee committee always knew.", body),

    Paragraph("12 · The African Advantage", h2),
    Paragraph(
        "The reframe the productivity industry will never sell you: <b>the cultures labelled "
        "worst at time are sitting on the best anti-procrastination technology ever built.</b> "
        "The wedding may start two hours late — and the wedding <i>happens</i>, planned by a "
        "committee of forty, financed by contribution lists that close on time. The harambee hits "
        "its target. The chama pays out on schedule for decades. The burial society moves a body "
        "across continents in days. The market stall opens every single dawn. None of that runs "
        "on individual willpower. It runs on <b>visible stakes and present witnesses</b> — "
        "exactly the two variables migration deletes, and exactly the two the research says "
        "matter most.", body),
    Paragraph(
        "Event-time cultures are not weak at completion; they are weak at <i>solitary, invisible, "
        "clock-audited</i> completion, because they never needed it. The tasks that defeat the "
        "diaspora — forms filled alone at midnight, exams booked by no one — are tasks stripped "
        "of every mechanism our cultures built. The fix is not to become German. The fix is to "
        "<b>re-communalise your paperwork</b>: put the citizenship application on the group’s "
        "agenda the way the wedding was, and watch the same machinery ship it.", body),
    Paragraph("Your culture never failed at deadlines. It failed to anticipate a life where "
              "deadlines would arrive without people attached.", pull),
]

# ================= 13 =================
story += [
    Paragraph("13 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First: “it’s just our culture” is sometimes a launderette.</b> Event-time is a real "
        "and defensible value system — between consenting participants who share it. The diaspora "
        "event that starts three hours late in a city where guests booked babysitters and last "
        "trains is not event-time; it is a co-ordination failure wearing culture as a costume, "
        "and everyone in the room knows the difference. Respecting our own people’s time — the "
        "scarcest thing working immigrants own — is not colonial assimilation.", body),
    Paragraph(
        "<b>Second: the structural excuse and the personal excuse take in each other’s "
        "washing.</b> Fees, hostile bureaucracies and missing information explain much of the "
        "deferral ledger, and blaming individuals for structural barriers is the oldest trick in "
        "the anti-immigrant book. But the reverse trick is ours: citing the structure while the "
        "barrier in your specific case is an envelope and an evening. The honest audit takes ten "
        "minutes: for each deferred task, write what is actually blocking it. Where the answer is "
        "money or law, organise. Where the answer is dread, Section 11 is waiting.", body),
    Paragraph(
        "<b>Third: do not swap the shame of delay for the shame of rest.</b> The same industry "
        "that pathologised “African time” also pathologised the nap. Overcorrect into the "
        "productivity cult — every hour optimised, worth measured in output — and you will have "
        "imported the anxiety with none of the pension; the fastest countries in the pace-of-life "
        "study bought their speed with their hearts. The goal is not that you never delay. It is "
        "that your delays become <b>chosen</b> — the deliberate, unhurried presence your culture "
        "perfected — while the envelope that decides your future gets opened this week, with a "
        "cousin on the phone and the fee already paid.", body),
]

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("14 · Method &amp; Limits", h2),
    Paragraph("This report combines cross-cultural psychology, procrastination research and "
              "migration data, as at 27 August 2026.", body),
]
story += bullets([
    "<b>Procrastination is measured by self-report scales</b>, and prevalence figures move with "
    "the scale and sample. The 95% / 80–95% / 15–20% bands are from Steel’s 2007 meta-analysis; "
    "the ~14% cross-national figure is Ferrari et al.’s 2007 six-nation study. Those six nations "
    "did not include an African country — the African evidence is from separate campus studies "
    "(Ethiopia, Tunisia, Sudan, Nigeria) using comparable instruments: convergent, not identical, "
    "methodology.",
    "<b>The lateness/procrastination distinction is analytically clean but empirically "
    "entangled:</b> both are self-reported, and a culture’s norms shape what respondents count as "
    "“delay” at all. We rest the argument on the cross-national flatness of chronic rates, which "
    "survives this caveat better than any single percentage.",
    "<b>The pace-of-life data is from 1999</b> and measured cities, not nations. We use it for "
    "its correlational structure — pace tracks wealth and climate — not for current rankings.",
    "<b>The naturalisation numbers are structural first.</b> The 9.2 million and the 61% "
    "information gap are documented by the Niskanen Center and the New Americans Campaign; the "
    "8–11% earnings differential is associational and partly selection. We explicitly do not "
    "claim the gap is procrastination — we claim deferral has measurable costs and some unknown "
    "fraction of it is voluntary delay. No study has measured procrastination specifically in "
    "African diaspora populations; that absence is itself a finding.",
    "<b>The health association</b> (procrastination with hypertension and cardiovascular "
    "disease) is cross-sectional; causality is plausible but not proven by that design.",
    "<b>Sections 06, 09 and 12 are interpretive</b> — our syntheses of established mechanisms "
    "applied to diaspora life, labelled as argument rather than measurement.",
    "<b>The framework reached us partly through a secondary source</b> — Mark Manson’s "
    "<i>Procrastination Guide</i>, shared by a member of this network. We went to the primary "
    "papers — Steel (2007), Sirois &amp; Pychyl (2013), Ferrari et al. (2007), Sapadin (1996), "
    "Levine &amp; Norenzayan (1999) — and cite those; the guide is credited as the pointer, not "
    "as evidence.",
    "<b>Nothing here is clinical advice.</b> Chronic, distressing procrastination travels with "
    "ADHD, anxiety and depression often enough that a stuck year deserves a professional "
    "conversation, not another productivity system.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Steel (2007), The Nature of Procrastination, Psychological Bulletin; Ferrari, "
        "Díaz-Morales, O’Callaghan et al. (2007), Journal of Cross-Cultural Psychology; Sirois "
        "&amp; Pychyl (2013) on mood repair; Sirois (2015) on procrastination and "
        "hypertension/CVD; Levine &amp; Norenzayan (1999), The Pace of Life in 31 Countries; van "
        "Eerde &amp; Azar (2020) on lateness norms; Ethiopian, Tunisian and Sudanese campus "
        "studies; Niskanen Center and New Americans Campaign on naturalisation; Sapadin (1996); "
        "Steel &amp; König’s Temporal Motivation Theory; African Studies scholarship on “African "
        "time”. Located partly via Mark Manson’s Procrastination Guide. Full inline links in the "
        "web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/cost-of-later-2026<br/>"
        "Companion reports: The Sense of Time · The Most Optimistic People on Earth · The Black "
        "Tax Ledger · What Will People Say?<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
