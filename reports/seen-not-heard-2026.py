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
IMG = os.path.join(HERE, "seen-not-heard-2026", "img")
OUT = os.path.join(HERE, "seen-not-heard-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "Seen and Not Heard · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 2 September 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="Seen and Not Heard (2026)",
                      author="Africa Global Forum",
                      subject="The silent African childhood, the adult voice it shaped, and raising the next generation heard")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("Seen and", h1),
    Paragraph("not heard.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Many of us were raised to be quiet. It worked — maybe too well. “Don't talk when adults "
        "are talking.” “Never answer back.” A silent child was a disciplined child, and the goal "
        "was respect. But the discipline ran one way — commands and consequences, no conversation "
        "— and the side effects show up decades later, in adults who are capable but quiet, "
        "talented but shy, full of ideas they never say out loud. What that upbringing built, "
        "what it cost, what it got right — and how the respect stays while the silence goes.",
        lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("9 in 10", big_num), Paragraph("0 of 17", big_num),
    Paragraph("3 of 4", big_num), Paragraph("2×", big_num),
], [
    Paragraph("children in Nigeria and Ghana<br/>experience violent discipline<br/>at home (UNICEF)", big_lbl),
    Paragraph("outcomes favoured physical<br/>punishment in the largest<br/>meta-analysis ever run", big_lbl),
    Paragraph("of Bandura's confidence<br/>sources cancelled by the<br/>silent, error-only home", big_lbl),
    Paragraph("as often rated effective:<br/>teams where people feel<br/>safe to speak up (Google)", big_lbl),
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
    fig("one_way.png",
        "Fig 1 — The one-way channel. Discipline was real; conversation was not on the "
        "curriculum.", max_h=88 * mm),
    Paragraph("Published September 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/seen-not-heard-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "This report began as a few paragraphs shared inside this network that hit a nerve: "
        "<i>we knew exactly what we did wrong, and never learned what we did right</i>. The "
        "response told us it was not one family's story. So we took the lived observation to the "
        "research, and report back honestly.", body),
]
story += bullets([
    "<b>The upbringing is real and near-universal.</b> The one-way home — instruction down, "
    "silence up — is the documented default across much of the continent and its diaspora: "
    "UNICEF finds 9 in 10 children in Nigeria and Ghana experience violent discipline, and "
    "researchers consistently classify African parenting as high-control, low-negotiation. "
    "Obedience was the product, and the product shipped.",
    "<b>The side effects are the ones the essay named.</b> Sixty years of research from Baumrind "
    "onward: discipline-without-conversation produces obedient children who score lower on "
    "self-esteem, social confidence and assertiveness — while discipline-<i>with</i>-conversation "
    "produces the confident, competent adults every parent was aiming for. The variable was "
    "never the rules. It was the voice.",
    "<b>“You cannot build confidence on nothing” is literally what the science says.</b> Bandura's "
    "sources of self-belief include being told, by people who matter, that you are doing well. "
    "The silent home cancelled that source entirely; error-only feedback builds a compass with "
    "one hemisphere — you know every wrong turn and none of the right ones.",
    "<b>The lesson does not expire at eighteen — and abroad it compounds.</b> The economies the "
    "diaspora moved into pay out on exactly what the childhood punished: Google found "
    "psychological safety — the freedom to speak up — the number-one factor in team performance. "
    "The meeting is a dinner table with worse lighting, and the old rule still runs.",
    "<b>The fix is not Western permissiveness.</b> The evidence-backed target keeps everything "
    "our parents valued — boundaries, respect, standards — and changes one thing: the channel "
    "opens both ways. Confidence is not taught; it is experienced, one completed sentence at a "
    "dinner table at a time. <b>The respect stays. The silence goes.</b>",
])
story += [
    Paragraph("A silent child was called a disciplined child. Nobody asked what the silence was "
              "practising for.", pull),
]

# ================= 02 & 03 =================
story += [
    PageBreak(),
    Paragraph("02 · The House Rules", h2),
    Paragraph(
        "In the classic African home, a child's standing orders were clear: be quiet around "
        "adults, do as told, never answer back. Greetings were mandatory and scripted; opinions "
        "were not solicited; questions beyond a certain line were insolence. When adults spoke, "
        "you became furniture. <b>You were there to be seen, not heard</b> — and a child who "
        "mastered the art was praised to other parents as <i>disciplined</i>, the highest "
        "compliment the system issued.", body),
    Paragraph(
        "The feedback architecture matters as much as the silence. <b>Mistakes were corrected "
        "fast</b> — loudly, specifically, often physically. But good behaviour, good marks, good "
        "work? Silence — or the famous audit: <i>where are the other points?</i> Love was real "
        "and enormous, but proved in school fees and sacrifice, almost never in words. The "
        "system was not lazy and not loveless; it was a deliberate technology with a clear goal "
        "— respect, obedience, survival — and by its own metrics it worked. The question is what "
        "else it built, that nobody ordered.", body),

    Paragraph("03 · An English Proverb in an African Mouth", h2),
    Paragraph(
        "The flag we defend as tradition is often an import. <b>“Children should be seen and not "
        "heard” is an English proverb</b> — recorded around 1450 in Mirk's Festial (“A mayde "
        "schuld be seen, but not herd” — aimed, originally, at young women) and industrialised "
        "into child-rearing doctrine by the Victorians. It arrived in Africa the way the clock "
        "did: through the mission school, the colonial classroom and the cane — institutions "
        "designed to produce quiet, compliant subjects — which then handed the method to homes "
        "as <i>modern</i> discipline.", body),
    Paragraph(
        "Pre-colonial Africa was not a continent of silent children. The record shows societies "
        "that took the training of <b>speech</b> seriously in ways the Victorian model never "
        "did: evening riddling and story sessions where children performed; age-grade systems "
        "with formal oratory instruction; the palaver tradition; the griot lineages of West "
        "Africa, where eloquence was a hereditary profession of the highest status. Respect for "
        "elders was absolute — and it coexisted with structured, celebrated channels for young "
        "voices. <b>The pure silence doctrine is the colonial residue, not the ancestral "
        "inheritance.</b> Retiring it is not abandoning culture. It is repatriating an older "
        "one.", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · The Parenting Map", h2),
    fig("baumrind.png",
        "Fig 2 — Baumrind's framework. The goal was never less discipline; it was discipline "
        "plus conversation.", max_h=105 * mm),
    Paragraph(
        "Baumrind's map has two axes: how much parents <b>demand</b> (rules, standards) and how "
        "much they <b>respond</b> (warmth expressed, reasons given, voice allowed). The dials "
        "are independent, and the outcomes split accordingly. <b>Authoritative</b> homes — high "
        "demands <i>and</i> open channel — reliably produce the most confident, competent adults "
        "in the literature. <b>Authoritarian</b> homes — high demands, closed channel — produce "
        "exactly what ours advertised: obedient children who score lower on happiness, social "
        "competence and self-esteem. <b>Permissive</b> homes — the “spoiled” children African "
        "parents point at — genuinely underperform too. The alternative to permissiveness was "
        "never silence; it was every rule kept, plus reasons, plus a channel up.", body),
    Paragraph(
        "One honest caveat, here and in Method: research on African, African-American and "
        "immigrant families shows the authoritarian style's harm profile is <b>moderated by "
        "context</b> — where strictness is normative and clearly bonded to love and protection, "
        "children often read it as care, and outcomes are less negative than in white Western "
        "samples. The old way was not poison. It was simply — as the evidence keeps saying — "
        "not the best version of itself.", body),
]

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("05 · The Measured Baseline", h2),
    fig("numbers.png",
        "Fig 3 — UNICEF's violent-discipline data and the Gershoff meta-analysis: the baseline, "
        "measured.", max_h=95 * mm),
    Paragraph(
        "UNICEF's household surveys measure “violent discipline” — physical punishment and/or "
        "psychological aggression in the past month: <b>94% of Ghanaian children</b> and <b>91% "
        "of Nigerian children</b> in the most recent rounds; worldwide, <b>two in three "
        "children</b> — 1.6 billion. This is not an African peculiarity; it is a global norm at "
        "its strongest. On outcomes, the largest analysis ever conducted — Gershoff and "
        "Grogan-Kaylor's review of five decades and 160,000 children — found that of 17 measured "
        "outcomes, <b>not one favoured physical punishment</b>.", body),
    Paragraph(
        "Two honest notes. Most of these associations are correlational, and the cultural-"
        "moderation caveat is real. And — more important — <b>the cane is not even the core of "
        "the story</b>. The deepest claim is about the silence: the missing praise, the closed "
        "channel, the one-hemisphere compass. A home can retire the stick and keep the silence — "
        "many modern African homes have — and the confidence machinery stays broken. That is why "
        "the fix is conversation, not just gentler punishment.", body),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · The Compass That Never Formed", h2),
    fig("compass.png",
        "Fig 4 — Error-only feedback: a map with one hemisphere."),
    Paragraph(
        "Learning requires two signals: <i>stop that</i> and <i>more of that</i>. The one-way "
        "home transmitted the first at full volume and the second at zero. The result is an "
        "adult who can recite every childhood failing verbatim decades later — and who genuinely "
        "does not know what they are good at, because <b>no authoritative voice ever told "
        "them</b>. In Bandura's terms: mastery experiences went unconfirmed — a win nobody names "
        "does not update your self-belief; verbal persuasion was structurally absent — praise "
        "was feared as the fertiliser of pride; and where discipline was harsh, the "
        "physiological channel ran on vigilance. <b>Three of four confidence sources, cancelled "
        "or crippled.</b> Confidence is not taught; it is experienced — and an experience never "
        "reflected back might as well not have happened. You cannot build confidence on "
        "nothing.", body),

    PageBreak(),
    Paragraph("07 · The Lesson That Doesn't Expire", h2),
    fig("expires.png",
        "Fig 5 — The silence that was safety, still running — decades past its expiry date.",
        max_h=105 * mm),
    Paragraph(
        "The pattern the child's brain learned was clean: <b>your voice causes problems; silence "
        "keeps you safe.</b> Eighteen consecutive years of confirmation, from the people you "
        "loved most. That is not a habit; it is training — and training does not check your "
        "birthday before running. The meeting where you have the answer and do not raise your "
        "hand. The salary negotiation that never happens, because negotiating with a superior "
        "still feels like answering back. The seminar where participation is a fifth of the "
        "grade and your respectful silence is marked as absence. The ideas composed fully, "
        "internally, and never released. And the compliment that bounces: adults who never heard "
        "“well done” at seven do not automatically believe it at thirty-seven.", body),
    Paragraph("Speaking up was punished at seven, so it is impossible at thirty-seven. The "
              "lesson was learned perfectly. That was the problem.", pull),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · What Voice Is Worth Abroad", h2),
    fig("voice_worth.png",
        "Fig 6 — Project Aristotle and Edmondson's psychological-safety research: the modern "
        "economy pays out on voice.", max_h=100 * mm),
    Paragraph(
        "When Google studied 180 of its own teams, the number-one predictor of performance was "
        "not talent, seniority or workload — it was <b>psychological safety</b>: whether members "
        "felt safe to speak up, ask questions and challenge ideas. Teams high on it were <b>rated "
        "effective twice as often by executives</b>. Edmondson's founding research carries the "
        "sharpest version: the best hospital teams <i>reported more errors</i> than the worst — "
        "because speaking up was safe. <b>Silence does not mean nothing is wrong. It means "
        "nobody is saying it</b> — a sentence every graduate of the one-way home can verify from "
        "childhood.", body),
    Paragraph(
        "Stack the diaspora's position: the market pays for voice — ideas credited, raises "
        "negotiated, mistakes flagged early — the childhood trained its opposite, and the CV "
        "research shows we start with a discount only advocacy can claw back. Success today "
        "depends on being confident, outspoken and willing to challenge — <b>the exact opposite "
        "of what we were taught.</b> Not because the West is right about everything, but because "
        "that is the tariff structure of the economy we chose to work in.", body),

    Paragraph("09 · What the Old Way Got Right", h2),
]
story += bullets([
    "<b>The standards were a gift.</b> High expectations are half of the winning quadrant — the "
    "half Western permissiveness threw away. The diaspora's academic overperformance came from "
    "homes where excellence was assumed, not requested.",
    "<b>The respect trained something valuable.</b> Deference done right is attention — "
    "listening, reading rooms, honouring experience — and that relational attention is worth "
    "real money professionally. Cultures that train only self-expression produce meetings full "
    "of talkers and empty of listeners.",
    "<b>The love was real, and sacrifice was its language.</b> Parents who never said “I love "
    "you” paid it in night shifts and school fees for decades. The channel was wrong; the signal "
    "was enormous.",
    "<b>And the context was survival.</b> A generation raised under colonial administrators and "
    "hard states taught silence because, for them, a mouthy child was in danger — and for Black "
    "parents abroad, “the talk” still teaches exactly this calculus today. The silence was "
    "armour, sized for a world the parents knew. The question is whether the armour still fits "
    "the world the child actually lives in.",
])

# ================= 10 =================
story += [
    Paragraph("10 · Rebuilding the Adult Voice", h2),
    fig("rebuild.png",
        "Fig 7 — The rebuild. Voice is built like confidence: by reps, not affirmations.",
        max_h=105 * mm),
    Paragraph(
        "The repair follows the confidence mechanics, because it is the same machinery: <b>voice "
        "is re-learned by experience, in graded doses, with witnesses.</b> Start where the "
        "stakes are lowest — one question per meeting, one corrected order at a restaurant, one "
        "“I see it differently” per week: mastery experiences in miniature, each a data point "
        "against eighteen years of the old dataset. Script the first sentence before the meeting "
        "— the barrier is initiation, not vocabulary. Practise in safer rooms first: the chama, "
        "the church committee, this Forum — where the accent is home and a stumble costs "
        "nothing. Name the training out loud to a mentor: “I was raised not to challenge "
        "authority; I'm unlearning it” converts a mystery weakness into a visible journey. And "
        "re-parent the inner critic: the voice that says <i>who asked you?</i> is a recording, "
        "not a referee. You have kept the ledger of everything you did wrong since childhood. "
        "Start keeping the other one.", body),
]

# ================= 11 =================
story += [
    PageBreak(),
    Paragraph("11 · The Dinner Table", h2),
    fig("dinner_table.png",
        "Fig 8 — The whole edit, at the table. The respect stays; the silence goes.",
        max_h=105 * mm),
    Paragraph(
        "For the next generation the intervention is almost embarrassingly cheap, and it starts "
        "at the dinner table. Regular mealtime conversation tracks with children's vocabulary, "
        "school performance and later mental health — and the active ingredient is the "
        "<b>turn</b>: the child asked about their day, and <i>waited for</i>. Let them finish "
        "sentences, even slow, childish, wrong ones; a child allowed to complete a thought "
        "learns that thoughts are completable and their voice does not cause problems. Then fix "
        "the feedback ledger: <b>praise the process, precisely and out loud</b> — “you worked "
        "hard at that” builds persistence where “you're so clever” builds fragility and silence "
        "builds the one-hemisphere compass. When they attempt hard things, tell them it gets "
        "easier — because it does. Tell them you love them, in words, and hug them; school fees "
        "are love, but children cannot hear them. <b>A child who feels loved does not spend "
        "adulthood searching for that feeling.</b>", body),

    Paragraph("12 · The Second Generation", h2),
    Paragraph(
        "Your child is being raised between two grammars — a school that grades hands-up "
        "assertiveness, and a home that grades deference. Handled by accident, the collision "
        "produces the worst of both: children who learn their parents' culture as the thing that "
        "silences them. Handled on purpose, it is an inheritance: a child fluent in both — "
        "respectful <i>and</i> heard, able to honour an elder at the table and challenge a "
        "professor in the seminar. The recipe is <b>authoritative, bicultural, explicit</b>: "
        "keep the standards and the respect; open the channel; and narrate the two grammars out "
        "loud — “at Shangazi's house we greet first and let elders finish; at school, raise your "
        "hand and argue your point — both are respect, in different languages.” A child told the "
        "rules of both rooms owns both rooms. The foundation is not only for the child. <b>It is "
        "for the generation that comes from that child</b> — the first one raised with the "
        "respect and the voice, instead of a forced choice between them.", body),
]

# ================= 13 =================
story += [
    PageBreak(),
    Paragraph("13 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First: we are not just survivors of this system; we are its current operators.</b> "
        "The reflex that hushes a child mid-sentence at a family gathering, the “who asked "
        "you?” deployed on a nephew, the pride we feel when someone calls our quiet child “so "
        "disciplined” — the system runs on us now. The test is small and brutal: the next time "
        "a child in your orbit interrupts adults with something to say, watch what you do "
        "before you think.", body),
    Paragraph(
        "<b>Second: blaming our parents is a dead end — and so is pretending nothing "
        "happened.</b> They ran the software they were given, under conditions where it was "
        "rational, and they paid for our lives with theirs. Both things are true: they did "
        "their best, <i>and</i> some of what they did left marks. The mature position holds "
        "both — gratitude without amnesia, honesty without prosecution. The account is settled "
        "by what we do at our own tables, not by what we relitigate at theirs.", body),
    Paragraph(
        "<b>Third: the goal is voice, not noise.</b> Overcorrect into the cult of "
        "self-expression — every feeling broadcast, every thought a take — and we trade a "
        "silence problem for a listening problem, and the cultures we moved to are drowning in "
        "that one. The old system's deepest value, underneath the distortion, was that speech "
        "is weighty and other people matter. Keep that. The child we are trying to raise — and "
        "the adult we are trying to become — is not the loudest in the room. It is the one who "
        "can speak when it counts, stay silent by choice rather than by training, and tell the "
        "difference. That is what “the respect stays, the silence goes” actually means.", body),
]

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("14 · Method &amp; Limits", h2),
    Paragraph("This report combines parenting research, cross-cultural developmental psychology, "
              "survey data on child discipline and organisational research on voice, as at 2 "
              "September 2026.", body),
]
story += bullets([
    "<b>This report began as a member essay</b> shared inside this network; its argument "
    "structure and several of its lines are retained deliberately. The research was gathered to "
    "test the essay's claims, not to decorate them.",
    "<b>The parenting-styles literature is heavily correlational</b> — parenting is not randomly "
    "assigned — and dominated by Western samples. The authoritative-style advantage is among its "
    "most consistent findings; exact effect sizes vary.",
    "<b>The cultural-moderation caveat is real and stated in the text:</b> studies of African, "
    "African-American and immigrant families find authoritarian-style parenting less harmful "
    "where it is normative and embedded in evident love. Our claim is not that the old way broke "
    "everyone; it is that the evidence points to a better version that keeps its strengths.",
    "<b>The UNICEF figures</b> (Ghana 94%, Nigeria 91%, world 2-in-3) measure “violent "
    "discipline” — physical punishment and/or psychological aggression in the past month, by "
    "caregiver report (MICS). Prevalence, not severity.",
    "<b>The Gershoff &amp; Grogan-Kaylor meta-analysis</b> (2016; ~160,000 children) is robust "
    "in direction, debated in magnitude, and largely correlational. We report it as the balance "
    "of evidence, which it is.",
    "<b>The organisational-voice research</b> (Edmondson; Project Aristotle) measures specific "
    "corporate and clinical settings; we use it to establish that modern knowledge economies "
    "reward voice, not as a universal law.",
    "<b>The historical section</b> rests on the documented English origin of the proverb "
    "(Mirk's Festial, c. 1450) and the ethnographic record of African oratory traditions; the "
    "colonial-import claim is our synthesis, labelled as argument. Pre-colonial practices "
    "varied enormously and included strong deference norms of their own.",
    "<b>Sections 06–08's application to diaspora adults is interpretive</b> — no study traces "
    "“seen and not heard” childhoods into diaspora salary negotiations directly. The mechanisms "
    "are established; the join is ours.",
    "<b>Nothing here is clinical advice.</b> Where childhood discipline crossed into abuse, or "
    "its echoes are heavy, a professional conversation is not a luxury — and having one is a "
    "break with the silence, not a betrayal of anyone.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "The parenting-styles literature from Baumrind (1966) onward; UNICEF MICS "
        "violent-discipline data (Ghana, Nigeria, global); Gershoff &amp; Grogan-Kaylor (2016) "
        "on physical punishment; Bandura (1977) on the sources of self-efficacy; Dweck on "
        "process versus person praise; Edmondson (1999) on psychological safety and Google's "
        "Project Aristotle; research on African immigrant parenting; the documented origin of "
        "the proverb in Mirk's Festial (c. 1450); family-mealtime research on child language "
        "and wellbeing. Full inline links in the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/seen-not-heard-2026<br/>"
        "Companion reports: The Most Optimistic People on Earth · What Will People Say? · Three "
        "Generations to Silence<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
