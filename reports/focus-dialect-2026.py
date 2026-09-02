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
IMG = os.path.join(HERE, "focus-dialect-2026", "img")
OUT = os.path.join(HERE, "focus-dialect-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Focus Dialect · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 2 September 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Focus Dialect (2026)",
                      author="Africa Global Forum",
                      subject="Attention in Africa, the world outliers, and integrating into a foreign focus culture")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Focus", h1),
    Paragraph("dialect.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "The best selective attention ever measured in a laboratory belongs to Himba herders in "
        "northern Namibia — and South Africa and Kenya now top the entire world in daily screen "
        "time. Both facts are African, both are true, and together they demolish every lazy story "
        "about who can and cannot concentrate. What focus actually is, how cultures attend "
        "differently, why the diaspora's attention is structurally harder than anyone admits — "
        "and how reading a host culture's focus norms is one of the fastest integration skills "
        "you can learn.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("No. 1", big_num), Paragraph("9h 24m", big_num),
    Paragraph("47 sec", big_num), Paragraph("~13 IQ", big_num),
], [
    Paragraph("best selective attention<br/>on record: traditional<br/>Himba herders, Namibia", big_lbl),
    Paragraph("South Africa's daily time<br/>online — the most in the<br/>world; Kenya close behind", big_lbl),
    Paragraph("average attention on one<br/>screen today, down from<br/>2½ minutes in 2004", big_lbl),
    Paragraph("points of bandwidth<br/>consumed by financial<br/>scarcity — the remitter's tax", big_lbl),
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
    fig("himba.png",
        "Fig 1 — The Himba studies: the strongest attentional control in the cross-cultural "
        "record — and its reversal by urban exposure (Caparos, Linnell, de Fockert & Davidoff).",
        max_h=88 * mm),
    Paragraph("Published September 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/focus-dialect-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "A member of this network described her week in one sentence: at work in Frankfurt she is "
        "told she seems “scattered” in deep-work culture, and on Sunday her mother tells her she "
        "has become “too busy to pick up a phone”. Failing two attention cultures at once, in one "
        "head. This report is about that machine — and how to run it on purpose.", body),
]
story += bullets([
    "<b>The world's best measured focus is African.</b> Across a decade of studies, traditional "
    "Himba herders in Namibia outperformed British adults on selective-attention tasks across "
    "the board — the strongest attentional control on record. The same research found the kill "
    "switch: Himba who moved to town lost the edge. <b>Focus is not a trait cultures have. It is "
    "a state environments produce.</b>",
    "<b>The distraction environment has reached Africa at full strength.</b> South Africans "
    "spend 9 hours 24 minutes a day online — the most in the world; Kenya sits near the top at "
    "9:05; the world average is 6:38. The continent leapfrogged the desktop era straight into "
    "the most attention-hostile technology ever built.",
    "<b>Focus is also a dialect.</b> Western samples attend <i>analytically</i> — locking onto "
    "the focal object; interdependent cultures attend <i>holistically</i> — monitoring the whole "
    "field and its relationships. Neither is deficit. But migration means being graded in an "
    "attention dialect you did not grow up speaking.",
    "<b>The diaspora's focus is structurally harder, not weaker.</b> Two time zones of "
    "obligation, the always-answer norm, the vigilance of being on trial, the two-job schedule — "
    "and the scarcity tax: financial pressure alone consumes roughly 13 IQ points of bandwidth. "
    "Your attention is not broken. It is billed in two currencies.",
    "<b>Knowing the difference is an integration skill.</b> The colleague's headphones are a "
    "closed door, not a closed heart; your instant availability can read as absence of "
    "seriousness. Reading their focus rituals — and making yours legible — converts daily "
    "friction into fluency faster than almost anything else you can practise.",
])
story += [
    Paragraph("Your grandmother could follow one goat across a hillside of goats. The capacity "
              "is your inheritance. The environment is the fight.", pull),
]

# ================= 02 =================
story += [
    PageBreak(),
    Paragraph("02 · The Most Focused People on Record", h2),
    Paragraph(
        "Over a decade of fieldwork in northern Namibia, a Goldsmiths (University of London) "
        "team ran the standard laboratory attention batteries on <b>Himba pastoralists</b> and "
        "matched British adults. The result, replicated across tasks: <b>the Himba showed better "
        "selective attention than the Londoners, on both local-focus and global-focus tests</b>. "
        "They locked onto targets harder, ignored distractors better, and switched attentional "
        "scope more deliberately. In the published cross-cultural literature, nobody has "
        "out-focused a traditional Himba herder.", body),
    Paragraph(
        "Then the same team found the mechanism, and it is the whole report in miniature. Himba "
        "who had relocated to the regional town — same people, same upbringing, different "
        "environment — showed <b>defocused attention</b>; even traditional Himba who had merely "
        "<i>visited</i> town shifted measurably. The researchers' conclusion: urban environments "
        "“decrease attentional engagement”, pushing the mind toward constant exploration at the "
        "expense of engagement and control.", body),
    Paragraph(
        "Sit with what this means. The deepest measured focus on earth was produced by an "
        "African life: herding demands hours of sustained, selective, consequence-bearing "
        "attention — one animal tracked across a moving herd, one snake-shaped shadow monitored "
        "in the grass. <b>The capacity is not Western, not East Asian, not a gift of industrial "
        "schooling. On the best evidence available, it is most purely African.</b> What varies "
        "is the environment the capacity is deployed in — and that is the variable that follows "
        "you through the airport.", body),

    Paragraph("03 · The Foraging Brain", h2),
    Paragraph(
        "What is distraction, mechanically? A bee drains a flower and moves on; a brain exploits "
        "an information source until the estimated reward drops, then explores for a better one. "
        "Scientists call it the <b>explore–exploit dilemma</b>, and every phone-check mid-task "
        "is that ancient algorithm running exactly as built. Distraction is not a character "
        "flaw. It is <b>Stone Age foraging hardware dropped into an environment "
        "precision-engineered to exploit it</b>: infinite scroll removed the stopping points, "
        "variable rewards made every notification a maybe, and algorithms learned precisely how "
        "long to keep you at each flower. Three consequences: willpower is the wrong tool — you "
        "cannot out-discipline a slot machine, so the winners design their environment; the "
        "brain follows perceived importance — a task that does not feel like it matters makes "
        "exploration the rational default; and whoever controls the environment controls the "
        "focus — which is why the Himba result reverses in town.", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · The Feed Reaches the Continent", h2),
    fig("screen_time.png",
        "Fig 2 — Daily time online per internet user (DataReportal / GWI). Africa's connected "
        "populations now sit at the very top of the world.", max_h=95 * mm),
    Paragraph(
        "Here is the Himba mechanism at national scale. <b>South Africa leads the entire world "
        "in daily time online — 9 hours 24 minutes per internet user — with Kenya close behind "
        "at about 9:05</b>, alongside Brazil and the Philippines; the world average is 6:38, and "
        "Japan, the outlier, runs a tech superpower on roughly four hours. The same continent "
        "that produced the most focused community ever measured now contains the heaviest "
        "scrollers on earth. There is no contradiction — only the same finding repeated: change "
        "the environment, and the attention follows.", body),
    Paragraph(
        "Why did Africa arrive at the top? Partly measurement — the surveys count connected "
        "users, who skew young and urban. But mostly structure: Africa <b>leapfrogged the "
        "desktop era</b>. The first internet most of the continent touched was the phone — the "
        "most intimate, most interruptive, most algorithmically optimised attention machine "
        "ever built — arriving fused with the wallet (mobile money), the market (WhatsApp "
        "commerce), the church group and the family. For the diaspora this history travels: the "
        "phone is not a gadget you can casually put down, because it is simultaneously your "
        "bank branch, your obligation ledger, and the only door to everyone you love.", body),
]

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("05 · Focus Is a Dialect", h2),
    fig("aquarium.png",
        "Fig 3 — Masuda & Nisbett's aquarium studies: same tank, two ways of seeing. Neither is "
        "wrong."),
    Paragraph(
        "Focus does not just vary in amount — it varies in <b>shape</b>. In cross-cultural "
        "psychology's most famous perception experiments, Americans and Japanese watched the "
        "same animated aquarium. <b>Americans described the biggest, fastest fish. Japanese "
        "described the water, the rocks, the relationships</b> — referring to context roughly "
        "twice as often. The split — <b>analytic attention</b> (object-first, typical of Western "
        "samples) versus <b>holistic attention</b> (field-first, typical of interdependent "
        "cultures) — shows up in eye movements, memory, even what counts as “the point” of a "
        "scene.", body),
    Paragraph(
        "Where does Africa sit? Honestly: under-studied — the literature is a rebuke to "
        "psychology's WEIRD sampling problem. But the structural argument is straightforward: "
        "African social life is profoundly interdependent, and it trains exactly what holistic "
        "attention is — <b>continuous monitoring of people, relationships and context, because "
        "in a communal economy the context is the survival information</b>. The aunties tracking "
        "every guest's plate; the trader reading a whole market's mood; the child raised to "
        "notice who has not eaten. This is not distractibility. It is a different "
        "professional-grade attention, pointed at a different target. The tragedy is only that "
        "nobody at your performance review knows the dialect exists.", body),
    Paragraph("Analytic cultures focus on the fish. Holistic cultures focus on the water. "
              "Migration is being a water-reader in a fish-grading economy — while holding the "
              "world's heaviest phone.", pull),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · The Outliers", h2),
    fig("shrinking.png",
        "Fig 4 — Gloria Mark's two decades of workplace tracking: the West measured its own "
        "attention collapsing.", max_h=80 * mm),
]
story += bullets([
    "<b>The West is the strangest case: it invented both the deep-work cult and the distraction "
    "economy.</b> Attention on a single screen fell from 2½ minutes (2004) to 47 seconds; half "
    "of all screen sessions now last under 40 seconds; a genuine interruption costs ~23 minutes "
    "of refocusing. The same culture then built a booming market of focus apps and co-working "
    "subscriptions to buy back what its platforms took. When you integrate into a Western "
    "workplace, understand: <b>they are not natives of focus — they are refugees from their own "
    "environment.</b> Rituals are what cultures build where instinct failed.",
    "<b>Japan is the quiet outlier.</b> A technological superpower whose internet users report "
    "roughly four hours a day online — the lowest of any major economy — and whose craft "
    "culture (shokunin, monotasking, the tea ceremony's single-pointedness) treats sustained "
    "attention as a moral practice. Holistic attention did not stop deep focus; it shaped what "
    "the focus is for.",
    "<b>And the strongest outlier is the Himba</b> — a Namibian community out-focusing the "
    "industrialised world, until the industrialised environment arrived. No culture owns "
    "concentration. Environments rent it out.",
])

# ================= 07 =================
story += [
    PageBreak(),
    Paragraph("07 · The Scarcity Tax", h2),
    fig("scarcity_tax.png",
        "Fig 5 — Mullainathan & Shafir's scarcity research, translated to the remitter's "
        "ledger.", max_h=95 * mm),
    Paragraph(
        "Financial worry consumes cognitive bandwidth — <b>roughly 13 IQ points' worth</b>, "
        "comparable to losing a full night's sleep. In the field version, 464 Indian sugarcane "
        "farmers were tested before and after their annual harvest payout: <b>the same farmer "
        "scored significantly sharper once the money worry lifted</b>. Poverty does not make "
        "people less intelligent. It runs an unkillable background process in working memory — "
        "and attention is what the process eats.", body),
    Paragraph(
        "Now apply it to the remitting migrant. The black tax is not only a financial ledger — "
        "it is a <b>cognitive subscription</b>: rent here and school fees there, the exchange "
        "rate watched like weather, the sick aunt's results pending. Each is an open loop, and "
        "open loops are what working memory cannot put down. Add the vigilance of being on "
        "trial — monitoring how your accent, name and competence are landing, which consumes "
        "the same executive bandwidth — and the conclusion writes itself: <b>the diaspora "
        "professional who feels scattered is not weaker than their colleague. They are running "
        "more programs on the same hardware.</b>", body),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · The Interrupted Life Abroad", h2),
    fig("interrupted.png",
        "Fig 6 — The interruption stack. None of these five is a character flaw; all five are "
        "structural.", max_h=110 * mm),
    Paragraph(
        "Why this matters specifically in a demanding foreign culture: <b>two time zones of "
        "obligation</b> — home wakes in the middle of your workday, so the family WhatsApp "
        "detonates inside the deep-work block your job grades you on, at ~23 minutes per "
        "glance. <b>The always-answer norm</b> — in communal culture availability is love, and "
        "a phone that rings unanswered is a statement; you are caught between a culture that "
        "measures love in responsiveness and one that measures competence in unresponsiveness. "
        "<b>Vigilance</b> — the self-monitoring of the only African in the room is a background "
        "task with a bandwidth bill. <b>The portfolio of survival</b> — two jobs, night shifts "
        "and paperwork produce fragmented schedules, and nobody deep-works at hour fourteen. "
        "<b>And the feed as painkiller</b> — homesickness makes the scroll medicinal, the "
        "cheapest available visit home; shame-based app-deleting fails because the mood-repair "
        "loop runs on feelings, and the feeling here is longing.", body),
    Paragraph("The colleague who out-focuses you is not out-disciplining you. They are playing "
              "the same game with one time zone, one job, one audience and no ledger.", pull),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("09 · The Integration Decoder", h2),
    fig("decoder.png",
        "Fig 7 — The decoder. Integration is not becoming them; it is becoming bilingual, in "
        "both directions.", max_h=100 * mm),
]
story += bullets([
    "<b>Read their rituals as rituals, not rejection.</b> The headphones, the blocked calendar, "
    "the two-line email, the colleague who does not chat before 11 — in deep-work cultures these "
    "are focus liturgy, the formal rules a distraction-saturated society built because instinct "
    "failed. The warmth is not absent; it is scheduled. Taking the closed door personally costs "
    "relationships that were never actually cold.",
    "<b>Know what your norms broadcast.</b> Answering every call instantly, monitoring the group "
    "chat in meetings, treating availability as politeness — in your dialect this is respect; in "
    "theirs it can read as never fully here. The fix is naming the dialect out loud: “I go "
    "heads-down 9 to 12; after that I'm all yours” converts what they misread as flakiness into "
    "what they respect as discipline.",
    "<b>Deploy the holistic advantage deliberately.</b> Field-first attention — reading rooms, "
    "tracking relationships, noticing the client's hesitation everyone else missed — is rare and "
    "valuable in analytic workplaces. Volunteer for the stakeholder-heavy, people-dense work "
    "where it wins.",
    "<b>And run the exchange home too.</b> Explain the host dialect to your family as a window, "
    "not a wall: “my deep hours are your night; my 7 p.m. is fully yours.” Most families accept "
    "a reliable window with gratitude. What breaks trust is not boundaries; it is unexplained "
    "silence.",
])

# ================= 10 & 11 =================
story += [
    PageBreak(),
    Paragraph("10 · The Diaspora Focus Toolbox", h2),
    fig("toolbox.png",
        "Fig 8 — The toolbox, translated for a life in two time zones. Every item is "
        "environmental, not motivational.", max_h=110 * mm),
    Paragraph(
        "<b>Schedule home; don't silence it</b> — a reliable daily hour answered with full "
        "presence honours the always-answer value and protects the deep block: boundary without "
        "abandonment. <b>Move the phone, not the willpower</b> — its mere presence on the desk "
        "measurably drains working memory (Ward, 2017); another room, because removing the cue "
        "survives homesickness where debating it does not. <b>Protect one block like a shift</b> "
        "— 90 defended minutes at your best hour outproduce a fragmented day, and that is where "
        "the citizenship form and the conversion exam go; energy is the substrate, and 17–19 "
        "hours awake impairs you like alcohol. <b>Borrow a body</b> — body doubling rides "
        "social facilitation, psychology's oldest finding, and it is the chama principle again: "
        "nobody scrolls in front of the group. <b>Start stupidly small</b> — two minutes on the "
        "avoided task; initiation, not completion, is where focus dies.", body),

    Paragraph("11 · The Four Triggers, Diaspora Edition", h2),
    Paragraph(
        "When focus fails, it fails for one of four reasons — <b>importance, clarity, calmness, "
        "or health</b> — and forcing effort through the symptom is painkillers for a broken "
        "leg. <b>Importance:</b> is the task actually yours? Half the diaspora's to-do list is "
        "borrowed — a brain refusing a goal you never chose is not malfunctioning; it is "
        "voting. <b>Clarity:</b> “sort my papers” is fog; “find my reference number” is a step — "
        "migration bureaucracy manufactures fog at industrial scale. <b>Calmness:</b> a nervous "
        "system running precarity and visa anxiety attends to every threat at once, which is "
        "functionally focusing on nothing; regulate first. <b>Health:</b> shift-slept, "
        "dehydrated, hour twelve — no system compensates; sometimes the answer is water, food "
        "and one honest night of sleep. Run the four before the guilt. The answer is usually "
        "one of them — and almost never “you are lazy”.", body),
]

# ================= 12 & 13 =================
story += [
    PageBreak(),
    Paragraph("12 · The African Advantage", h2),
    Paragraph(
        "The deepest measured focus on record is African. The attention dialect our cultures "
        "train — holistic, relational, field-first — is professional gold in every job that "
        "involves human beings. The communal structures our cultures built are the top-ranked "
        "intervention in the literature: body doubling is the harambee of attention, and the "
        "study group, the chama meeting and the church committee are focus technologies with "
        "centuries of field testing. The discipline of the market stall — open every dawn, one "
        "transaction at a time, fully present — is monotasking of a purity the productivity "
        "industry sells courses about.", body),
    Paragraph(
        "What Africa and its diaspora face is not a focus deficit. It is a <b>focus heist</b>: "
        "the world's most attention-hostile environment, delivered through the world's most "
        "indispensable device, to the populations with the heaviest cognitive load and the "
        "youngest median age — plus, abroad, a grading system that recognises only one dialect. "
        "Name it that way and the strategy stops being self-improvement and becomes defence of "
        "a resource. <b>Your attention is the last asset that arrived with you fully intact "
        "through customs. Guard it like the remittance it funds.</b>", body),

    Paragraph("13 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First: the always-available norm has costs we bill to each other.</b> The community "
        "that respects no closed doors also interrupts its own students before exams and its "
        "own founders before launches. If availability is love, then guarding each other's "
        "focus blocks is love too — the community that texts “call me when you surface” instead "
        "of triple-calling is richer, in degrees and businesses, than the one that measures "
        "loyalty in ringtones.", body),
    Paragraph(
        "<b>Second: nine hours is still nine hours.</b> The scroll is medicinal, the phone is "
        "the bank and the door home — and the medicine has a dosage problem, the feed's owners "
        "are not neutral pharmacists, and the hours are real hours out of finite lives. "
        "Compassion for why we scroll cannot become a permission slip. The honest question is "
        "the one this library keeps asking about money: who is the audience for this hour, and "
        "what do they contribute to your actual life?", body),
    Paragraph(
        "<b>Third: do not integrate all the way into the burnout.</b> The deep-work culture you "
        "are learning to read also produced the 47-second attention span and the loneliest "
        "workplaces on record — it is a culture coping, not a culture arrived. Learn its "
        "dialect fluently, use its rituals gladly, and keep the thing it is trying to buy back: "
        "the presence, the long conversation, the meal without screens, the afternoon with an "
        "elder that our cultures never lost. Integration done right is bilingual, not "
        "converted.", body),
]

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("14 · Method &amp; Limits", h2),
    Paragraph("This report combines cross-cultural attention research, workplace attention "
              "tracking, digital-use data and cognitive economics, as at 2 September 2026.", body),
]
story += bullets([
    "<b>The Himba findings</b> come from a programme of peer-reviewed studies using standard "
    "laboratory tasks with necessarily modest field samples. “Best selective attention "
    "measured” means best in the published cross-cultural comparisons we could find; Fig 1's "
    "bars illustrate the replicated ordering, not exact scores. The urbanization effect is the "
    "programme's own within-culture comparison.",
    "<b>Screen-time figures</b> are from DataReportal/GWI-based surveys of internet users, who "
    "skew young and urban — which inflates African national figures relative to whole "
    "populations. The ranking is stable across recent waves; exact minutes are marked "
    "approximate where uncertain.",
    "<b>The 2½-minutes-to-47-seconds decline and the ~23-minute interruption cost</b> are "
    "Gloria Mark's longitudinal workplace research, overwhelmingly on US knowledge workers.",
    "<b>The analytic/holistic literature is badly under-sampled in Africa.</b> Our placement of "
    "African attention on the holistic-relational side is a structural argument from "
    "interdependence, labelled as argument. Sections 05, 08, 09 and 12 are interpretive "
    "syntheses in the same sense.",
    "<b>The scarcity findings</b> (13 IQ points; sugarcane farmers) are from Mullainathan &amp; "
    "Shafir's programme; effect sizes have been debated in replications, though the bandwidth "
    "mechanism is well supported. The “remitter's bandwidth tax” is our extension — no study "
    "has measured scarcity load in remitting migrants specifically. That absence is itself a "
    "finding.",
    "<b>The framework reached us partly through a secondary source</b> — Mark Manson's <i>Focus "
    "Toolkit</i>, shared by a member of this network. We went to the primary papers it "
    "references — Pirolli &amp; Card on information foraging, Ward on smartphone brain drain, "
    "Zajonc on social facilitation, Kurzban's opportunity-cost model — and cite those; the "
    "toolkit is credited as the pointer, not as evidence.",
    "<b>Nothing here is clinical advice.</b> Focus problems that persist across every "
    "environment can be ADHD — real, treatable, and heavily under-diagnosed in African "
    "communities. A stuck year deserves an assessment, not another system.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Caparos, Linnell, Bremner, de Fockert &amp; Davidoff (2013) and the wider Himba "
        "research programme, including the urbanization studies; Masuda &amp; Nisbett (2001) on "
        "holistic versus analytic attention; DataReportal / GWI digital-use surveys; Gloria "
        "Mark's attention-span research (UC Irvine); Mullainathan &amp; Shafir on scarcity and "
        "bandwidth; Ward, Duke, Gneezy &amp; Bos (2017) on smartphone brain drain; Pirolli "
        "&amp; Card (1999) on information foraging; Zajonc (1965) on social facilitation; Deci "
        "&amp; Ryan on self-determination; Kurzban et al. (2013) on the opportunity-cost model; "
        "Williamson &amp; Feyer (2000) on sleep deprivation. Located partly via Mark Manson's "
        "Focus Toolkit. Full inline links in the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/focus-dialect-2026<br/>"
        "Companion reports: The Sense of Time · The Cost of Later · The Envy Economy · The Most "
        "Optimistic People on Earth<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
