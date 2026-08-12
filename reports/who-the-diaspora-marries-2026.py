#!/usr/bin/env python3
"""Generate the AGF report PDF: Who the Diaspora Actually Marries (2026)."""

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
IMG = os.path.join(HERE, "who-the-diaspora-marries-2026", "img")
OUT = os.path.join(HERE, "who-the-diaspora-marries-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "Who the Diaspora Marries · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 12 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="Who the Diaspora Actually Marries (2026)",
                      author="Africa Global Forum",
                      subject="Intermarriage among Africans who moved abroad to study or work")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])

story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("Who the Diaspora Marries", h1),
    Paragraph("Intermarriage among Africans who moved abroad to study or work",
              S("sub", fontName="Helvetica-Oblique", fontSize=15, leading=19,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "What the data actually shows, why the patterns exist, and why the most common explanation "
        "for them is wrong.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("24% / 12%", big_num), Paragraph("46%", big_num),
    Paragraph("8 yrs", big_num), Paragraph("10.1%", big_num),
], [
    Paragraph("intermarriage, Black men<br/>vs Black women (US)", big_lbl),
    Paragraph("of African immigrants hold<br/>a degree — and still rarely<br/>marry out", big_lbl),
    Paragraph("until the study and work<br/>routes converge", big_lbl),
    Paragraph("of England &amp; Wales households<br/>are mixed-ethnicity", big_lbl),
]], colWidths=[CONTENT_W / 4] * 4)
kpi.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), INK),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 14),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story += [kpi, Spacer(1, 6 * mm)]
story += [fig("gender_gap.png",
              "Intermarriage among recently married Black adults in the US, by gender "
              "(Pew Research Center). The most stable finding in the field.", max_w=150 * mm)]
story += [Paragraph(
    "Published August 2026 by Africa Global Forum · "
    "africaglobalforum.com/reports/who-the-diaspora-marries-2026", small), PageBreak()]

# ================= 01 =================
story += [
    Paragraph("01 · Executive Summary", h2),
    Paragraph(
        "Few subjects in diaspora life generate more conversation and less evidence than who people marry. "
        "The talk runs in two directions, both of them loaded: intermarriage as proof of arrival, or "
        "intermarriage as a kind of leaving. Neither framing survives contact with the data.", body),
]
story += bullets([
    "<b>Intermarriage is roughly twice as common for Black men as for Black women.</b> Among recently "
    "married Black adults in the US, about <b>24% of men and 12% of women</b> have a spouse of a different "
    "race or ethnicity. This is the single largest and most persistent pattern in the field.",
    "<b>African immigrants break the standard model.</b> They are among the most educated migrant groups "
    "anywhere — and, despite that, research finds they have <i>extremely low</i> rates of marriage with "
    "white partners. The usual assumption that education drives intermarriage does not hold here.",
    "<b>When Africans abroad marry outside their own national group, they are more likely to marry African "
    "Americans or other Black populations than white partners.</b>",
    "<b>Intermarriage rises reliably with generation</b> — lowest for the first generation, intermediate "
    "for their children, highest for the generation after. This holds for virtually every migrant group "
    "ever studied.",
    "<b>Arriving to study and arriving to work produce different timelines.</b> Student migrants delay "
    "partnership and children; labour migrants are more likely to arrive already partnered. <b>The two "
    "converge after about eight years.</b>",
    "<b>In England and Wales, mixed-ethnicity households reached 10.1% by the 2021 Census</b>, and the "
    "Mixed White &amp; Black African population stands at about 250,000.",
])
story += [Paragraph(
    "The strongest predictor of who you marry is not your values, your education, or your loyalty to "
    "home. It is who is standing in the room during the years you are looking.", pull)]

# ================= 02 =================
story += [
    Paragraph("02 · What We Are Measuring", h2),
    Paragraph(
        "Three different things get called “interracial marriage” in diaspora conversation, and they "
        "behave differently. <b>Interracial</b> — marrying across a racial boundary, which is what most of "
        "the US data measures. <b>Inter-ethnic</b> — marrying across an ethnic or national line within the "
        "same broad racial group: a Nigerian and a Ghanaian, a Somali and an African American. "
        "Statistically invisible in most datasets, socially enormous in real families. And "
        "<b>cross-border</b> — marrying someone who lives in another country, which is primarily an "
        "immigration question and the subject of a separate report, <i>Marrying Across Borders</i>. This "
        "report is mostly about the first two, because they are what the migration data captures.", body),
    Paragraph(
        "<b>A note on how to read it.</b> Nothing here is an argument about who anyone should marry. "
        "Intermarriage is not a score. It is not evidence of integration succeeding or of culture being "
        "abandoned — both readings are common in diaspora discussion and neither is supported by what "
        "follows. These are population-level patterns, and population-level patterns say nothing about any "
        "individual couple.", body),
]

# ================= 03 =================
story += [
    PageBreak(),
    Paragraph("03 · The Baseline", h2),
    fig("trend.png",
        "Fig 1 — Share of US newlyweds married to someone of a different race or ethnicity "
        "(Pew Research Center). 1967 is the year the US Supreme Court struck down bans on interracial "
        "marriage in Loving v. Virginia."),
    Paragraph(
        "In 1967, when interracial marriage was still illegal in parts of the United States, <b>3% of "
        "newlyweds</b> married across racial lines. By 2015 it was <b>17%</b> — more than a fivefold "
        "increase within a single lifetime. Among Black newlyweds specifically the rate <b>more than "
        "tripled, from 5% in 1980 to 18% in 2015</b>. That is the backdrop against which every diaspora "
        "conversation about this happens: a society-wide shift, moving fast, in one direction. What follows "
        "is about where Africans abroad sit inside it — and the answer is not where you would guess.", body),

    Paragraph("04 · The Gender Gap", h2),
    Paragraph(
        "<b>24% of recently married Black men, against 12% of recently married Black women</b> (see cover "
        "chart). Exactly double. The gap is one of the most stable findings in the whole literature, and it "
        "is far wider for Black Americans than for most other groups.", body),
    Paragraph(
        "It is worth being careful about what this does and does not mean. A gap in rates is not a "
        "statement about desirability, standards or loyalty — the explanations that circulate most freely "
        "in diaspora group chats. Demographers point instead to a set of structural factors: differences in "
        "where men and women work and study, sex ratios within local marriage markets, differences in "
        "educational sorting, and the simple fact that men and women in the same community often move "
        "through different social spaces.", body),
    Paragraph(
        "A gender gap in a population statistic is a description of a market, not a verdict on anybody "
        "in it.", pull),
]

# ================= 05 =================
story += [
    Paragraph("05 · The African Exception", h2),
    Paragraph(
        "Here is the finding this report exists for, and it cuts directly against the standard model of "
        "immigrant integration. The conventional theory says intermarriage follows education and time: the "
        "more educated an immigrant group, and the longer it has been settled, the more it marries into the "
        "majority. African immigrants satisfy the first condition emphatically — <b>46% of sub-Saharan "
        "African immigrants in the US hold a bachelor's degree or higher, about 61% for Nigerian-born "
        "immigrants</b> — well above both the foreign-born and US-born averages.", body),
    Paragraph(
        "And yet research on Black populations in the United States finds that <b>despite exceptionally "
        "high levels of education among Black African immigrants, they have extremely low rates of marriage "
        "with white partners</b> (Cornell University). Two further findings sharpen it.", body),
]
story += bullets([
    "<b>African immigrants are more likely to partner with African Americans than with white Americans.</b> "
    "When marriage happens outside the national-origin group, it happens most often within the broader "
    "Black population.",
    "<b>Marriage between different Black populations remains low.</b> Unions between African immigrants and "
    "African Americans, or between African and West Indian communities, occur at low rates — researchers "
    "describe the social distance between these groups as substantial. The diaspora is not one marriage "
    "market. It is several, sitting next to each other.",
])
story += [Paragraph(
    "That second point is the one that tends to surprise people most, because it contradicts the "
    "assumption that shared heritage produces shared social life. It often does not — not at the scale of "
    "marriage.", body)]

# ================= 06 =================
story += [
    Paragraph("06 · The Education Effect", h2),
    fig("education.png",
        "Fig 2 — Intermarriage among Black newlyweds by education level (Pew Research Center)."),
    Paragraph(
        "Education does raise intermarriage — <b>21% for those with a bachelor's degree or more, against "
        "15% for those with a high school diploma or less</b> — but look at the size of the effect. Six "
        "percentage points across the entire education range. Set that against the gender gap on the cover, "
        "which is twelve points. <b>Being a man matters roughly twice as much as having a degree.</b> And "
        "set it against the African immigrant finding in Section 05, where a group with extraordinarily "
        "high education shows very low intermarriage.", body),
    Paragraph(
        "The conclusion is that education is a weak lever here. What a degree actually does is change "
        "<i>which rooms you are in</i> — and if those rooms are full of people from your own community, as "
        "they often are for African graduates who studied together and work in the same sectors, high "
        "education produces no increase in intermarriage at all.", body),
]

# ================= 07 =================
story += [
    PageBreak(),
    Paragraph("07 · The Generation Ladder", h2),
    fig("generation.png",
        "Fig 3 — The generational pattern (Migration Policy Institute). Bar heights are illustrative "
        "— the direction is the measured finding; no published rate exists for African migrants "
        "specifically by generation."),
    Paragraph(
        "For virtually every racial and ethnic group ever studied, <b>intermarriage rates rise with each "
        "generation</b>: lowest among new immigrants, intermediate among the native-born children of "
        "foreign-born parents, highest among the third generation.", body),
    Paragraph(
        "This is the most reliable regularity in the field, and it reframes the whole question for anyone "
        "in the diaspora. <b>The generation that moved is, statistically, the generation least likely to "
        "marry out.</b> If you arrived as a student or a worker, you are at the bottom of the ladder — and "
        "the pattern predicts that your children will be somewhere in the middle and your grandchildren "
        "near the top.", body),
    Paragraph(
        "That is not a warning and it is not a target. It is what happens when each successive generation "
        "is born further inside a society's schools, workplaces and friendship networks. Every diaspora "
        "community in history has walked up this ladder. Knowing the shape of it is more useful than being "
        "surprised by it in twenty years.", body),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · The UK Picture", h2),
    fig("uk_picture.png",
        "Fig 4 — UK inter-ethnic partnering and mixed populations (ONS 2011 Census analysis; 2021 "
        "Census). The two measures differ — couples in 2011, households in 2021 — so the pair shows "
        "direction, not a clean like-for-like change."),
    Paragraph(
        "Inter-ethnic partnerships were <b>9% of couples in England and Wales at the 2011 Census, up from "
        "7% in 2001</b>, and by 2021 mixed-ethnicity households were <b>10.1%</b> of all households.", body),
    Paragraph(
        "The right-hand panel carries the more interesting comparison. <b>The Mixed White &amp; Black "
        "Caribbean population is roughly double the Mixed White &amp; Black African population</b> — "
        "513,000 against 250,000 — even though the Black African population in Britain is now larger than "
        "the Black Caribbean one. The explanation is time, not preference. Caribbean migration to Britain "
        "began in earnest in the late 1940s; large-scale African migration is mostly a phenomenon of the "
        "1990s onwards. <b>Britain's Black African communities are, on this measure, where its Caribbean "
        "communities were a generation or two ago</b> — and both Mixed categories have more than doubled "
        "since they were first counted in 2001.", body),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("09 · Study vs Work", h2),
    Paragraph(
        "The research does distinguish the two routes people take — not in <i>who</i> people marry, but in "
        "<i>when</i>.", body),
    fig("channel.png",
        "Fig 5 — Family formation by migration channel (European Journal of Population). The "
        "convergence by year eight is the measured finding; the curve shape is illustrative."),
    Paragraph(
        "<b>Labour migrants are more likely to arrive already partnered</b>, or to have a spouse abroad "
        "awaiting reunification. <b>Student migrants delay</b>: they stay in education longer, experience a "
        "steeper income climb, and are less likely to be married or to have children in their early years "
        "abroad. But the gap does not last — <b>the differences between the two groups become minimal after "
        "about eight years</b> in the country.", body),
    Paragraph("Why this matters for partner choice, even though the research does not measure it "
              "directly:", body),
]
story += bullets([
    "<b>The student route puts you in the most mixed environment of your life at exactly the age most "
    "people partner.</b> A university is a dense, age-matched, diverse social market. If intermarriage is "
    "going to happen, this is structurally the likeliest moment.",
    "<b>The work route often does the opposite.</b> Arriving at 30 into a job, a commute and a small "
    "professional circle is a far narrower social market — and if you arrive already partnered, the "
    "question is settled before you land.",
    "<b>Timing compounds with the visa.</b> Post-study work windows run 12 to 36 months. Those are the "
    "years when a student-route migrant is deciding both where to live and who to live with, often under "
    "time pressure. The immigration clock and the relationship clock run together, and people rarely plan "
    "for that.",
])

# ================= 10 =================
story += [
    Paragraph("10 · Why These Patterns Exist", h2),
    Paragraph("Five structural explanations do most of the work. None of them is about anyone's "
              "character.", body),
]
story += bullets([
    "<b>Who is in the room.</b> Demographers call it the marriage market: you can only partner with people "
    "you actually encounter. African migrants often arrive into dense co-ethnic networks — the same church, "
    "the same student association, the same hospital ward, the same city district. High education does not "
    "widen that circle if the education happened alongside the same people.",
    "<b>Group size and concentration.</b> Larger, more geographically concentrated communities intermarry "
    "less, everywhere, for every group. A Nigerian in Houston or a Somali in Minneapolis has a large local "
    "marriage market of their own; a Malawian in a small European city may have almost none.",
    "<b>Age at arrival.</b> Arriving at 19 to study and arriving at 33 for work place you at completely "
    "different points in your own partnering life. This is probably the single biggest difference between "
    "the two routes.",
    "<b>Family expectation, and how far it reaches.</b> Parental preference is a documented influence on "
    "partner choice across migrant communities in Europe. Its force declines with distance and generation — "
    "which is part of why the generation ladder exists.",
    "<b>Religion, which is frequently the real boundary.</b> Much of what gets discussed as a racial "
    "boundary is in practice a religious one. A Muslim Senegalese and a Catholic Congolese may face more "
    "family resistance than either would in marrying a co-religionist of another race entirely.",
])
story += [Paragraph(
    "Almost every pattern in this report is explained by geography, timing and group size — not by "
    "preference. Which means the patterns change when your circumstances change, and not before.", pull)]

# ================= 11 =================
story += [
    Paragraph("11 · What This Means", h2),
]
story += bullets([
    "<b>Stop reading population statistics as personal verdicts.</b> The 24%/12% gap describes a market of "
    "millions. It says nothing about any individual's worth, standards or choices, and it is routinely "
    "deployed in diaspora discourse as though it did.",
    "<b>If you want a partner from your own community, understand that it takes deliberate effort "
    "abroad.</b> Co-ethnic marriage is the statistical norm for first-generation migrants precisely because "
    "they live inside co-ethnic networks. If your work and neighbourhood do not supply that, no amount of "
    "preference will — you have to build the network.",
    "<b>Expect the generational shift, and decide now what you want to transmit.</b> The generation ladder "
    "is close to a law of migration. Families who plan for it — language, visits home, food, faith, naming, "
    "honest conversation — transmit more of what they care about than families who are surprised by it.",
    "<b>If you are on the student route, know that your social market is at its widest right now.</b> "
    "Whatever you want — a partner from home, from the diaspora, or from anywhere — university years are "
    "when the room is most open. It narrows considerably afterwards.",
    "<b>Do not confuse the intermarriage question with the immigration question.</b> Marrying across a "
    "border is a visa problem with published costs and timelines. Marrying across a race or ethnicity is a "
    "social question with no paperwork attached. They get discussed together and they have almost nothing "
    "in common.",
    "<b>The African–African American distance is worth naming.</b> The low rate of marriage between African "
    "immigrants and African Americans is one of the quieter findings here, and it points at a real social "
    "gap between communities that outsiders assume are one. Closing it is a matter of actual contact, not "
    "shared category.",
])

# ================= 12 =================
story += [
    Paragraph("12 · Method &amp; Limits", h2),
    Paragraph(
        "<b>What this report is:</b> a synthesis of published demographic research on intermarriage, read "
        "specifically for Africans who moved abroad to study or work. Data as at 12 August 2026. "
        "<b>Significant limits, and there are more than usual here:</b>", body),
]
story += bullets([
    "<b>The headline US figures are for Black newlyweds overall, not African immigrants.</b> Pew's "
    "intermarriage series does not break out African-born respondents. We use it as the baseline and flag "
    "every point where African immigrants are known to diverge from it — which is a lot.",
    "<b>The African-specific findings are qualitative in the sources.</b> The research establishes that "
    "African immigrants have very low intermarriage with white partners despite high education, but "
    "published percentage rates for African-born migrants by year are not available. We have quoted the "
    "direction and declined to invent numbers.",
    "<b>Figures 3 and 5 have illustrative heights and curves.</b> The generational direction and the "
    "eight-year convergence are the measured findings; the shapes are drawn to communicate them.",
    "<b>The Pew reference year is 2015.</b> It remains the most-cited comparable series, but intermarriage "
    "has continued to rise since, so these figures are likely conservative.",
    "<b>UK figures mix two measures</b> — inter-ethnic couples in 2011 and mixed-ethnicity households in "
    "2021. They show direction, not a like-for-like change.",
    "<b>Almost all usable data is US and UK.</b> France, Germany, Canada, the Gulf and intra-African "
    "contexts are barely covered here, and French statistics in particular do not record ethnicity by law. "
    "This is an anglophone-skewed picture of a global population.",
    "<b>Marriage is not partnership.</b> These series count marriages. Cohabitation patterns differ, and in "
    "several countries a majority of couples under 35 are not married at all.",
    "<b>No causal claims.</b> Nothing here establishes that any factor causes any outcome. These are "
    "associations in population data.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Pew Research Center, Intermarriage in the U.S. 50 Years After Loving v. Virginia; Pew, statistical "
        "portrait of the US Black immigrant population; Cornell University on interracial marriage and "
        "cohabitation among America's diverse Black populations; Migration Policy Institute on "
        "second-generation intermarriage; Intermarriage among New Immigrants in the USA; ONS on "
        "inter-ethnic relationships and the 2021 Census; European Journal of Population on migration motive "
        "and family trajectories. Full inline links in the web edition.", small),
    Spacer(1, 6 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=8),
]
story += [callout(
    "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit together, "
    "and bounce ideas. This research is part of an open library, free to read and share. The Forum itself "
    "is by application.<br/><br/>"
    "Read the web edition with live source links: "
    "africaglobalforum.com/reports/who-the-diaspora-marries-2026<br/>"
    "Companion reports: Marrying Across Borders · The Diaspora, Counted<br/>"
    "Apply to join: africaglobalforum.com", bg=INK)]

doc.build(story)
print("wrote", OUT)
