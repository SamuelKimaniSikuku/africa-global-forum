#!/usr/bin/env python3
"""Generate the AGF report PDF: The Third Fire — The Developing World in the AI Era (2026)."""

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
IMG = os.path.join(HERE, "third-fire-2026", "img")
OUT = os.path.join(HERE, "third-fire-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Third Fire · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 16 September 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Third Fire (2026)",
                      author="Africa Global Forum",
                      subject="How the developing world was, is, and will be in the AI era — with the lessons of the internet and the atom, told simply for every reader")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Third", h1),
    Paragraph("fire.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Written for everyone — your parents, your teenage cousin, the friend who has "
        "never opened an AI app. One story in three pieces: how the developing world WAS "
        "before AI, how it IS in the era's first four years, and how it WILL BE on the "
        "three roads ahead. It starts with the two great teachers: the atom, which gave "
        "the world 9% of its electricity AND twelve thousand warheads — and the internet, "
        "which grew from 39 million users to six billion and delivered both M-Pesa and "
        "the scam economy. Every powerful tool arrives with two hands. This is the story "
        "of the newest one, told simply, with the numbers — and in the words of the "
        "people who built each era.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("9%", big_num), Paragraph("39m→6bn", big_num),
    Paragraph("847m", big_num), Paragraph("19", big_num),
], [
    Paragraph("of world electricity from the<br/>atom — beside ~12,000<br/>warheads. Both hands", big_lbl),
    Paragraph("internet users, 1995–2025 —<br/>M-Pesa AND the scam arrived<br/>on the same phone", big_lbl),
    Paragraph("people below $3.00/day —<br/>the waiting world that<br/>AI arrived into", big_lbl),
    Paragraph("the median African age —<br/>the youngest people meet<br/>the newest tool", big_lbl),
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
    fig("pattern.png",
        "Fig 1 — The pattern, across five technologies: the tool never chooses. People "
        "do.", max_h=80 * mm),
    Paragraph("Published September 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/third-fire-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "One plain definition first, so nobody is left outside: AI — artificial "
        "intelligence — means computer programs that can read, write, answer questions "
        "and do office work the way a person does. Since late 2022 they became good "
        "enough for anyone to use, free, on an ordinary phone. That is all the technical "
        "background you need. The five findings:", body),
]
story += bullets([
    "<b>History has seen this movie before — twice, recently.</b> Nuclear science "
    "produced clean electricity for 31 countries AND the two bombs of 1945; the internet "
    "grew from 39 million users to six billion, delivering M-Pesa and free knowledge AND "
    "scams and misinformation. Powerful technologies do not choose between good and bad. "
    "They do both, at once — and people decide the mix.",
    "<b>How they were:</b> before AI, the developing world was a waiting world: 847 "
    "million below the $3.00/day line, 85% of African work informal, 655 million without "
    "electricity, and 10–12 million young Africans chasing ~3 million formal jobs a "
    "year. AI arrived at a queue, not a paradise.",
    "<b>How they are:</b> four years in, the era is real but early — AI can touch 34% "
    "of jobs in rich countries and 11% in poor ones, yet only a fifth of rich-world "
    "firms use it. Both hands already show: six weeks of supervised AI tutoring in "
    "Nigeria produced some of the biggest cheap learning gains ever measured — while "
    "the office-job ladder poor countries hoped to climb is being sawn off by the same "
    "machine.",
    "<b>How they will be:</b> three roads to 2040 — the leapfrog (the gap narrows), "
    "left behind again (AI arrives only as an import), and the split (likeliest: both "
    "at once). No expert knows which wins. Anyone claiming to is selling something.",
    "<b>The deciding factors are not mysterious — and none is AI.</b> Power to the 655 "
    "million; African languages in the tools; rules written early; classrooms that "
    "teach WITH the machine. Four hinges, all human choices.",
])
story += [
    Paragraph(
        "Fire cooked our food and burned our villages. The atom lit cities and "
        "flattened two. The internet gave Kenya M-Pesa and gave the world the scam "
        "call. Now comes the third fire — and the only question that matters is the old "
        "one: whose hands, and which hand?", pull),
]

# ================= 02 =================
story += [
    Paragraph("02 · Every Tool Has Two Hands", h2),
    Paragraph(
        "Fire cooked food, warmed homes and lit the dark — and burned villages and "
        "armed wars. Nobody concluded fire was good or bad; every family learned to "
        "keep it in the hearth and away from the roof. The printing press filled the "
        "world with books — and with propaganda. This is not coincidence; it is a law: "
        "a technology is powerful precisely because it amplifies what people do, and "
        "people do both kinds of things.", body),
    Paragraph(
        "The loudest voices about AI shout one of two things: “it will save us” or "
        "“it will destroy us.” History's answer to both is the same: yes. Both, at "
        "once, in proportions not yet decided — and different countries and families "
        "will experience the mix differently. The two most recent powerful technologies "
        "show how that works, and the developing world lived through both. Two short "
        "lessons, then our own story.", body),
]

# ================= 03 =================
story += [
    Paragraph("03 · Lesson One: The Atom", h2),
    fig("nuclear.png",
        "Fig 2 — One science, two futures (World Nuclear Association, IAEA, FAS "
        "warhead estimates).", max_h=112 * mm),
    Paragraph(
        "In the 1940s scientists learned to split the atom. Within a decade the same "
        "knowledge produced two opposite things: bombs that killed over a hundred "
        "thousand people in two mornings — and power stations. Today 416 reactors in 31 "
        "countries quietly generate about 9% of the world's electricity, while ~12,000 "
        "warheads still stand. Nobody “chose” between the futures; the science did "
        "both. What varied is what people built — and the world noticed early: "
        "Eisenhower's “Atoms for Peace” speech at the UN in 1953, and the treaties "
        "that followed, kept the weapons at nine countries while the electricity spread "
        "to thirty-one.", body),
    Paragraph(
        "Two lessons travel to AI. Rules written early matter — the atom got treaties "
        "because a mushroom cloud photographs well; AI's harms are quieter (a job "
        "unfilled, a lie believed), so early rules are harder to demand. And the "
        "developing world got the short end of both futures: one African country "
        "generates nuclear power, and most of the continent received neither the "
        "electricity nor a seat at the rule-writing table. When people say Africa must "
        "be in the room where AI rules are written, the atom is the receipt for what "
        "happens when it is not.", body),
]

# ================= 04 =================
story += [
    Paragraph("04 · Lesson Two: The Internet", h2),
    fig("internet.png",
        "Fig 3 — The internet's thirty years (ITU; Central Bank of Kenya).", max_h=112 * mm),
    Paragraph(
        "In 1995 the internet had 39 million users — under 1% of humanity, almost none "
        "in Africa. Today: about six billion, 74% of everyone alive. No tool ever "
        "spread faster. And the part the Silicon Valley histories skip: the internet's "
        "most celebrated financial invention happened in Nairobi. M-Pesa — sending "
        "money by phone, no bank account needed — launched in 2007 for people the "
        "banking system ignored, and today mobile money moves more than half of "
        "Kenya's GDP, with M-Pesa alone serving over 34 million users. The developing "
        "world did not just receive the internet; it did something with it the rich "
        "world had not imagined — because it aimed the tool at its own problems. "
        "Remember that sentence.", body),
    Paragraph(
        "The other hand arrived in the same envelope: the phone that carries school "
        "fees carries the con artist's call; the networks that reunited families carry "
        "the rumours; the platforms that taught millions were engineered to be "
        "un-put-downable. Nobody voted; everybody adapted. The internet's double lesson "
        "for the AI era: the developing world can win bigger than the inventors "
        "imagined — and the bad arrives bundled with the good, on the same device, in "
        "the same year. Preparation beats surprise.", body),
]

# ================= 05 =================
story += [
    Paragraph("05 · Piece One: How They Were", h2),
    fig("before.png",
        "Fig 4 — The world AI arrived into (World Bank, ILO, AfDB, SDG7 tracking).", max_h=118 * mm),
    Paragraph(
        "You cannot judge what a technology changes without knowing what it found. It "
        "found a developing world that was WORKING — nearly everyone works — but "
        "waiting. 847 million people below $3.00 a day, nearly half of Sub-Saharan "
        "Africa among them. 85.3% of African work informal: farms, stalls, workshops, "
        "boda bodas — real work without contracts or protection. The formal job was the "
        "scarce prize: 10–12 million young Africans entering the market yearly against "
        "roughly 3 million formal jobs. Four chasing every one, before any computer "
        "learned to write.", body),
    Paragraph(
        "It found classrooms short of teachers, clinics short of doctors, and 655 "
        "million people — over 560 million of them African — without electricity. And "
        "it found the world's youngest population: median age about nineteen, half the "
        "continent younger than the internet itself. A world short of everything except "
        "young people. That is what AI arrived into — a waiting world, wondering if "
        "this tool, finally, was the one that would be aimed at ITS problems.", body),
]

# ================= 06 =================
story += [
    Paragraph("06 · Piece Two: How They Are", h2),
    fig("now.png",
        "Fig 5 — 2022–2026, measured (ILO, OECD, World Bank, the Nigerian randomized "
        "tutoring evaluation).", max_h=115 * mm),
    Paragraph(
        "Four years in: earlier than the noise suggests, and both hands visible. The "
        "reach is uneven by design — AI can touch about 34% of rich-country jobs but "
        "11% of poor-country ones, because AI does office work and most "
        "developing-world work is not office work. The farmer, the trader and the "
        "mason are safe from the machine (and untouched by its gains). Even where it "
        "can reach, only about one firm in five in the rich world actually used AI in "
        "2025. The era has begun; the race has not been run.", body),
    Paragraph(
        "The good hand, measured: in Nigeria, a randomized experiment — the gold "
        "standard of testing, like a medical trial — gave schoolchildren six weeks of "
        "supervised AI tutoring and produced learning gains among the largest ever "
        "measured for a cheap program. A new value chain runs from data-labelling "
        "piecework at ~$2 an hour (hard, poorly paid — and a first rung) to structured "
        "remote AI work at $1,000–2,000 a month. Farmers ask crop questions by chatbot "
        "in Kiswahili; students everywhere quietly study with it.", body),
    Paragraph(
        "The bad hand, measured: the office-job ladder poor countries planned to climb "
        "— call centres, back offices, the path that lifted India and the Philippines — "
        "is being sawn off: ~1 million Philippine call-centre jobs rated at risk by "
        "2030, and the first jobs AI takes are exactly the clerk-and-assistant roles "
        "that were the developing world's first formal rungs. Scams are now written "
        "fluently by machine; and a careful Kenyan trial that gave small businesses AI "
        "advice found no average gain — the weakest did WORSE, because fluent advice "
        "is not capital. Both hands, same countries, same year. Exactly as the "
        "internet taught us to expect.", body),
]

# ================= 07 =================
story += [
    Paragraph("07 · Piece Three: How They Will Be", h2),
    fig("futures.png",
        "Fig 6 — Scenarios, not predictions. Anyone claiming to know which road wins "
        "is selling something.", max_h=118 * mm),
    Paragraph(
        "Road one: the leapfrog. The developing world aimed the internet at its own "
        "problems and produced M-Pesa. AI suits a repeat even better, because its "
        "scarcest ingredient is expertise — exactly what the developing world has "
        "always lacked. On this road, power arrives (Mission 300: 300 million Africans "
        "connected by 2030), the tools learn African languages, classrooms teach with "
        "the machine, and the youngest population adopts it fastest. The tutor, the "
        "doctor's assistant and the crop advisor reach every pocket — and for the "
        "first time in a century, the gap NARROWS.", body),
    Paragraph(
        "Road two: left behind again. The atom's pattern repeats: benefits concentrate "
        "where the power stations, computers and rule-writers already are. The office "
        "jobs poor countries hoped to sell are automated in the rich world instead; AI "
        "arrives only as an import, priced in dollars; the tools never learn the "
        "languages. The cost is mostly invisible — not mass firings but opportunities "
        "that quietly never arrive: the cruellest kind of loss, because nobody "
        "protests a job that was never created.", body),
    Paragraph(
        "Road three: the split — likeliest. Both roads at once: Kenya leapfrogs in one "
        "sector while a neighbour stalls; Nairobi wins while a rural county waits for "
        "power; the family that learns the tools pulls ahead of the family that fears "
        "them. The dividing line is not luck — it is the four hinges of Section 11, "
        "and every one of them is a human decision. That is the most hopeful sentence "
        "in this report, if you read it slowly.", body),
]

# ================= 08 =================
story += [
    Paragraph("08 · The Bright Side, Counted", h2),
]
story += bullets([
    "<b>The teacher that never leaves.</b> A tutor for every child was the one reform "
    "no budget could afford. It now costs approximately nothing — and the Nigerian "
    "trial measured what it does. The same for a first-opinion health assistant, a "
    "legal explainer, a crop advisor.",
    "<b>The precedent with receipts.</b> M-Pesa: 34+ million users, over half of "
    "Kenya's GDP flowing through mobile money — built where experts said it could not "
    "be. The playbook (aim the tool at local problems) is proven and repeatable.",
    "<b>Work that ignores borders.</b> $1,000–2,000/month remote AI roles reachable "
    "from Nairobi or Kigali — incomes that once required a visa now require a "
    "connection.",
    "<b>Help that makes the helper stronger.</b> The best workplace study so far found "
    "AI made customer-service workers 15% more productive — with the biggest gains to "
    "the newest workers. The tool helped the bottom most: the opposite of how most "
    "technologies have worked.",
    "<b>The demographic jackpot.</b> The youngest population on earth meets the most "
    "powerful learning tool ever built — while the rich world ages out of exactly such "
    "people. No other region holds this card.",
])

# ================= 09 =================
story += [
    Paragraph("09 · The Dark Side, Counted", h2),
]
story += bullets([
    "<b>The ladder, sawn.</b> ~1M Philippine BPO roles at risk by 2030; young workers "
    "in AI-exposed jobs measurably behind their peers; the entry office job — the "
    "developing world's classic first formal rung — is the first thing the machine "
    "does cheaply.",
    "<b>Lies at industrial quality.</b> Deepfake scams up over 1300% in recent counts; "
    "the con artist now writes perfect English, and soon perfect Kiswahili; election "
    "rumours arrive with video. Young institutions have the least immune system.",
    "<b>Rented rails.</b> Models, chips and clouds owned elsewhere, priced in dollars "
    "— a leapfrog that can be re-priced or restricted by other countries' boardrooms.",
    "<b>Gains stack where advantages already are.</b> The Kenyan business-advice trial "
    "(no average gain; weakest firms −10%) and the IMF's intelligence-divide warning "
    "point one way: without deliberate effort, AI widens gaps before it closes any.",
    "<b>The invisible cost.</b> Road two's signature harm is not a firing; it is the "
    "BPO park never built, the industry that migrated to machines before it could "
    "migrate to Africa. No headline will report it. This report exists partly so "
    "somebody counts it.",
])

# ================= 10 =================
story += [
    Paragraph("10 · What the Builders Said", h2),
    fig("voices.png",
        "Fig 7 — Four eras, four warnings-and-promises. Documented public statements, "
        "sourced in Section 14.", max_h=138 * mm),
    Paragraph(
        "Andrew Ng, who taught a generation of AI engineers: “AI is the new "
        "electricity” — it will soak into everything until nobody calls it technology. "
        "Sundar Pichai went further: more profound than electricity or fire. But the "
        "same industry speaks in its other voice too. Sam Altman, whose company built "
        "ChatGPT, told the US Senate: “If this technology goes wrong, it can go quite "
        "wrong.” Geoffrey Hinton — the “godfather of AI”, who spent fifty years "
        "building it — left Google in 2023 to warn freely: “It is hard to see how you "
        "can prevent the bad actors from using it for bad things.” When the builders "
        "themselves speak in both voices, believe both voices.", body),
    Paragraph(
        "The older eras left their words too. Einstein, 1946: “The unleashed power of "
        "the atom has changed everything save our modes of thinking” — the tools "
        "change faster than the wisdom; the whole danger in one sentence. And Mandela, "
        "1995, as the internet era opened: “The capacity to communicate will almost "
        "certainly be a key human right in the twenty-first century.” Swap "
        "“communicate” for “compute”, and Madiba's sentence is this report's "
        "argument: access to the new tool is not a luxury debate. It is a justice "
        "debate.", body),
]

# ================= 11 =================
story += [
    Paragraph("11 · What Decides Which Road", h2),
    fig("decides.png",
        "Fig 8 — Four hinges, none mysterious, all human decisions.", max_h=138 * mm),
    Paragraph(
        "None of the four is about AI itself. Electricity: no power, no era — 655 "
        "million people are locked out before the story starts, which is why Mission "
        "300, a dams-and-grid project with no algorithms in it, is the most important "
        "AI decision on the continent. Language: tools trained on English work worst "
        "for those who need them most; putting Kiswahili, Hausa, Yoruba and Amharic "
        "into the machines is cheap — and the one hinge Africans can turn without "
        "anyone's permission. Rules: the atom got treaties, the internet got almost "
        "none and delivered the scam economy; whether AI gets real rules — and who "
        "sits at the table writing them — decides who is protected and who is the "
        "product. People: the median African is nineteen and meets the most powerful "
        "learning tool ever built this decade; whether schools teach WITH it or ban it "
        "is the quietest hinge and possibly the biggest.", body),
]

# ================= 12 =================
story += [
    Paragraph("12 · What You Can Do — No Technical Degree Required", h2),
]
story += bullets([
    "<b>Touch the tool this week.</b> The free AI apps work in a browser on an "
    "ordinary phone. Ask real questions for ten minutes. Fear of AI is mostly fear of "
    "the unknown; ten minutes converts it into judgement.",
    "<b>Teach the family both hands.</b> The M-Pesa-era rule again: wonderful tool, "
    "and never trust a voice, video or message just because it sounds real. Agree a "
    "family code word for money requests — this one habit defeats most AI-era fraud.",
    "<b>Let the children use it — supervised.</b> Tutoring with an adult involved "
    "produced remarkable gains; unsupervised leaning weakened learning. Same rule as "
    "fire: with the child, not instead of the child.",
    "<b>Verify before you share.</b> The scam economy and the rumour economy both run "
    "on forwarding. The five-second pause — who says this, and how do they know? — is "
    "a civic act now.",
    "<b>Choosing studies or work?</b> This library holds your map: The Leapfrog Test "
    "(the university decision at home), Before You Board (studying abroad), The New "
    "Ladder (the jobs evidence in full).",
    "<b>Hold any influence at all</b> — a classroom, a chama, a company, a pulpit, a "
    "WhatsApp group? Spend it on the four hinges: power, language, rules, skills. The "
    "roads are still open. That is the point of telling the story now.",
])

# ================= 13 =================
story += [
    Paragraph("13 · The Uncomfortable Part", h2),
]
story += bullets([
    "<b>Analogies teach, but can mislead.</b> AI is like the atom and the internet in "
    "its double-handedness — but unlike them it improves itself yearly, spreads at "
    "zero cost, and speaks. The history lessons are a floor for thinking, not a "
    "ceiling.",
    "<b>The future sections are scenarios, not forecasts.</b> No probabilities were "
    "assigned because none can be defended. A reader in 2030 should expect parts of "
    "Piece Three to look naive — we cannot know which parts.",
    "<b>This report was made with the technology it describes</b> — drafted, charted "
    "and fact-checked with AI assistance under human editorial control. Disclosed here "
    "and in Section 14; a reader who finds that circular is owed the acknowledgement.",
    "<b>The calm tone is itself a choice.</b> Some serious people believe AI risk "
    "deserves alarm; others believe the harms talk is overblown. We let the verified "
    "numbers set the temperature — and where the numbers ran out, we said so, and "
    "stopped.",
])

# ================= 14 =================
story += [
    Paragraph("14 · Method & Limits", h2),
]
story += bullets([
    "<b>Nuclear:</b> World Nuclear Association / IAEA (~9% of world electricity; 416 "
    "reactors in 31 countries); FAS warhead estimates (~12,000); nine nuclear-armed "
    "states; South Africa as the continent's only nuclear-power operator.",
    "<b>Internet:</b> 39.2M users (1995) to ~6bn / 74% (2025), ITU-based; Africa "
    "region 36%. Mobile money: Central Bank of Kenya (agents transacted over half of "
    "Kenya's GDP in 2024); M-Pesa 34M+ users. “Flows through” is a transaction "
    "measure, not value created.",
    "<b>Baseline and AI-era numbers</b> are carried from our verified companion "
    "reports: poverty 847M ($3.00/day, World Bank Mar 2026), informality 85.3% (ILO), "
    "electricity 655M (SDG7 2026), jobs arithmetic (AfDB), exposure 34%/11% (ILO), "
    "adoption 20.2% (OECD), the Nigerian tutoring RCT, the QJE +15% experiment, the "
    "Kenyan GPT-4 business RCT, Philippine BPO risk (~1M, officially debated), wage "
    "ranges (journalistic), deepfake growth (industry-reported) — all sourced in full "
    "in The Leapfrog Test, The New Ladder and The Algorithm at the Border.",
    "<b>Quotes</b> are documented public statements: Pichai (2018 interview remarks); "
    "Ng (2017 Stanford talk); Altman (US Senate testimony, May 2023); Hinton (New "
    "York Times interview, May 2023); Einstein (1946 telegram, as published); "
    "Eisenhower (“Atoms for Peace”, UN, Dec 1953); Mandela (Telecom 95, Geneva, "
    "Oct 1995). Reproduced in their commonly documented form.",
    "<b>Simplifications:</b> readability was chosen over precision — “AI” means the "
    "2022–26 generative wave; “the developing world” compresses very different "
    "countries; three roads compress a continuum. The companion reports carry the "
    "uncompressed versions.",
    "<b>Futures flag:</b> Sections 07–09 and 11–12 are scenarios and judgement, not "
    "measurement. Flagged for revisit by mid-2027 with the rest of the AI series.",
    "<b>AI use in production:</b> drafted, charted and fact-checked with AI assistance "
    "under editorial control — the same tools this report describes. Every "
    "load-bearing number verified against the primary source; the interpretation and "
    "errors are ours.",
])
story += [
    Paragraph(
        "Companion reports — the AI series this report overviews: The Algorithm at the "
        "Border (the journey), The New Ladder (the jobs), The Leapfrog Test (the home "
        "front), Before You Board (the student's handbook). All at "
        "africaglobalforum.com/reports. · Africa Global Forum · Research · 2026 · "
        "Free to read and share — especially with those who have never opened an AI app.", small),
]

doc.build(story)
print("PDF built:", OUT)
