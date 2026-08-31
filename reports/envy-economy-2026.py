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
IMG = os.path.join(HERE, "envy-economy-2026", "img")
OUT = os.path.join(HERE, "envy-economy-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Envy Economy · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 31 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Envy Economy (2026)",
                      author="Africa Global Forum",
                      subject="Social comparison, status anxiety, and the two mirrors of African life abroad")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Envy", h1),
    Paragraph("economy.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Every African abroad is measured in two mirrors at once: rich in the one facing home, "
        "behind in the one facing the host country — on the same salary, on the same day. This "
        "report is about the machinery inside that double reflection: the brain that prices "
        "everything relatively, the half of humanity that would take half the salary to come "
        "first, the neighbour's win that sends you to the moneylender — and what the science says "
        "about living between mirrors without being broken by either.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("~50%", big_num), Paragraph("+2.4%", big_num),
    Paragraph("1 in 3", big_num), Paragraph("84%", big_num),
], [
    Paragraph("would take HALF the salary<br/>to out-earn everyone<br/>around them", big_lbl),
    Paragraph("rise in neighbours'<br/>bankruptcies per $1,000 a<br/>nearby lottery winner takes", big_lbl),
    Paragraph("feel worse — envious,<br/>resentful — after browsing<br/>social media", big_lbl),
    Paragraph("of surveyed migrants<br/>overestimated the wages<br/>waiting abroad", big_lbl),
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
    fig("two_mirrors.png",
        "Fig 1 — The double reference group. Psychology mostly studies people with one comparison "
        "audience; the migrant carries two, permanently, facing opposite directions.",
        max_h=92 * mm),
    Paragraph("Published August 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/envy-economy-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "A member of this network told us a story that fits in one sentence: on the same Sunday, "
        "her aunt in Kisumu asked when she would “remember those of us you left behind”, and her "
        "Canadian colleague asked, sympathetically, whether she was “still renting”. Two mirrors, "
        "one woman, one salary. This report is about the machinery behind that Sunday.", body),
]
story += bullets([
    "<b>Comparison is not a character flaw; it is the brain's pricing system.</b> fMRI studies "
    "show the reward circuitry responds to <i>relative</i> outcomes — identical money literally "
    "feels worse when a peer got more. In the classic Harvard survey, about half of respondents "
    "preferred $50,000 where others earn $25,000 over $100,000 where others earn $200,000 — "
    "<b>half the real income, for the relative win</b>.",
    "<b>The pain is engineered to be strongest exactly where the diaspora lives.</b> Tesser's "
    "research shows comparison burns in proportion to closeness × relevance: the age-mate with "
    "your same start hurts more than any billionaire. The diaspora WhatsApp group is a machine "
    "for delivering close, relevant comparisons across nine time zones, daily.",
    "<b>Migration doubles the reference groups.</b> The migrant has two audiences: the home "
    "mirror, where your converted salary makes you rich and envied, and the host mirror, where "
    "locals your age started compounding at birth. You are simultaneously ahead and behind — and "
    "both mirrors are calibrated against fictions: 84% of surveyed migrants overestimated the "
    "wages waiting abroad before they left.",
    "<b>Envy has an invoice.</b> For every $1,000 a lottery winner takes home, their neighbours' "
    "bankruptcy filings rise 2.4% — comparison spends borrowed money. The diaspora edition: the "
    "December performance, the shipped car, the wedding that outruns income, the “rich relative” "
    "myth that inflates the black tax.",
    "<b>The fix is not to stop comparing — the instinct is older than language.</b> It is to "
    "compare wisely: against yourself at arrival, against process rather than outcomes, with "
    "curated mirrors — and with the occasional honest post, because visible struggle keeps your "
    "success attainable, and attainable success keeps your community's envy benign.",
])
story += [
    Paragraph("The envy economy has no currency of its own. It is denominated entirely in other "
              "people's highlight reels — and everyone in it is both customer and vendor.", pull),
]

# ================= 02 & 03 =================
story += [
    PageBreak(),
    Paragraph("02 · The Two Mirrors", h2),
    Paragraph(
        "Reference-group research has shown since the 1940s that wellbeing tracks the group you "
        "compare against far more than your absolute condition. Migration performs a strange "
        "surgery on that machinery: it does not replace your reference group — <b>it adds a "
        "second one and keeps both switched on.</b> Face the home mirror and you are wealthy: "
        "your salary converts into school fees for half a compound, your winter coat photographs "
        "like success. Face the host mirror and the same life reads as behind: renting at an age "
        "your colleagues bought, starting a pension in your thirties, explaining your credentials "
        "to people younger than your discounted CV. Neither mirror is lying, exactly — each "
        "measures a different economy — but your nervous system does not apply purchasing-power "
        "adjustments to feelings. It receives both verdicts at once, forever: <i>you are "
        "envied</i>, and <i>you are behind</i>.", body),
    Paragraph(
        "And there is a third pane most people miss: the <b>diaspora mirror</b> — other Africans "
        "abroad, the truest comparison group of all, same start, same visa queues, same "
        "remittance load. Which is exactly why it is the one that burns hottest.", body),

    Paragraph("03 · The Oldest Instrument", h2),
    Paragraph(
        "The measuring instinct did not arrive with smartphones. Festinger's 1954 social "
        "comparison theory formalised it: humans have a basic drive to evaluate themselves, and "
        "where objective standards are missing we measure against other people. The equipment is "
        "far older than the theory — status-tracking is primate infrastructure, and Gilbert's "
        "social-rank research argues much of our emotional palette is status machinery: <b>pride "
        "signals a rise, shame signals a fall, and envy is the alarm that someone has something "
        "your survival systems have decided matters.</b> The system was tuned for villages of "
        "roughly 150 people, where every comparison target was a real, whole, visible life.", body),
    Paragraph(
        "Africa's cultures have always known this machinery intimately. A continent that "
        "developed the evil eye, the praise singer, the age-grade system that compares only peers "
        "initiated together, and a thousand proverbs about the neighbour's harvest did not need "
        "Festinger. What tradition understood is that comparison is a communal force requiring "
        "communal management.", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · The Relative Brain", h2),
    fig("relative_brain.png",
        "Fig 2 — The neuroscience: reward is relative, envy is processed like pain, and the "
        "envied person's stumble is processed like winning."),
    Paragraph(
        "In Fliessbach's fMRI experiment, participants received identical money for identical "
        "work — and the ventral striatum, the reward centre, <b>responded more when others got "
        "less and less when others got more</b>. Takahashi's team completed the picture: envy "
        "activates the anterior cingulate cortex, a region that processes physical pain, while "
        "news of the envied person's misfortune lights up the reward system. Schadenfreude is, "
        "neurally, a payday. When your first reaction to an age-mate's setback shames you, it "
        "helps to know the reaction is circuitry, not character — and that what you do "
        "<i>next</i> is character.", body),
    fig("half_salary.png",
        "Fig 3 — Solnick & Hemenway (1998): half the real income, for the relative win.",
        max_h=70 * mm),
    Paragraph(
        "How much does relative position weigh against real money? In the Harvard survey, "
        "<b>about half of respondents chose $50,000 where others earn $25,000 over $100,000 "
        "where others earn $200,000</b> — surrendering half their purchasing power to stand "
        "above the crowd. Anyone who has watched a diaspora wedding budget triple to impress a "
        "WhatsApp group has seen the finding replicate in the field. The stakes are not only "
        "financial: Sapolsky's primate work shows chronic one-down status tracks with cortisol, "
        "inflammation and illness. Feeling permanently behind is physiologically expensive — a "
        "tax the host mirror levies daily.", body),
]

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("05 · The Cousin Principle", h2),
    fig("cousin_principle.png",
        "Fig 4 — Tesser's self-evaluation maintenance model, drawn as a map of who can hurt "
        "you.", max_h=105 * mm),
    Paragraph(
        "Why does a stranger's Lamborghini amuse you while your age-mate's modest house keeps you "
        "up at night? Tesser's answer is an equation: <b>comparison pain scales with closeness × "
        "relevance.</b> A distant person in a different life is entertainment. A close person in "
        "a different lane is pride — the cousin who sings gets your genuine applause. But a close "
        "person succeeding in <i>your</i> domain — same school, same start, same definition of "
        "success — is a direct audit of your self-concept. That is the furnace.", body),
    Paragraph(
        "African social life runs unusually hot on this equation. The <b>age-mate</b> is an "
        "institution: initiated with you, graduated with you, bride price and job title known to "
        "your mother to the shilling. The extended family is a permanently close comparison "
        "pool; the “what will people say” audit keeps every domain relevant. And migration feeds "
        "the equation: the diaspora WhatsApp group curates your closest, most relevant "
        "comparisons and delivers their promotions, keys and gender reveals to your pocket at "
        "breakfast. Nobody lies awake over a billionaire. They lie awake over the age-mate from "
        "secondary school who arrived the same year — and just posted the house.", body),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · The Two Envies", h2),
    fig("two_envies.png",
        "Fig 5 — Van de Ven et al. (2009): same trigger, two roads, and the fork is perceived "
        "attainability."),
    Paragraph(
        "Envy is not one emotion. <b>Malicious envy</b> is hostile and wants to pull the other "
        "down; <b>benign envy</b> is the admiring ache that makes you work harder. The fork is "
        "<b>perceived attainability</b>: success that looks earned and reachable becomes fuel — "
        "“if they can, so can I” is the sentence that filled every visa queue on the continent — "
        "while success that looks undeserved or impossible turns to poison: gossip, “must be "
        "nice”, and the quiet hope of a stumble.", body),
    Paragraph(
        "African culture carries a rich folk theory of the malicious kind — the evil eye, the "
        "“village people” jokes that are only half jokes, the real fear that visible success "
        "invites attack. Strip the metaphysics and the sociology underneath is sound: "
        "<b>communities correctly understood that unexplained, unshared success destabilises "
        "them</b>, and built rituals — redistribution, feasts, deliberate modesty — to manage "
        "it. The attainability fork also hands you a practical lever: post only outcomes — the "
        "car, the keys — and your success looks like magic: unattainable, malicious-envy bait. "
        "Show the process — the night shifts, the failed applications, the years — and the same "
        "success becomes a roadmap.", body),
]

# ================= 07 =================
story += [
    PageBreak(),
    Paragraph("07 · The Feed That Never Sleeps", h2),
    fig("feed.png",
        "Fig 6 — The scroll, quantified. Krasnova et al. (2013) on Facebook envy; Dunbar on what "
        "the hardware was built for.", max_h=100 * mm),
    Paragraph(
        "Connect the ancient machinery to a global feed. In Krasnova's studies of Facebook "
        "users, <b>one in three reported feeling worse — envious, resentful, lonelier — after "
        "browsing</b>, with passive scrolling the trigger and <b>travel photos the number-one "
        "envy stimulus</b>. Lurking does the damage, not posting. A brain built to compare "
        "against ~150 known, whole lives now scans thousands of strangers' curated peaks — and "
        "concludes, as Chou and Edge showed, that everyone else is happier.", body),
    Paragraph(
        "The diaspora scroll is this problem squared, because each mirror has a feed. One "
        "thumb-flick serves a home-friend's new build (“they're leveling up while I pay rent "
        "abroad”), the next a local colleague's lake house (“I will never catch up here”), the "
        "next a fellow diasporan's citizenship post (“same year as me — what have I been "
        "doing?”). Three upward comparisons, three reference groups, ninety seconds — before "
        "breakfast. And each is a fiction: the build has a loan on it, the lake house an "
        "inheritance behind it, the passport five years of paperwork cropped out. The feed is "
        "not a window. It is a market stall where every vendor displays only the ripest fruit — "
        "including yours.", body),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · The Price of Keeping Up", h2),
    fig("keeping_up.png",
        "Fig 7 — The envy ledger. Comparison borrows, spends, and bills you later.",
        max_h=100 * mm),
    Paragraph(
        "If envy were only a feeling, this would be a wellness essay. It is a balance-sheet "
        "item. Using lottery wins as random shocks to neighbourhood status, Agarwal, Mikhed and "
        "Scholnick found that <b>every $1,000 a winner took home raised bankruptcy filings among "
        "close neighbours by 2.4%</b> — strongest in low-income, high-inequality areas, with the "
        "mechanism visible in the bankrupts' asset lists: conspicuous goods, bought on debt, to "
        "keep up. One person's visible rise, other people's borrowed spending.", body),
    Paragraph(
        "The diaspora runs its own editions yearly, and this library has priced several: the "
        "wedding arms race, where celebrations outrun annual incomes because the real audience "
        "is the comparison pool; the December homecoming performance — the shipped car, the "
        "rounds for the whole bar, two weeks of display costing three months of margin; the plot "
        "bought because an age-mate bought one, unseen and gone. None of this is stupidity. When "
        "half of humanity will pay half its income for relative position, a visible-status "
        "purchase is not irrational — it is just expensive. The colder question: <b>who exactly "
        "is the audience for this purchase, and what do they contribute to your actual life?</b>",
        body),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("09 · The Myth of Abroad", h2),
    Paragraph(
        "Now turn the mirror around, because the diaspora is not only envy's victim. To the home "
        "audience, <b>you are the lottery winner next door</b> — the visible rise against which "
        "cousins measure their own stalled queues. That mirror too is calibrated against a "
        "fiction: in one study of migrants to Italy, <b>84% had overestimated the wages waiting "
        "for them</b>; migration-expectations research finds systematic over-optimism about life "
        "abroad, maintained by a century of one-directional evidence — successful migrants "
        "photographed, failed migrations unphotographed.", body),
    Paragraph(
        "And every African abroad is now a maintenance worker for that myth. You cannot post the "
        "warehouse shift, the racist landlord, the fourth rejection — partly pride, partly "
        "kindness, partly the shame audit waiting for any admission of struggle. So you post the "
        "graduation, the snow, the skyline. The home audience takes the photos as data and "
        "adjusts two behaviours: the remittance expectations (a rich relative can obviously "
        "afford more), and the migration queue itself, restocked by your highlight reel. The "
        "performance is not free for you either. The researchers' term is information asymmetry; "
        "the lived version is loneliness — being envied for a life you cannot admit is hard, by "
        "the only people who truly know you. The envy economy's cruellest trade: <b>both mirrors "
        "polishing their fictions at each other, both sides paying interest on images.</b>", body),

    Paragraph("10 · The Double Bill", h2),
]
story += bullets([
    "<b>The upward bill (host mirror): chronic behindness.</b> Not episodic envy but a baseline — "
    "daily structural comparison against people whose compounding started at birth, in a country "
    "that also discounts your name and credentials. Sapolsky's one-down physiology is the health "
    "footnote; relative-deprivation research shows the feeling operates independently of your "
    "actual standard of living.",
    "<b>The downward bill (home mirror): being envied.</b> It sounds like a compliment and "
    "functions like a tax: inflated remittance expectations, requests priced off your imagined "
    "salary, the impossibility of saying “I can't afford it” without being disbelieved — plus "
    "friendships that curdle into transactions, the fear of the eye that hides wins even from "
    "family, and the guilt of having “made it” into a life that does not feel made.",
    "<b>The lateral bill (diaspora mirror): the furnace.</b> The comparison pool that best "
    "understands your life is best equipped to wound you with theirs — and diaspora communities "
    "can develop a real malicious-envy culture: success policed with “who does she think she "
    "is”, the business undermined from inside, the crab bucket that greets every climber.",
    "<b>The compound interest: every bill feeds the others.</b> Feeling behind abroad makes the "
    "home performance more necessary; the performance inflates the envy and the expectations; "
    "the expectations deepen the squeeze that keeps you feeling behind. The mirrors are not two "
    "problems. They are one loop.",
])

# ================= 11 =================
story += [
    PageBreak(),
    Paragraph("11 · What the Traditions Knew", h2),
]
story += bullets([
    "<b>Buddhism trained the counter-emotion.</b> <i>Mudita</i> — sympathetic joy in another's "
    "success — is the direct antidote to envy, and it is trainable: compassion-training studies "
    "show a few weeks of practice increases positive affect and reduces hostility. “I'm glad "
    "it's you” is a skill, not a temperament.",
    "<b>Aristotle drew the fork first.</b> His Rhetoric separates <i>phthonos</i> — envy that "
    "wants to strip the other — from <i>zelos</i>, emulation: the moral discomfort that spurs "
    "you to rise. Twenty-four centuries before the psychologists, the two envies were on the "
    "page.",
    "<b>The Stoics changed the measuring stick.</b> Epictetus called envy “a disease of the "
    "soul”; the Stoic move survives intact — measure yourself against your values, not the "
    "room. “Am I living according to what I control?” converts comparison from a status game "
    "into an integrity audit.",
    "<b>And African traditions engineered the environment.</b> Ubuntu makes the neighbour's "
    "success partly yours by definition; the harambee converts one family's rise into communal "
    "stakeholding — hard to maliciously envy a graduation you helped fund; age-grade systems "
    "restricted comparison to true peers; and the deliberate modesty norms around wealth were "
    "envy management, not superstition. The village knew what the feed forgot: <b>comparison is "
    "safe only inside relationships thick enough to hold it.</b>",
])

# ================= 12 =================
story += [
    PageBreak(),
    Paragraph("12 · Comparing Wisely", h2),
    fig("compare_wisely.png",
        "Fig 8 — The rebuild. The goal is not to stop comparing — it is to choose the mirrors "
        "and the questions.", max_h=110 * mm),
    Paragraph(
        "Suppressing comparison fails; the instinct is older than language. What works is "
        "redirecting it. <b>Compare to yourself at arrival</b> — the only benchmark that prices "
        "your actual handicaps; against arrival-you, the language learned, the system decoded, "
        "the people carried, the growth is undeniable. <b>Curate the mirrors</b> — passive "
        "scrolling is the documented damage-dealer, so unfollow what reliably wounds, keep the "
        "accounts that show process, and convert lurking into contact: the age-mate's house "
        "feels different once you have heard about the loan. <b>Ask the process question</b> — "
        "not “why not me?” but “what did they do that I can try?”; if the answer is a method, "
        "copy it; if the answer is an inheritance, the comparison was never valid. <b>Practise "
        "mudita — and post honestly sometimes</b>: congratulate fully, first, out loud; and show "
        "your own struggle occasionally, because it keeps your success attainable and someone in "
        "your mirror is waiting for exactly that permission. <b>And read your envy as a "
        "compass</b> — the sting marks what you actually value; sometimes it is a goal to chase, "
        "sometimes a value you have been outsourcing to other people's scoreboards.", body),
]

# ================= 13 =================
story += [
    PageBreak(),
    Paragraph("13 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First: you are not only the customer in the envy economy — you are also a "
        "vendor.</b> The same person wounded by the feed curates one. Your December photos, your "
        "graduation post, your careful silence about the warehouse years — someone in Kitale "
        "measures their life against that highlight reel the way you measure yours against a "
        "colleague's lake house. This is not an accusation; it is bookkeeping. The fastest way "
        "to soften the economy is for its vendors to start labelling their goods honestly.", body),
    Paragraph(
        "<b>Second: some of what the diaspora calls envy is actually grief, and some of what it "
        "calls hustle is actually envy.</b> The pang at the friend who stayed home and thrived "
        "is often not wanting their life — it is mourning the version of yours that stayed. "
        "Naming it grief changes what heals it. And an ambition that only activates when an "
        "age-mate posts — the degree started after their graduation, the business launched after "
        "their launch — is not a vision, it is a reaction. A life steered by other people's "
        "milestones arrives at other people's destinations.", body),
    Paragraph(
        "<b>Third: the community's malicious envy is real, and pretending otherwise protects "
        "it.</b> The crab bucket is not a stereotype — it is what the attainability fork "
        "predicts when success looks unattainable and unshared inside a tight group under "
        "scarcity. The diaspora business quietly boycotted from within, the achiever cut down "
        "with “she has forgotten herself”, the return home downplayed to avoid the eye — these "
        "are our own line items, and they answer to our own tools: make success legible (show "
        "process), make it communal (stakeholders do not sabotage), and call the behaviour what "
        "it is. A community that can celebrate its winners without auditing them — and whose "
        "winners can be honest without performing — has exited the worst of the envy economy, "
        "whatever the feeds are doing.", body),
]

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("14 · Method &amp; Limits", h2),
    Paragraph("This report combines social-comparison research, neuroscience, behavioural "
              "economics and migration studies, as at 31 August 2026.", body),
]
story += bullets([
    "<b>The core psychology is the replicated canon</b> — Festinger (1954), Tesser's "
    "self-evaluation maintenance model, Van de Ven's benign/malicious distinction, and the fMRI "
    "findings on relative reward and envy/schadenfreude. Neuroimaging samples are small and "
    "reverse inference has limits; we use them as converging evidence, not proof by brain scan.",
    "<b>The Solnick &amp; Hemenway survey</b> polled 257 Harvard-affiliated respondents in 1995 "
    "— stated preferences, not behaviour. It sits, however, on a large literature on positional "
    "concerns pointing the same way.",
    "<b>The lottery-bankruptcy result</b> is a quasi-experiment from one Canadian province; the "
    "2.4%-per-$1,000 figure is an estimate, not a universal constant. We cite it for the "
    "mechanism — visible peer income causing debt-financed status spending — which the authors "
    "document directly in balance-sheet data.",
    "<b>The Facebook findings (2012–13) predate today's platforms;</b> TikTok and Instagram are "
    "structurally more comparison-dense, which likely makes those estimates conservative, but we "
    "cannot show that directly.",
    "<b>The 84% wage-overestimate figure</b> is from one 2015 study of migrants to Italy; the "
    "direction is well replicated across migration-expectations research, the exact percentage "
    "is not.",
    "<b>No study has measured the double-reference-group effect in African diaspora populations "
    "directly.</b> The two-mirrors framework is our synthesis of established mechanisms applied "
    "to diaspora life — labelled as argument, not measurement. The same holds for the reading of "
    "African institutions as envy management: plausible, ethnographically grounded, not "
    "experimentally tested.",
    "<b>The framework reached us partly through a secondary source</b> — Mark Manson's <i>Social "
    "Comparison Guide</i>, shared by a member of this network. We went to the primary papers — "
    "Festinger, Tesser, Van de Ven, Fliessbach, Takahashi, Krasnova — and cite those; the guide "
    "is credited as the pointer, not as evidence.",
    "<b>Nothing here is clinical advice.</b> Comparison that has curdled into persistent "
    "depression, anxiety or rumination deserves a professional conversation, not a better feed.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Festinger (1954), A Theory of Social Comparison Processes; Tesser (1988) on "
        "self-evaluation maintenance; Van de Ven, Zeelenberg &amp; Pieters (2009) on benign and "
        "malicious envy; Fliessbach et al. (2007) and Takahashi et al. (2009) in Science; "
        "Solnick &amp; Hemenway (1998) on positional concerns; Agarwal, Mikhed &amp; Scholnick "
        "(2020), Review of Financial Studies, on lottery wins and neighbouring bankruptcies; "
        "Krasnova et al. (2013) on Facebook envy; Chou &amp; Edge (2012); Migration Policy "
        "Centre research on migrants' wage expectations; Klimecki et al. (2013) on compassion "
        "training; Sapolsky (2005) on hierarchy and health; Lockwood &amp; Kunda (1997) on role "
        "models. Located partly via Mark Manson's Social Comparison Guide. Full inline links in "
        "the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/envy-economy-2026<br/>"
        "Companion reports: What Will People Say? · The Black Tax Ledger · The Price of “I Do” · "
        "The Cost of Later<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
