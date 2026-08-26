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
IMG = os.path.join(HERE, "african-confidence-2026", "img")
OUT = os.path.join(HERE, "african-confidence-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "African Confidence · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 24 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Most Optimistic People on Earth (2026)",
                      author="Africa Global Forum",
                      subject="Confidence in African culture, what migration does to it, and how to rebuild it")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Most Optimistic", h1),
    Paragraph("people on earth.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "By the numbers, Africans are the most confident people alive: three of the five most "
        "optimistic countries on earth, and the highest entrepreneurial self-belief of any region "
        "ever measured. This report asks what that confidence actually is, why the same person so "
        "often goes quiet abroad — and what half a century of psychology says about getting it "
        "back.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("3 of 5", big_num), Paragraph("76%", big_num),
    Paragraph("0", big_num), Paragraph("4", big_num),
], [
    Paragraph("of the world's most optimistic<br/>countries are African", big_lbl),
    Paragraph("of sub-Saharan adults believe<br/>they can start a business —<br/>the highest region measured", big_lbl),
    Paragraph("what “believe in yourself”<br/>builds without evidence", big_lbl),
    Paragraph("sources of real confidence,<br/>ranked — the industry sells<br/>the list upside down", big_lbl),
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
    fig("optimism.png",
        "Fig 1 — Share expecting the coming year to be better (Gallup International). Three of the "
        "five most optimistic countries on earth are African; Western Europe sits far below.",
        max_h=95 * mm),
    Paragraph("Published August 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/african-confidence-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Everyone in this network has seen both halves of the puzzle. The uncle in Kumasi who has "
        "failed at four businesses and describes the fifth with total certainty. And the brilliant "
        "cousin in Toronto — top of her class at home — who now rewrites one email for forty "
        "minutes. Same family, same culture, opposite confidence. This report is about why.", body),
]
story += bullets([
    "<b>African confidence is real and measured.</b> <b>Nigeria (80%), Sierra Leone and Côte "
    "d'Ivoire</b> sit among the five most optimistic countries on earth, while Western Europe sits "
    "near the bottom. And <b>76% of sub-Saharan adults believe they have the skills to start a "
    "business</b> — the highest of any region GEM has measured.",
    "<b>The paradox is the direction.</b> The world's highest confidence sits in some of its "
    "hardest circumstances — while <b>East Asian students top every global test with below-average "
    "stated self-belief</b>. Whatever confidence is, it is not a readout of conditions.",
    "<b>Psychology splits it into two things.</b> <i>Optimism</i> is a feeling about the future in "
    "general. <i>Self-efficacy</i> — Bandura's term — is an evidence-based judgement that you can "
    "do a specific thing. The African data is strongest on the first. The second is built one way "
    "only: by doing.",
    "<b>On the second measure, Africa has a hidden advantage.</b> The informal economy is a machine "
    "for <i>mastery experience</i> — nobody at the market stall waits until they feel ready. The "
    "action-before-readiness loop the confidence literature prescribes is the African street's "
    "default setting.",
    "<b>Migration dismantles it — structurally, not psychologically.</b> Self-efficacy is "
    "domain-specific and evidence-based; migration changes the domain and voids the evidence. Add "
    "the foreign-experience discount, the silent name-based rejections and stereotype threat, and "
    "the confident arrival's quiet second year is not a personality change. It is a ledger change.",
    "<b>What rebuilds it is boring and specific:</b> small mastery wins at the edge of ability, "
    "models who genuinely resemble you, values-affirmation before high-stakes moments — and almost "
    "never the imported “believe in yourself” ritual, which the evidence has been unkind to for "
    "seventy years.",
])
story += [
    Paragraph("Africa did not learn confidence from a book, and the diaspora will not get it back "
              "from one. It was built by acting before feeling ready — and that is exactly how it "
              "is rebuilt, anywhere.", pull),
]

# ================= 02 =================
story += [
    PageBreak(),
    Paragraph("02 · The Measured Facts", h2),
    Paragraph(
        "Year after year, the global optimism surveys find <b>hope concentrated in Africa, South "
        "Asia and Latin America, and anxiety concentrated in the rich West</b>. In the latest "
        "Gallup International round, <b>Nigeria (80% expecting a better year), Sierra Leone (77%) "
        "and Côte d'Ivoire</b> sit in the world's top five; much of Europe sits at the bottom. Fig "
        "1 on the cover has the table.", body),
    fig("gem.png",
        "Fig 2 — GEM's sub-Saharan Africa regional survey. South Africa is the striking outlier "
        "within the region, at roughly half the regional rate."),
    Paragraph(
        "The second measure is closer to this report's subject, because it is not about the world — "
        "it is about the self. Asked whether they personally have <i>the skills and knowledge to "
        "start a business</i>, <b>about 76% of sub-Saharan adults say yes</b> — the highest "
        "regional figure in the Global Entrepreneurship Monitor's data. The region with the least "
        "capital and the hardest operating conditions contains the people most convinced they can "
        "build something.", body),

    Paragraph("03 · Two Different Things", h2),
    fig("two_things.png",
        "Fig 3 — The distinction the whole report turns on, from Bandura's 1977 self-efficacy "
        "theory."),
    Paragraph(
        "In 1977, Albert Bandura drew the line the confidence conversation still ignores. What "
        "predicts whether a person attempts a difficult task and persists is <b>not how they feel "
        "about themselves in general</b> — it is whether they believe, <i>based on real "
        "evidence</i>, that they can execute the specific behaviours the situation demands. "
        "Self-efficacy is a judgement, not a feeling; it is domain-specific; and it is calibrated "
        "to what you have actually done, which is why it cannot be chanted into existence.", body),
    Paragraph(
        "Apply the split to the two charts above. The optimism surveys measure the general feeling "
        "— Africa leads the world. The GEM question sits closer to efficacy — Africa leads there "
        "too, but self-assessed. The interesting question is which kind survives migration. The "
        "answers are different, and the difference is the whole story.", body),
]

# ================= 04 =================
story += [
    Paragraph("04 · The Fallacy Africa Never Needed", h2),
    Paragraph(
        "The modern self-help industry descends substantially from one anxious 1950s preacher, "
        "Norman Vincent Peale, whose method compresses to a single instruction: <b>generate the "
        "feeling of confidence first, then act.</b> The research verdict, accumulated over "
        "decades, is bruising.", body),
]
story += bullets([
    "<b>Affirmations can backfire for the people who need them most.</b> In a widely cited 2009 "
    "study, people with low self-esteem who repeated “I am a lovable person” felt <i>worse</i>. (A "
    "2020 replication with larger samples found no effect either way — we report both — but the "
    "underlying mechanisms are robust.)",
    "<b>Fantasy visualisation drains motivation.</b> Oettingen's three decades of work show that "
    "vividly imagining the achieved goal satisfies the motivation system prematurely. Positive "
    "<i>expectations</i> grounded in past behaviour predict success; positive <i>fantasies</i> "
    "predict less effort.",
    "<b>The causation runs backwards.</b> High performers do not perform because they feel calm; "
    "they feel calm because they have performed. <b>Competence is the engine. Confidence is the "
    "readout.</b>",
])
story += [
    Paragraph("Most of Africa never adopted the Peale model — because most of Africa never had the "
              "option of waiting to feel ready.", pull),

    Paragraph("05 · The Action-First Continent", h2),
    fig("action_loop.png",
        "Fig 4 — The action-first loop the confidence research prescribes — and the informal "
        "economy runs by default."),
    Paragraph(
        "<b>The informal economy — the majority employer across most of the continent — is "
        "structurally incapable of the Peale model.</b> Nobody at Balogun market conducts a "
        "visualisation exercise before opening the stall. Necessity runs the loop daily: act with "
        "no cushion, survive, adjust, act again. Failure is frequent, public, and <i>ordinary</i> — "
        "which drains it of the paralysing weight it carries in salaried cultures.", body),
    Paragraph(
        "This reframes the GEM number. When 76% of sub-Saharan adults say they can start a "
        "business, a large part is <b>accurate self-report from people who have already run the "
        "loop</b>: traded, hustled, recovered, improvised. Their efficacy has an evidence base — "
        "simply one that formal institutions do not recognise. Two more African confidence "
        "structures deserve naming: <b>early responsibility</b> (the child sent to the market at "
        "eight is accumulating mastery experiences) and <b>communal witness</b> (your record is "
        "public, which converts personal history into socially confirmed evidence). Both are "
        "efficacy machines. Neither travels well.", body),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · The Immune System", h2),
    Paragraph(
        "Much of the optimism data is, by any calibrated standard, unrealistic. Is that a flaw? In "
        "a landmark 1988 review, Taylor and Brown showed that <b>mentally healthy adults "
        "systematically overestimate themselves</b> — while it is the mildly depressed who see "
        "themselves most accurately. These “positive illusions” function as a <b>psychological "
        "immune system</b>: a background process that softens reality enough to keep people "
        "functional and taking daily risks.", body),
    Paragraph(
        "Read the African data through that lens and it inverts the condescending interpretation. "
        "Unrealistic optimism under hard conditions is not naivety. It is <b>the immune system "
        "working at scale</b> — the evolved psychological infrastructure of populations that kept "
        "functioning through currency collapses, coups and droughts that would flatten a calibrated "
        "pessimist. Faith belongs here too: the world's most religious continent runs a daily "
        "discipline of hope, communal reinforcement and reinterpretation of setbacks that maps "
        "directly onto this machinery.", body),
    Paragraph(
        "One caution, and it matters: <b>the functional dose of self-delusion is greater than zero, "
        "but small</b> — and it works only when stacked on real evidence. Optimism riding on a "
        "record is fuel. Optimism <i>instead of</i> a record is the fifth business plan that "
        "ignores why the first four died. Our investment research is, among other things, a "
        "catalogue of the immune system overdosing.", body),

    Paragraph("07 · The Outliers", h2),
    fig("dialects.png",
        "Fig 5 — Confidence as dialect. Stated self-belief varies by culture far more than "
        "capability does."),
    Paragraph(
        "<b>East Asia is the mirror image of Africa.</b> Students in Japan, Korea and Shanghai top "
        "every international assessment — while reporting <i>below-average</i> confidence, and "
        "inside the highest-performing systems the within-country correlation between stated "
        "confidence and scores runs negative. The world's least confident-sounding students are "
        "its most capable, exactly as the world's most confident-sounding region is its least "
        "capitalised. <b>The Nordics suppress it</b> (Jante norms); <b>the United States "
        "overstates it</b> (the culture that invented Peale also produces the above-average "
        "effect).", body),
    Paragraph("How loudly a culture speaks confidence tells you almost nothing about what its "
              "people can do. Confidence talk is a dialect. Capability is a record. The tragedy of "
              "migration is arriving somewhere that grades your dialect while being unable to read "
              "your record.", pull),
]

# ================= 08 =================
story += [
    Paragraph("08 · What Migration Does to a Confident Person", h2),
    fig("migration_reset.png",
        "Fig 6 — The dismantling, assembled from Bandura's framework and this library's own "
        "measured findings."),
    Paragraph(
        "Why does the most confident population on earth produce so many quietly hesitant people "
        "abroad? Not fragility. Take Bandura's three properties — evidence-based, domain-specific, "
        "built by mastery — and migration attacks each in turn. <b>The evidence is voided:</b> "
        "foreign-only experience roughly halves callbacks; the name alone costs 40–50% more "
        "silence; every unexplained rejection is a small downward update from an environment that "
        "stopped crediting your history. <b>The domain shifts:</b> the skills that made you "
        "formidable in Lagos are real skills in a domain that no longer exists around you — "
        "domain-specificity misread as personal decline. <b>The witnesses are gone, replaced by "
        "judges:</b> the communal record stays home; the audience without the evidence remains.",
        body),
    Paragraph(
        "Understand this structurally and the shame lifts. The confident Nigerian who becomes a "
        "hesitant Torontonian has not changed personality. <b>The inputs to confidence changed, and "
        "the output followed.</b> Inputs can be re-engineered.", body),

    Paragraph("09 · The Threat in the Room", h2),
    Paragraph(
        "<b>Stereotype threat</b>, formalised by Steele and Aronson in 1995 and first measured on "
        "Black students, is the performance cost of knowing your group is negatively stereotyped in "
        "the domain you are performing in. Managing the threat consumes cognitive bandwidth, and "
        "performance drops below ability. Three things matter here: <b>the cost comes from carrying "
        "the threat, not from any deficit in ability</b>, which is why it vanishes when the threat "
        "is lifted; it compounds the CV findings — the screen discounts your record before the "
        "room, the threat taxes you inside it; and it is specifically a confidence thief, because "
        "underperformance you can feel happening reads internally as confirmation. The threat "
        "manufactures the evidence for itself.", body),
]

# ================= 10 & 11 =================
story += [
    PageBreak(),
    Paragraph("10 · The Affirmation That Actually Works", h2),
    Paragraph(
        "The researcher who discovered stereotype threat also documented the one affirmation "
        "practice that reliably neutralises it — and it looks nothing like Peale. In <b>values "
        "affirmation</b>, a person under threat writes briefly about something they genuinely value "
        "<i>in a completely unrelated domain</i> — faith, family, a craft. In the canonical "
        "experiments, women who did this before a hard maths test performed at the level of "
        "unthreatened peers. Affirming an unrelated strength restores the broader self, so the "
        "threatened domain shrinks to a small fraction of who you are.", body),
]
story += bullets([
    "<b>Affirm sideways, never at the target.</b> Writing “I am good at interviews” before an "
    "interview spotlights the fear and backfires. Writing about your mother's cooking, your faith, "
    "or the team you coach — that works. The African diaspora is unusually rich in exactly the "
    "affirmable material this requires.",
    "<b>Keep affirmations small, specific and evidenced.</b> “I prepare carefully for hard "
    "conversations” survives contact with your own scepticism. “I am unstoppable” is a flag "
    "planted across a canyon you have not crossed.",
    "<b>Note the trap:</b> the effect fades when it becomes a self-conscious technique. This is a "
    "practice of remembering who you are, not a chant about who you wish to be.",
])
story += [
    Paragraph("11 · The Four Sources, for the Diaspora", h2),
    fig("four_sources.png",
        "Fig 7 — Bandura's ranking. Bar lengths illustrate the ordering, not measured effect "
        "sizes."),
    Paragraph(
        "For the diaspora, the second source is the strategic one. <b>Vicarious experience works "
        "only when the model genuinely resembles you</b> — watching a native-born executive "
        "succeed tells your calibration system nothing about what <i>you</i> can do; watching a "
        "compatriot who arrived three years ago with your accent and your credential succeed tells "
        "it everything. This is why representation is machinery rather than sentiment — and why a "
        "functioning diaspora network is, quite literally, <b>confidence infrastructure</b>: a "
        "curated supply of believable models two steps ahead.", body),
]

# ================= 12 =================
story += [
    PageBreak(),
    Paragraph("12 · Rebuilding the Record Abroad", h2),
    fig("rebuilding.png",
        "Fig 8 — The rebuild, ordered by the strength of the evidence behind each practice."),
    Paragraph(
        "<b>Restart the record small</b> — mastery compounds from wins at the edge of current "
        "ability, not from leaps; the uncle with the market stall was never too proud for small, "
        "and that is why he is confident. <b>Engineer your models</b> — find the person who "
        "resembles you and is slightly ahead; mentoring someone behind you rebuilds your own "
        "calibration too. <b>Deploy values affirmation</b> before high-stakes moments — sideways. "
        "<b>Reinterpret the body</b> — the surge before the interview reads as “terrified” or "
        "“ready” depending on the story attached. And <b>spend the inheritance wisely</b>: the "
        "optimism you carry is the immune system of a continent, unstoppable when attached to a "
        "specific, finishable, evidence-generating plan — and dangerous when asked to substitute "
        "for one.", body),

    Paragraph("13 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First, some of the confidence gap abroad is rational, and calling it “imposter "
        "syndrome” obscures that.</b> The popular framing locates the problem inside the migrant's "
        "head. Our research measured the outside: the screen that discounts the record, the name "
        "that halves the callbacks, the threat in the room. The hesitancy is partly accurate "
        "perception, and the fix is partly environmental — networks, referrals, targeting — rather "
        "than therapeutic. Telling people to feel confident inside a machine built to discount them "
        "is Peale with better branding.", body),
    Paragraph(
        "<b>Second, African confidence has a shadow side this report cannot skip.</b> The same "
        "culture that produces magnificent self-belief also produces the fifth identical business, "
        "the “God will provide” that replaces the feasibility study, and the confident wire "
        "transfer into the scheme that collapses. Optimism uncorrected by ledgers is how CBEX "
        "happened. The raw material is world-class; the calibration layer is what needs building.",
        body),
    Paragraph(
        "<b>Third, the loudest person in the room is still not the most capable</b> — and the "
        "diaspora knows both errors from both sides. East Asia's results argue a culture can run "
        "on quiet competence; America's argue that stated confidence opens doors regardless. The "
        "wise position is bilingual: keep the record honest, and learn to speak the local "
        "confidence dialect fluently enough that your record gets read.", body),
    Paragraph("Confidence was never the feeling of being certain. It is the accumulated evidence "
              "of having survived uncertainty — and by that definition, nobody on earth arrives "
              "abroad with more of it than an African who got there.", pull),
]

# ================= 14 =================
story += [
    Paragraph("14 · Method &amp; Limits", h2),
    Paragraph("This report combines cross-national survey data with the experimental psychology of "
              "confidence, as at 24 August 2026.", body),
]
story += bullets([
    "<b>All cross-cultural confidence data is self-report, which is partly the phenomenon "
    "itself.</b> Modesty and self-enhancement norms shape how people answer surveys, not only how "
    "they feel. We treat stated confidence as a dialect precisely because the measurement problem "
    "and the finding are entangled.",
    "<b>The optimism figures are from Gallup International's end-of-year survey</b>; wording, "
    "sampling and urban skews vary by country, and single-year rankings move. The pattern — Global "
    "South optimism, Western anxiety — is stable across years and rival surveys; the percentages "
    "are snapshots. Kenya illustrates the volatility: historically among the most optimistic "
    "countries in youth surveys, yet last on youth economic confidence in the 2026 African Youth "
    "Survey.",
    "<b>The GEM 76% comes from the sub-Saharan regional analysis and is not a 2026 "
    "measurement</b>; country values vary widely (South Africa sits near 40%). It is self-assessed "
    "capability — which is part of the subject rather than a nuisance.",
    "<b>The East Asian negative correlation is an ecological finding</b> about groups and systems; "
    "it does not mean confidence harms an individual student.",
    "<b>The psychology cited is the replicated core</b> — Bandura, Steele, Taylor &amp; Brown, "
    "Oettingen — and where a famous result has replication trouble (the 2009 affirmation study), "
    "we said so in the text. These are levers, not switches.",
    "<b>Sections 05 and 06 are interpretive.</b> No study measures the informal economy as an "
    "efficacy machine or African optimism as a Taylor-Brown immune system; these are our "
    "syntheses, labelled as argument rather than measurement.",
    "<b>The framework reached us partly through a secondary source</b> — Mark Manson's "
    "<i>Confidence Guide</i>, shared by a member of this network. We went to the primary papers "
    "and cite those; the guide is credited as the pointer, not as evidence.",
    "<b>Nothing here is clinical advice.</b> Persistent anxiety or depression is a medical matter, "
    "not a calibration exercise.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Gallup International end-of-year global survey; GEM sub-Saharan Africa regional report; "
        "Bandura (1977) on self-efficacy and its four sources; Steele &amp; Aronson (1995) on "
        "stereotype threat and Martens et al. (2006) on values affirmation; Taylor &amp; Brown "
        "(1988) on positive illusions; Wood et al. (2009) and the 2020 replications on "
        "affirmations; Oettingen on fantasy and motivation; Amabile &amp; Kramer's progress "
        "principle; PISA analyses of the East Asian confidence paradox. Located partly via Mark "
        "Manson's Confidence Guide. Full inline links in the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/african-confidence-2026<br/>"
        "Companion reports: What Will People Say? · The Name on the CV · How Long Until It Was "
        "Worth It?<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
