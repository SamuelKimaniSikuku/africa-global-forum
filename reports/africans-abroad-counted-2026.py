#!/usr/bin/env python3
"""Generate the AGF report PDF: More Africans Move to Africa Than Leave It (2026)."""

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
IMG = os.path.join(HERE, "africans-abroad-counted-2026", "img")
OUT = os.path.join(HERE, "africans-abroad-counted-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Diaspora, Counted · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 11 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="More Africans Move to Africa Than Leave It (2026)",
                      author="Africa Global Forum",
                      subject="How many Africans live outside the continent, what they do, and how long they stay")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])

story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Diaspora, Counted", h1),
    Paragraph("More Africans move to Africa than leave it",
              S("sub", fontName="Helvetica-Oblique", fontSize=17, leading=21,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "How many Africans actually live outside the continent, where they are, how many are working "
        "and how many are studying, why they went — and the question nobody asks until it is too late: "
        "<b>how long do they stay?</b>", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("20.7m", big_num), Paragraph("~500k", big_num),
    Paragraph("41.4%", big_num), Paragraph("20–50%", big_num),
], [
    Paragraph("Africans living outside<br/>the continent", big_lbl),
    Paragraph("African students<br/>studying abroad each year", big_lbl),
    Paragraph("of non-EU citizens work<br/>below their qualification", big_lbl),
    Paragraph("of all immigrants leave<br/>within five years", big_lbl),
]], colWidths=[CONTENT_W / 4] * 4)
kpi.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), INK),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 14),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story += [kpi, Spacer(1, 6 * mm)]
story += [fig("inside_outside.png",
              "African migrants by destination type, 2024 (UN DESA International Migrant Stock 2024). "
              "Intra-African movement is the larger flow, by 21%.")]
story += [Paragraph(
    "Published August 2026 by Africa Global Forum · "
    "africaglobalforum.com/reports/africans-abroad-counted-2026", small), PageBreak()]

# ================= 01 =================
story += [
    Paragraph("01 · Executive Summary", h2),
    Paragraph(
        "The African diaspora is discussed constantly and counted rarely. When it is counted, the numbers "
        "usually arrive without the two things that make them useful: <i>what these people are actually "
        "doing</i>, and <i>how long they stay</i>. Here is the picture the data supports.", body),
]
story += bullets([
    "<b>20.7 million Africans live outside the continent</b> — but <b>25 million moved to another African "
    "country</b>. Intra-African migration is 21% larger than the exodus everyone writes about.",
    "<b>Europe holds about 11 million, Asia including the Gulf about 6.9 million, and Northern America "
    "about 2.7 million.</b> The Gulf is a far bigger destination than the popular narrative allows, and "
    "North America a far smaller one.",
    "<b>Roughly half a million African students study abroad each year.</b> France is the largest single "
    "host, followed by China — not the United States, and not the United Kingdom.",
    "<b>46% of sub-Saharan African immigrants in the US hold a bachelor's degree or higher</b>, against "
    "about 31% of all foreign-born adults. For Nigerian-born immigrants it is roughly <b>61%</b>.",
    "<b>And 41.4% of non-EU citizens in the EU work below the level they are qualified for.</b> The same "
    "population, the same year. That is the central finding of this report.",
    "<b>Between 20% and 50% of all immigrants leave within five years</b> — 75% in the Netherlands, 67% in "
    "Germany, but only 15% in the United States. Where you move decides how likely you are to stay, more "
    "than why you moved.",
])
story += [Paragraph(
    "The diaspora is not a permanent population that occasionally goes home. It is a revolving door, and "
    "the door turns at completely different speeds depending on which country you walked into.", pull)]

# ================= 02 =================
story += [
    Paragraph("02 · The Headline Count", h2),
    Paragraph(
        "Almost every conversation about African migration starts in the wrong place. <b>25 million Africans "
        "live in an African country other than the one they were born in. 20.7 million live outside the "
        "continent altogether.</b> Intra-African movement is the larger flow, by 21%.", body),
    Paragraph(
        "This matters for the diaspora specifically, and not only as a corrective. It means the person who "
        "moved from Zimbabwe to South Africa, from Burkina Faso to Côte d'Ivoire, or from Somalia to Kenya "
        "is having a migration experience that is numerically <i>more typical</i> than the one had by the "
        "person in London or Houston. Most African migration is regional, driven by work and proximity, and "
        "largely invisible to the media framing of “the African diaspora”.", body),
    Paragraph(
        "It also puts the 20.7 million in proportion. Against a continental population well above 1.4 "
        "billion, <b>the Africans who have left the continent are on the order of 1.5% of all Africans.</b> "
        "The diaspora is enormously influential — it sends home more money than foreign investment and aid "
        "combined — but it is a small, self-selected slice of the continent, and its experience should not "
        "be mistaken for the general one.", body),
]

# ================= 03 =================
story += [
    Paragraph("03 · Where They Actually Are", h2),
    fig("where_they_are.png",
        "Fig 2 — Where Africans living outside the continent reside, 2024 (UN DESA). "
        "Percentages are of the 20.7m total.", max_w=135 * mm),
    Paragraph(
        "<b>Europe dominates, and it is not close.</b> Eleven million — more than half of all Africans "
        "outside the continent. The Mediterranean corridor, the French and British colonial ties, and the "
        "sheer proximity of North Africa to southern Europe make this the default destination in a way "
        "North America has never been.", body),
    Paragraph(
        "<b>Asia is the second-largest destination, mostly meaning the Gulf.</b> Nearly 7 million — two and "
        "a half times the North American figure. This population is largely invisible in diaspora "
        "conversation, partly because Gulf migration is structurally different: as <i>The Visa Treadmill</i> "
        "found, Saudi Arabia, Kuwait and the UAE offer <i>no realistic citizenship pathway at all</i>. "
        "Millions of Africans are living long-term in countries where permanent belonging is not on offer at "
        "any price. That is a different kind of diaspora, and it deserves more attention than it gets.", body),
    Paragraph(
        "<b>Northern America is smaller than almost anyone assumes.</b> 2.7 million, about 13%. It looms far "
        "larger in the imagination than in the count — a function of American cultural reach, the visibility "
        "of Nigerian and Ghanaian professional communities, and the fact that a disproportionate share of "
        "diaspora media is produced there.", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · The Students", h2),
    Paragraph(
        "Roughly <b>half a million African students were studying abroad annually</b> as of the last full "
        "pre-pandemic count, and the figure has climbed since. Against a global total of around seven "
        "million internationally mobile students by 2024, Africa is a significant and fast-growing share.", body),
    fig("study_destinations.png",
        "Fig 3 — Leading single destinations for African students (Carnegie Endowment, 2020 reference "
        "year). Counts across countries are not perfectly comparable — see Method."),
    Paragraph(
        "<b>France is the largest single destination</b> — roughly 126,000 African students — and the reason "
        "is structural rather than competitive: language, near-free public university tuition, and dense "
        "existing family networks across francophone West and North Africa.", body),
    Paragraph(
        "<b>China is second, at around 81,500</b>, and this is the number that surprises people. China built "
        "that position deliberately over two decades through scholarship diplomacy tied to infrastructure "
        "and trade relationships. It is now a larger host of African students than the United States. "
        "<b>The United States sits third at about 48,000</b> — a fraction of France's intake, despite "
        "hosting the world's largest international student population overall.", body),
    Paragraph(
        "The UK, Canada, Germany, Türkiye and the UAE are all significant and, in several cases, growing "
        "faster than the leaders. Canada and the UK saw extraordinary growth in African enrolments between "
        "2021 and 2023 — and both have since tightened, which is reshaping where the next cohort goes.", body),
    Paragraph(
        "The student flow is the front end of the diaspora pipeline. Where students go this decade "
        "determines where the workers, taxpayers and remitters are in the next one.", pull),
]

# ================= 05 =================
story += [
    Paragraph("05 · The Workers", h2),
    Paragraph(
        "Most Africans outside the continent are there to work, and the labour-market data tells a "
        "consistent story across destinations: <b>they participate heavily, and they are paid less than "
        "comparable native-born workers.</b> The OECD's 2025 finding is the clearest single number: "
        "<b>immigrants entering the labour market earn 34% less than native-born workers of the same age and "
        "sex.</b> Two-thirds of that gap is not discrimination in the direct sense — it is composition. "
        "Immigrants are concentrated in lower-paying sectors and lower-paying firms.", body),
    Paragraph(
        "That distinction matters enormously for what you do about it. If the gap were purely prejudice, the "
        "answer would be legal. Because it is largely <i>which firm and which sector you land in</i>, the "
        "answer is strategic: the first job you accept abroad has effects that compound for a decade, "
        "because moving up between firms and sectors is what closes the gap.", body),

    PageBreak(),
    Paragraph("06 · The Qualification Paradox", h2),
    fig("education.png",
        "Fig 4 — Educational attainment (Migration Policy Institute; Pew Research Center). Other "
        "analyses put the sub-Saharan African figure at 42% — the range is 42–46%."),
    Paragraph(
        "Africans who leave the continent are not the continent's average. They are, by a wide margin, among "
        "the most educated migrant populations anywhere. <b>46% of sub-Saharan African immigrants in the US "
        "hold a bachelor's degree or higher, against about 31% of all foreign-born adults. For Nigerian-born "
        "immigrants the figure is about 61%</b> — nearly double the US-born rate. Now set that beside the "
        "European labour data.", body),
    fig("paradox.png",
        "Fig 5 — The qualification paradox (MPI; Eurostat). The two figures describe different regions "
        "and cannot be summed — but they describe the same phenomenon.", max_w=155 * mm),
    Paragraph(
        "<b>41.4% of non-EU citizens in the EU are over-qualified for the job they hold</b> — the highest of "
        "any group, and highest of all among non-EU-born women. The rate has improved slowly, from 45.9% in "
        "2014 to 39.6% in 2024 for the non-EU-born, but it remains the defining feature of migrant "
        "employment in Europe.", body),
    Paragraph(
        "Africa is not losing its least employable people. It is losing its doctors, engineers and graduates "
        "— and then watching a large share of them drive taxis, stack shelves and staff care homes in "
        "countries that will not recognise their qualifications.", pull),
    Paragraph(
        "This is the real cost of migration, and it is paid twice. Africa loses the training investment. The "
        "migrant loses the career. The destination country gains a worker but not the skill it was trained "
        "for. Everybody involved is worse off than they would be under a functioning credential-recognition "
        "system — which is why that, and not visa policy, is arguably the highest-leverage reform "
        "available.", body),
]

# ================= 07 =================
story += [
    Paragraph("07 · Why They Went", h2),
    Paragraph("The data above explains a great deal about <i>who</i> leaves. Four structural forces explain "
              "<i>why</i>.", body),
]
story += bullets([
    "<b>The wage gap is the engine, and it is enormous.</b> Even earning 34% less than a native-born peer, "
    "an African professional in Europe or North America typically earns a multiple of what the same work "
    "pays at home, in a currency that does not depreciate. That single arithmetic fact outweighs almost "
    "every deterrent policy governments design.",
    "<b>Education is a route, not just a goal.</b> Half a million students a year are not only buying "
    "degrees — they are buying legal presence, a post-study work window, and a path to residence. The "
    "countries that shorten that window, as the UK is doing in January 2027, are changing the migration "
    "decision itself.",
    "<b>Networks compound.</b> Migration follows migration. France hosts the most African students because "
    "it already hosts the most African families; Gulf recruitment runs on established agency corridors. "
    "This is why flows are so persistent even when policy tightens.",
    "<b>Credential markets pull specific professions.</b> Health systems in the UK, US, Canada and the Gulf "
    "actively recruit African nurses and doctors. This is not incidental migration; it is targeted "
    "acquisition of skills that African health systems paid to produce.",
])
story += [Paragraph(
    "Note what is <i>not</i> on that list as a primary driver: desperation. The most-educated-migrants "
    "finding is decisive here. Leaving the continent requires a passport, a visa fee, an airfare, a "
    "qualification and usually a network — a package the poorest simply do not have. <b>Emigration out of "
    "Africa is overwhelmingly a middle-class act.</b> The people with the fewest options move within the "
    "continent, or do not move at all.", body)]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · How Long They Stay", h2),
    Paragraph(
        "This is the least-discussed number in migration and probably the most consequential for anyone "
        "planning a life.", body),
    fig("exit_rates.png",
        "Fig 6 — Five-year exit rates by destination (OECD). European figures are for the 2010–14 "
        "arrival cohort; US and Canada for 2010–19. “Exit” includes both returning home and moving on to a "
        "third country."),
    Paragraph(
        "Across the OECD, <b>between 20% and 50% of all immigrants leave within five years of arriving</b>. "
        "But the spread between destinations is the story. <b>Three quarters of arrivals in the Netherlands "
        "are gone within five years. Two thirds in Germany. Half across Europe on average.</b> Against that, "
        "<b>the United States loses only about 15%</b> and Canada about 21%. A move to Amsterdam and a move "
        "to Toronto are not the same decision with a different postcode — they have fundamentally different "
        "half-lives.", body),
    Paragraph(
        "Why the gap? European mobility is easier — onward movement within the EU is frictionless for many "
        "permit-holders, so “exit” often means moving to another European country rather than going home. "
        "Distance and cost matter too: transatlantic return is a bigger, more final decision than a flight "
        "within Europe. And settlement-oriented systems like Canada's are explicitly designed to convert "
        "arrivals into permanent residents.", body),
    Paragraph(
        "<b>One counter-intuitive finding worth sitting with:</b> the OECD notes that migrants who arrive "
        "for <i>family or humanitarian</i> reasons return at <i>lower</i> rates than economic migrants. The "
        "people who came for work are the ones most likely to leave. The people who came for love or for "
        "safety stay. Whatever brought you is a weaker predictor of permanence than whatever roots you.", body),
    Paragraph(
        "If you are choosing a destination, you are choosing a probability of still being there in five "
        "years. That probability ranges from 25% to 85% depending on the country — and almost nobody factors "
        "it in.", pull),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("09 · The Ten-Year Clock", h2),
    Paragraph("For those who stay, the years do real work — but they work slowly, and they never quite "
              "finish.", body),
    fig("earnings_clock.png",
        "Fig 7 — The immigrant earnings gap over time (OECD International Migration Outlook 2025). "
        "Intermediate years interpolated between the published five- and ten-year points."),
    Paragraph(
        "The pay gap starts at <b>34%</b>. It closes by about a third in the first five years, and by about "
        "half in the first ten. So after a decade of work in a new country, the typical immigrant still "
        "earns roughly <b>17% less</b> than a native-born worker of the same age and sex. The mechanism is "
        "documented and it is actionable: the gap narrows mainly because immigrants <i>move to higher-paying "
        "firms and sectors</i>. It does not narrow because employers gradually decide to pay you fairly. It "
        "narrows because you leave.", body),
    Paragraph("Put the three timeframes together and the shape of a diaspora life emerges from the data:", body),
]
story += bullets([
    "<b>Years 0–5:</b> the highest-risk window. Between a fifth and three quarters of arrivals leave. "
    "Earnings are at their worst relative to local peers. Qualifications are least likely to be recognised.",
    "<b>Years 5–10:</b> the sorting window. Those who stay move firms and sectors, and the gap closes "
    "fastest. This is also when most settlement clocks mature — five years to permanent residence in "
    "Germany, Ireland, France and the Netherlands.",
    "<b>Year 10 and beyond:</b> a durable residual gap of around 17%, and the beginning of the "
    "second-generation question, which is a different report.",
])

# ================= 10 =================
story += [
    Paragraph("10 · What the Numbers Miss", h2),
    Paragraph("Every figure above counts the <i>foreign-born</i>. That single methodological choice hides a "
              "great deal.", body),
]
story += bullets([
    "<b>The second generation is invisible.</b> Children born abroad to African parents do not appear in "
    "migrant-stock data at all. The lived African diaspora is substantially larger than 20.7 million.",
    "<b>The historic diaspora is excluded entirely.</b> The descendants of the transatlantic slave trade, "
    "tens of millions of people, are not migrants and appear nowhere in these statistics.",
    "<b>Irregular migrants are undercounted</b> by design, in every country, in every dataset.",
    "<b>Naturalised citizens may drop out</b> of some national statistics once they acquire citizenship, "
    "depending on whether the country counts by birthplace or by nationality.",
    "<b>Students are counted inconsistently</b> — some countries include them in migrant stock, others do "
    "not, and enrolment counts lag by years.",
])

# ================= 11 =================
story += [
    PageBreak(),
    Paragraph("11 · What This Means For You", h2),
]
story += bullets([
    "<b>Choose your destination for its five-year retention, not its brochure.</b> If your intention is to "
    "settle, the difference between a country where 15% leave and one where 75% leave is the single largest "
    "variable in this report. Settlement-oriented systems — Canada, the US, France — hold people. "
    "Frictionless-mobility systems churn them.",
    "<b>Treat the first job as a ten-year decision.</b> Two-thirds of the earnings gap is which sector and "
    "which firm you land in. Taking the fastest available job is rational in month one and expensive by "
    "year five.",
    "<b>Convert your qualification before you need to.</b> The 41.4% over-qualification rate is the biggest "
    "destroyer of value in the whole diaspora experience. Credential conversion is slow, expensive and "
    "boring — and it is the highest-return administrative act available to you.",
    "<b>If you are advising someone at home, price the regional option honestly.</b> Twenty-five million "
    "people moved within Africa. For many trades and professions, Kigali, Nairobi, Accra or Johannesburg "
    "offers a better real outcome than a European care home.",
    "<b>Know that leaving is normal.</b> Half of arrivals in Europe are gone within five years. If you are "
    "considering returning, you are not failing at migration. You are doing the statistically ordinary "
    "thing, and the data says nothing about whether it is right for you.",
    "<b>The Gulf population deserves your attention.</b> Nearly 7 million Africans live in Asia, largely in "
    "states offering no path to permanence. If your organising, advocacy or business thinks “diaspora” "
    "means London and Atlanta, you are missing a third of the people.",
])

# ================= 12 =================
story += [
    Paragraph("12 · Method &amp; Limits", h2),
    Paragraph("<b>What this report is:</b> a demographic portrait assembled from official migration "
              "statistics, published as at 11 August 2026.", body),
]
story += bullets([
    "<b>Migrant-stock figures count the foreign-born or foreign-national population</b>, not the ethnic or "
    "heritage diaspora. This excludes second generations and the historic diaspora entirely.",
    "<b>Student counts are not perfectly comparable across countries.</b> The France, China and US figures "
    "come from a single comparative analysis using a 2020 reference year; national systems define and count "
    "international students differently. Treat Fig 3 as a ranking, not a precise census.",
    "<b>The education figures are US-specific</b> and should not be read as describing African migrants in "
    "Europe or the Gulf. Sources put the sub-Saharan figure at 42–46%; we use 46% and state the range.",
    "<b>The over-qualification figure covers non-EU citizens</b>, not Africans specifically — no equivalent "
    "Africa-only series is published. It is directionally right for African migrants and is not a "
    "measurement of them alone.",
    "<b>Exit rates cover all immigrants, not African migrants specifically</b>, and cohorts differ. “Exit” "
    "conflates returning home with onward movement to a third country, which matters in Europe.",
    "<b>The earnings-gap curve interpolates</b> between the OECD's published entry, five-year and ten-year "
    "points. The intermediate years are drawn, not measured.",
    "<b>Gulf figures are the weakest here.</b> Several GCC states publish limited migration data, so the "
    "Asia total is more uncertain than the European or North American ones.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "UN DESA International Migrant Stock 2024; IOM World Migration Report 2026; OECD International "
        "Migration Outlook 2025; OECD, Sustainable Reintegration of Returning Migrants; Eurostat migrant "
        "integration statistics; Migration Policy Institute; Pew Research Center; Carnegie Endowment on "
        "student destinations; UNESCO on global student mobility. Full inline links in the web edition.", small),
    Spacer(1, 6 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=8),
]
story += [callout(
    "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit together, "
    "and bounce ideas. This research is part of an open library, free to read and share. The Forum itself "
    "is by application.<br/><br/>"
    "Read the web edition with live source links: "
    "africaglobalforum.com/reports/africans-abroad-counted-2026<br/>"
    "Companion reports: The Visa Treadmill · Where the Door Is Actually Open<br/>"
    "Apply to join: africaglobalforum.com", bg=INK)]

doc.build(story)
print("wrote", OUT)
