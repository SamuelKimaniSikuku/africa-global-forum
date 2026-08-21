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
IMG = os.path.join(HERE, "economics-of-shame-2026", "img")
OUT = os.path.join(HERE, "economics-of-shame-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Economics of Shame · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 19 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="What Will People Say? (2026)",
                      author="Africa Global Forum",
                      subject="Shame as a system of social enforcement in Africa, and what it costs")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("What Will People Say?", h1),
    Paragraph("The economics of shame.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Shame is usually discussed as a feeling. It is more useful to treat it as <b>a system of "
        "government</b> — a way of enforcing behaviour that costs nothing to run and works without "
        "police, courts or records. It is extraordinarily effective. This report is about what it is "
        "for, and what the bill looks like.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("90%", big_num), Paragraph("80%", big_num),
    Paragraph("15", big_num), Paragraph("2 in 5", big_num),
], [
    Paragraph("with mental illness in sub-<br/>Saharan Africa get no care", big_lbl),
    Paragraph("with epilepsy receive<br/>no treatment", big_lbl),
    Paragraph("Ghana's individualism<br/>score — the UK is 89", big_lbl),
    Paragraph("adults deterred from<br/>business by fear of failure", big_lbl),
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
    fig("the_words.png",
        "Fig 1 — The vocabulary. African terms are given as dictionary equivalents rather than as "
        "ethnographic claims — each carries meanings the English word does not.", max_h=95 * mm),
    Paragraph("Published August 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/economics-of-shame-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Every society needs a way of making people behave without watching them. Rich, "
        "institutionalised societies mostly use law and internalised conscience. Most of the world, "
        "including most of Africa, uses something cheaper and older: <b>the certainty that other "
        "people are watching, and that they will talk.</b>", body),
    Paragraph("It works. That is the part usually missed. And it has a price, which is now "
              "measurable.", body),
]
story += bullets([
    "<b>The enforcement is real.</b> On Hofstede's individualism scale, where 100 is the most "
    "individualist, <b>Ghana scores 15 and Nigeria 30</b>, against <b>89 for the UK and 91 for the "
    "US</b>. Low scores mean the group's judgement outranks the individual's.",
    "<b>The health bill is enormous.</b> Around <b>90%</b> of people with mental illness in "
    "sub-Saharan Africa receive no professional care, and around <b>80%</b> of people with epilepsy "
    "receive no treatment. In reviews of barriers to mental health care, stigma accounts for about "
    "<b>a quarter</b> of the obstacles named most often.",
    "<b>There is also almost nobody to go to.</b> About <b>2.2 mental health workers per 100,000</b> "
    "against a global median of <b>13.5</b>, and roughly <b>one psychiatrist per million</b> in "
    "sub-Saharan Africa. Silence suppresses demand; absent demand justifies not building services.",
    "<b>Women pay disproportionately.</b> Infertility prevalence reaches <b>up to 30%</b> in some "
    "sub-Saharan populations, and the woman is blamed <b>even where the medical cause is male</b>. "
    "Documented consequences include exclusion, disinheritance, violence and suicide.",
    "<b>It suppresses risk-taking.</b> Globally, fear of failure deters <b>two in five adults</b> "
    "from starting a business. Where stigma against failure is highest, people who have closed a "
    "business are <b>least likely to start another</b>.",
    "<b>It follows people abroad.</b> Diaspora members keep funding failing projects because "
    "stopping would be an admission, and fear returning home more than they fear staying somewhere "
    "that is not working.",
    "<b>And it is not an African peculiarity.</b> Hindi has <i>log kya kahenge</i>. Spanish has "
    "<i>¿qué dirán?</i> Japanese has <i>sekentei</i>. Mandarin has <i>mianzi</i>. South Korea, at "
    "<b>18</b>, is more collectivist than Nigeria.",
])
story += [
    Paragraph("Shame is not a flaw in African culture. It is a technology for producing order "
              "without institutions — and it becomes expensive at exactly the moment a society "
              "acquires institutions and forgets to switch.", pull),
]

# ================= 02 =================
story += [
    PageBreak(),
    Paragraph("02 · Everybody Has a Word For It", h2),
    Paragraph(
        "Start with language, because it is the cheapest evidence available and it points the same "
        "way everywhere. Fig 1 on the cover has the vocabulary.", body),
    Paragraph(
        "Hausa <i>kunya</i> does not translate cleanly as “shame.” It covers modesty, restraint, and "
        "the propriety that governs how you behave in front of in-laws and elders — a virtue as much "
        "as an affliction. Yoruba <i>ìtìjú</i> carries a similar double edge: to have none is a "
        "serious accusation.", body),
    Paragraph(
        "That double edge is the whole subject. In English, shame is close to unambiguously bad — "
        "something to be recovered from. In much of the world it names <b>both the punishment and "
        "the virtue of being susceptible to it.</b> A person without shame is not free; they are "
        "dangerous.", body),
    Paragraph(
        "And the question is universal. <i>Log kya kahenge</i> in South Asia. <i>¿Qué dirán?</i> in "
        "Spain and Latin America. <i>Sekentei</i> in Japan — not quite “society” but the invisible "
        "watching public whose opinion regulates conduct. If a phrase exists in that many unrelated "
        "languages, it is describing something structural rather than something cultural.", body),

    Paragraph("03 · Shame Is a Governance System", h2),
    Paragraph(
        "Every society has to solve the same problem: how do you get people to keep promises, care "
        "for relatives, avoid theft and honour obligations when nobody is checking?", body),
    Paragraph(
        "You can build <b>institutions</b> — contracts, courts, credit scores, police, registries. "
        "That is expensive. It requires functioning states, literacy, records, and enforcement that "
        "cannot be bought.", body),
    Paragraph(
        "Or you can use <b>reputation</b>. Make everyone's standing depend on what everyone else "
        "thinks, and the enforcement runs itself. No budget, no staff, no paperwork. In a village of "
        "four hundred people where you will live your whole life, this is close to unbeatable.", body),
    Paragraph("Where the state is weak, shame is not a substitute for law. It <i>is</i> the law. And "
              "it is enforced by everyone, all the time, for free.", pull),
    Paragraph(
        "The system has one design characteristic that matters more than any other: <b>it punishes "
        "visibility, not harm.</b> An action is costly to the extent it is seen. That is a "
        "serviceable proxy for wrongdoing in a small community where everything is seen anyway. It "
        "becomes a very poor proxy in a city of fifteen million, and a catastrophic one when the "
        "thing being hidden is an illness.", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · Three Ways to Make People Behave", h2),
    fig("three_systems.png",
        "Fig 2 — The guilt–shame–fear typology, popularised after Ruth Benedict's 1946 work. Useful "
        "as a lens; unreliable as a map."),
    Paragraph(
        "In <b>guilt</b> cultures the punishment is internal: you feel bad even if nobody knows. In "
        "<b>shame</b> cultures the punishment is exposure: what matters is being seen. In <b>fear</b> "
        "cultures the sanction is attributed to unseen forces. Estimates commonly put "
        "guilt-innocence at roughly <b>30% of the world</b>, with the remainder predominantly "
        "honour-shame or fear-power.", body),
    Paragraph(
        "We include this framework because it is genuinely clarifying, and then we have to say "
        "plainly that <b>the popular version of it is bad social science.</b> It originates largely "
        "in wartime anthropology and later missionary literature. Its usual mapping — the West as "
        "guilt, Asia and the Middle East as shame, <i>Africa as fear-power</i> — is crude, "
        "essentialising, and carries an unmistakable hierarchy, with the West assigned the "
        "introspective conscience and Africa assigned superstition.", body),
    Paragraph(
        "All three mechanisms operate in every society. British bankruptcy carries shame; Nigerian "
        "courts enforce law; American reputational cancellation is shame with a modern interface. "
        "What differs is the <i>mix and the weighting</i>, and that is measurable without the "
        "typology.", body),
]

# ================= 05 =================
story += [
    PageBreak(),
    Paragraph("05 · Where Africa Actually Sits", h2),
    fig("individualism.png",
        "Fig 3 — Hofstede individualism scores. Higher means more individualist. These are "
        "decades-old survey instruments applied to whole countries — see Method &amp; Limits."),
    Paragraph(
        "<b>Ghana at 15 and Nigeria at 30 are strongly collectivist.</b> So is <b>South Korea at "
        "18</b> — more collectivist than Nigeria, in one of the richest, most institutionalised, "
        "most technologically advanced societies on earth. <b>Japan sits at 46</b>, near the middle. "
        "<b>South Africa at 65</b> is closer to Britain than to Ghana.", body),
]
story += bullets([
    "<b>This is not an African trait.</b> The most collectivist country in Fig 3 is in East Asia. "
    "Whatever is happening is not about Africa, and any argument that treats it as an African "
    "cultural defect is refuted by the chart.",
    "<b>It does not disappear with development.</b> South Korea got rich without becoming "
    "individualist. Shame-based enforcement is not a stage societies grow out of on the way to "
    "modernity — which means the costs described below are not self-correcting.",
])
story += [
    Paragraph(
        "“Africa” is also doing far too much work in this discussion. Fifty-four countries, over a "
        "thousand languages, and enormous internal variation. Everything in this report should be "
        "read as a pattern with heavy local exceptions.", body),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · What Is Shameful", h2),
    fig("domains.png",
        "Fig 4 — The recurring domains. Compiled from the stigma literature cited throughout this "
        "report."),
    Paragraph("Look at that list and a pattern appears immediately. <b>Almost every item is "
              "something that happens to a person rather than something they did.</b>", body),
    Paragraph(
        "Infertility is a medical condition. Epilepsy is a neurological one. Mental illness is an "
        "illness. Business failure is frequently a currency movement. Being unmarried at thirty-five "
        "is not an act.", body),
    Paragraph(
        "This is the central malfunction. A reputational system evolved to punish <i>choices</i> — "
        "theft, betrayal, broken obligations — has been pointed at <i>conditions</i>. And the "
        "sanction it applies, exposure, is precisely the wrong treatment for every condition on the "
        "list, because all of them require disclosure to be resolved.", body),
    Paragraph("You cannot be treated for something you cannot admit to having.", pull),
]

# ================= 07 =================
story += [
    PageBreak(),
    Paragraph("07 · The Bill: Health", h2),
    fig("health_cost.png",
        "Fig 5 — Treatment and disclosure gaps. These gaps have multiple causes; stigma is one of "
        "several."),
    Paragraph(
        "Around <b>90% of people needing mental health care in sub-Saharan Africa never receive "
        "professional care</b>. In a systematic review of barriers, <b>stigmatisation accounted for "
        "about a quarter</b> of the obstacles encountered most often. Around <b>80% of people with "
        "epilepsy</b> receive no treatment — a condition that is often controllable with inexpensive "
        "medication. A large study in suburban Senegal found <b>51% of respondents believed evil "
        "spirits caused epilepsy</b>; surveys in Rwanda found most respondents thought people with "
        "epilepsy should not be allowed to attend school or work.", body),
    Paragraph(
        "On HIV, pooled analysis across African countries finds discriminatory attitudes running "
        "<b>as high as 80%</b> of the population in some settings, and <b>more than half</b> of "
        "people with HIV in some settings choosing not to disclose their status.", body),
    fig("workforce.png",
        "Fig 6 — Mental health workforce density, WHO. A third of the African workforce counted here "
        "are non-professional workers."),
    Paragraph(
        "We want to be careful not to blame culture for a budget problem. Much of the 90% would go "
        "untreated in a society with no stigma at all, simply because there is nowhere to go. But "
        "the two are not independent: <b>silence suppresses measured demand. Absent demand justifies "
        "not funding services. Absent services make disclosure pointless, which deepens the "
        "silence.</b> Stigma and scarcity are a loop, not two separate problems.", body),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · The Bill: Who Carries It", h2),
    fig("infertility.png",
        "Fig 7 — Infertility in sub-Saharan Africa. Prevalence from a systematic review; the "
        "attribution of blame from a systematic review and meta-synthesis of infertility-related "
        "stigma in Africa."),
    Paragraph(
        "Sub-Saharan Africa has some of the highest infertility prevalence in the world — reaching "
        "<b>up to 30%</b> in some populations, with rates between 15% and 30% reported in South "
        "Africa, Nigeria and Ethiopia. Much of it is preventable, caused by untreated reproductive "
        "tract infection.", body),
    Paragraph(
        "The research finding that matters is this: <b>women are blamed even when male-factor "
        "infertility is medically identified as the cause.</b> Studies across Egypt, Nigeria, "
        "Mozambique and the Gambia record childless women being excluded from ceremonies, treated as "
        "inauspicious, kept away from children, ostracised, disinherited, subjected to physical and "
        "psychological violence, and in some cases driven to suicide.", body),
    Paragraph(
        "The mechanism recurs everywhere shame operates. <b>A woman's standing is tied to an outcome "
        "she does not control, and the sanction lands on whoever is most socially exposed rather "
        "than on whoever is medically responsible.</b> That is not a moral system malfunctioning at "
        "the edges. It is what a visibility-based system does by default.", body),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("09 · The Bill: Risk and Money", h2),
    fig("fear_failure.png",
        "Fig 8 — Fear of failure and entrepreneurship. Global Entrepreneurship Monitor; the "
        "stigma-and-re-entry finding from research in Small Business Economics."),
    Paragraph(
        "Globally, fear of failure deters roughly <b>two in five adults</b> from entrepreneurship. "
        "Research finds that in countries where stigma against business failure is highest, "
        "<b>entrepreneurs who exit a failed business are less likely to re-enter</b> — the talent is "
        "not merely discouraged once, it is removed permanently.", body),
]
story += bullets([
    "<b>Failure is concealed rather than examined.</b> If a closed business is a personal disgrace, "
    "nobody publishes what went wrong, and the next person repeats it. Shame destroys the feedback "
    "loop that makes an economy learn.",
    "<b>Debt is hidden until it is unrecoverable.</b> The point at which a problem is admitted is "
    "the point at which it can still be solved. Shame moves that point later, often past rescue.",
    "<b>People fund failing projects rather than admit them.</b> Our investment report found exactly "
    "this: diaspora members continuing to send money to builds they had privately stopped believing "
    "in, because stopping would be a public verdict.",
])

# ================= 10 =================
story += [
    PageBreak(),
    Paragraph("10 · The Bill: The Diaspora", h2),
    Paragraph(
        "Migration does not escape this system. It intensifies it, for a structural reason: <b>you "
        "are now being judged by people who cannot see your circumstances.</b>", body),
]
story += bullets([
    "<b>The obligation you cannot refuse.</b> A contributor writing about Cameroon named it the "
    "<i>loyalty tax</i>: where contracts are weak, guilt is the enforcement mechanism, and the "
    "person abroad cannot credibly walk away without abandoning a village.",
    "<b>The asymmetry of visibility.</b> People at home see the currency conversion, not the rent. A "
    "refusal reads as hoarding rather than as being stretched. Shame requires an audience that can "
    "see, and this audience structurally cannot.",
    "<b>The fear of returning.</b> Every community has the story of the man who came back after ten "
    "years with one bag. That story is the migration itself being read as a verdict on the person. "
    "It keeps people in situations that are not working long past the point where leaving would be "
    "rational.",
    "<b>The silence about not coping.</b> Accounts describe people funding relatives while living on "
    "savings, or reaching sixty abroad with no retirement provision, and never saying so — because "
    "the one thing that cannot be admitted is that the migration did not deliver.",
])
story += [
    Paragraph("The diaspora exports the enforcement and imports none of the support. You remain "
              "fully accountable to a community that can no longer see you, and fully unable to "
              "explain a life it has never witnessed.", pull),
    Paragraph(
        "There is a specific, cruel version of this in the health data. Africans abroad live in "
        "countries where mental health services exist and are frequently free at the point of use — "
        "and carry the disclosure norms of societies where they do not. The scarcity constraint is "
        "lifted; the shame constraint travels.", body),
]

# ================= 11 =================
story += [
    PageBreak(),
    Paragraph("11 · The Cultures That Share It", h2),
    Paragraph("Nothing above is African, and the comparison is not a consolation. It is analytically "
              "useful, because other societies have run this experiment further.", body),
    table([
        [Paragraph("Where", th), Paragraph("The concept", th), Paragraph("How it shows up", th)],
        [Paragraph("<b>South Asia</b>", cell),
         Paragraph("<i>Log kya kahenge</i> — “what will people say”", cell),
         Paragraph("Career choices abandoned, marriages constrained by caste and community "
                   "expectation. Common enough to title plays and films.", cell)],
        [Paragraph("<b>Japan</b>", cell),
         Paragraph("<i>Sekentei</i> — standing before the watching world", cell),
         Paragraph("An invisible shared sense of what everyone will think, functioning as a moral "
                   "observer. Widely discussed domestically in relation to conformity pressure.",
                   cell)],
        [Paragraph("<b>China</b>", cell), Paragraph("<i>Mianzi</i> — face", cell),
         Paragraph("Reputation as a transactable asset, given and lost on others' behalf as well as "
                   "your own.", cell)],
        [Paragraph("<b>South Korea</b>", cell), Paragraph("Individualism score <b>18</b>", cell),
         Paragraph("More collectivist than Nigeria, in a high-income, highly institutionalised "
                   "economy. The clearest evidence that wealth does not dissolve this.", cell)],
        [Paragraph("<b>Spain &amp; Latin America</b>", cell),
         Paragraph("<i>¿Qué dirán?</i>", cell),
         Paragraph("Shame tied to family honour and reputation — notable for persisting inside a "
                   "relatively individualist culture.", cell)],
        [Paragraph("<b>Arab world &amp; Mediterranean</b>", cell),
         Paragraph("Honour–shame as an organising frame", cell),
         Paragraph("The classical reference case in the anthropological literature, and the origin "
                   "of most of the theory.", cell)],
    ], [34 * mm, 48 * mm, 88 * mm]),
    Paragraph(
        "First, <b>Spain complicates the standard story.</b> It scores as fairly individualist and "
        "still runs on <i>¿qué dirán?</i> Shame is not simply the inverse of individualism, which "
        "means the Hofstede numbers explain less than they appear to.", body),
    Paragraph(
        "Second, <b>South Korea is the natural experiment.</b> It industrialised, democratised and "
        "got rich while remaining more collectivist than most of West Africa. Anyone arguing that "
        "African societies will shed shame-based enforcement automatically as incomes rise has to "
        "explain Korea. The honest conclusion is that this changes when it is <i>deliberately</i> "
        "changed, and not otherwise.", body),
]

# ================= 12 & 13 =================
story += [
    PageBreak(),
    Paragraph("12 · What Shame Is Actually For", h2),
    Paragraph("A report that only counted costs would be dishonest, and would also be useless as a "
              "guide to changing anything. Shame persists because it does real work.", body),
]
story += bullets([
    "<b>It enforces care.</b> The obligation to house a cousin, school a nephew, feed whoever "
    "arrives. Societies with strong welfare states outsource this to the tax system. Where there is "
    "no such system, shame is the pension, the insurance and the safety net.",
    "<b>It makes agreements enforceable without courts.</b> Where contract enforcement is slow or "
    "purchasable, reputation is often the only functioning collateral.",
    "<b>It restrains behaviour that law does not reach.</b> Rudeness to elders, neglect of a parent, "
    "public cruelty. Nobody is prosecuting these anywhere.",
    "<b>Hausa <i>kunya</i> is instructive.</b> It names a virtue of restraint and propriety. The "
    "English framing of shame as pure pathology is itself a culturally specific position.",
])
story += [
    Paragraph(
        "The realistic goal is therefore not the abolition of shame, which would be neither possible "
        "nor desirable. It is <b>narrowing its target</b> — keeping the sanction pointed at choices "
        "and moving it off conditions.", body),

    Paragraph("13 · What Actually Changes It", h2),
]
story += bullets([
    "<b>Contact beats information.</b> Campaigns that explain a condition move attitudes less than "
    "knowing someone who has it and is otherwise unremarkable. The first person to speak carries the "
    "most cost and does the most good.",
    "<b>Reattributing cause does specific work.</b> Where 51% of people believe evil spirits cause "
    "epilepsy, a medical explanation moves the condition out of the moral category entirely. The "
    "same applies to naming male-factor infertility out loud.",
    "<b>Services create permission.</b> Availability changes disclosure, not only the reverse. A "
    "clinic that exists makes admitting the problem rational; where nothing exists, silence is the "
    "sensible strategy.",
    "<b>Structure beats willpower in families.</b> A nominated gatekeeper, an evidence rule, a fixed "
    "ceiling — all work by <b>replacing a shame transaction with a documented one</b>. That is the "
    "same move as a contract, at family scale.",
    "<b>Language is a lever, and it is free.</b> “She is barren” and “the couple has an untreated "
    "infection” describe the same situation and assign blame entirely differently.",
])

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("14 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First, this subject is a magnet for condescension, and we have tried to avoid earning "
        "it.</b> There is a long and ugly tradition of Western writing that treats African social "
        "norms as backwardness to be outgrown. The single most useful fact in this report is that "
        "<b>South Korea is more collectivist than Nigeria</b>. Whatever this is, it is not a "
        "developmental deficiency.", body),
    Paragraph(
        "<b>Second, the people enforcing shame are usually not villains.</b> The aunt who will not "
        "discuss her nephew's depression, the community that isolates a childless woman — they are "
        "running the operating system they were handed, in which visible deviation genuinely "
        "threatened everyone's standing. Blaming individuals for a systemic incentive is both unfair "
        "and ineffective. The incentive is what has to change.", body),
    Paragraph(
        "<b>Third, and least comfortable: some of the shame is doing something we would miss.</b> "
        "The obligation that makes remittances non-negotiable is the same obligation that keeps a "
        "grandmother fed. Loosen it and some people are freer and some people are hungrier. Anyone "
        "who tells you this trade-off does not exist is selling something — usually individualism, "
        "and usually to people who cannot afford it.", body),
    Paragraph("The goal is not a society where nobody cares what anyone thinks. It is a society "
              "where what people think is triggered by what you <i>did</i>, not by what happened to "
              "you.", pull),
]

# ================= 15 =================
story += [
    PageBreak(),
    Paragraph("15 · Method &amp; Limits", h2),
    Paragraph("This report assembles published research as at 19 August 2026 and reads it through a "
              "single frame: shame as a mechanism of social enforcement with measurable costs.", body),
]
story += bullets([
    "<b>“Africa” is doing far too much work throughout.</b> Fifty-four countries and over a thousand "
    "languages are not one culture. The evidence base is heavily weighted toward Nigeria, Ghana, "
    "Kenya, Ethiopia and South Africa, because those are the countries that publish. Francophone and "
    "Lusophone Africa are under-represented for that reason and no other.",
    "<b>Hofstede's scores are contested and should not be over-read.</b> They derive from survey "
    "work begun decades ago, originally within a single multinational employer, and assign one "
    "number to an entire country. Several African scores rest on regional estimates rather than "
    "country-specific fieldwork. Fig 3 is a rough ordering, not a ranking.",
    "<b>The guilt–shame–fear typology is not neutral.</b> It comes substantially from wartime "
    "anthropology and missionary literature, and its conventional mapping of Africa to “fear-power” "
    "carries an implicit hierarchy we reject. We present it because it clarifies a real distinction "
    "and because readers will encounter it, not because we endorse its geography.",
    "<b>Treatment gaps have multiple causes and stigma is only one.</b> The 90% and 80% figures "
    "reflect workforce shortage, cost, distance, medication supply and policy as well as shame. We "
    "show the workforce data alongside precisely so the gap is not attributed entirely to culture.",
    "<b>Correlation is not mechanism.</b> We argue that shame causes specific costs. Most of the "
    "underlying research establishes association. Causal identification in this literature is "
    "genuinely hard and we have not overstated it.",
    "<b>The African-language terms in Fig 1 are dictionary equivalents</b>, not ethnographic "
    "analysis. Each carries meaning the English word does not, and we have flagged <i>kunya</i> and "
    "<i>ìtìjú</i> specifically because both name a virtue as well as a sanction.",
    "<b>Section 10 is argument, not measurement.</b> No study measures shame among the African "
    "diaspora specifically. That section connects mechanisms documented elsewhere to accounts "
    "recorded in our previous report, which were themselves self-reported and unverifiable.",
    "<b>Nothing here is clinical advice.</b> If any of it describes your situation, the relevant "
    "professional is a doctor rather than a research report.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Hofstede cultural dimensions via Clearly Cultural and comparative summaries; WHO and UNICEF "
        "on the mental health workforce in sub-Saharan Africa; systematic reviews of mental illness "
        "stigmatisation and of barriers to mental health services in Africa; epidemiology of "
        "epilepsy in sub-Saharan Africa; pooled analysis of HIV stigma and testing across Africa; "
        "systematic review and meta-synthesis of infertility-related stigma in Africa, and "
        "infertility prevalence in sub-Saharan Africa; Global Entrepreneurship Monitor on fear of "
        "failure and Small Business Economics on failure stigma and re-entry; published work on Log "
        "Kya Kahenge and on shame socialisation in Japan. Full inline links in the web edition.",
        small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/economics-of-shame-2026<br/>"
        "Companion reports: You Sent the Money. Did You Buy Anything? · How Long Until It Was Worth "
        "It?<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
