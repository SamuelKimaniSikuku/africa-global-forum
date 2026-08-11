#!/usr/bin/env python3
"""Generate the AGF report PDF: Where the Door Is Actually Open (2026)."""

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
IMG = os.path.join(HERE, "open-door-countries-2026", "img")
OUT = os.path.join(HERE, "open-door-countries-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "Where the Door Is Open · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Rules as at 11 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="Where the Door Is Actually Open (2026)",
                      author="Africa Global Forum",
                      subject="Immigration policy for Africans moving abroad: students, workers, family, settlement")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])

story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("Where the Door Is Open", h1),
    Paragraph("The countries with the best policy for Africans moving abroad",
              S("sub", fontName="Helvetica-Oblique", fontSize=15, leading=19,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Our last report priced what it costs to <i>stay</i> legal. This one answers the question that "
        "comes first: <b>where should you go?</b> A policy-by-policy read of the countries that actually "
        "make room for Africans — to study, to work, to bring family, and to stop renewing.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("€0", big_num), Paragraph("€36,848", big_num),
    Paragraph("3 yrs", big_num), Paragraph("28.2%", big_num),
], [
    Paragraph("tuition at German public<br/>universities, 15 of 16 states", big_lbl),
    Paragraph("Ireland's graduate salary<br/>floor — family from day one", big_lbl),
    Paragraph("to German citizenship<br/>on the accelerated route", big_lbl),
    Paragraph("of intra-African travel<br/>is now visa-free", big_lbl),
]], colWidths=[CONTENT_W / 4] * 4)
kpi.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), INK),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 14),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
story += [kpi, Spacer(1, 6 * mm)]
story += [fig("scorecard.png",
              "Fig 1 — The scorecard. AGF's own assessment built from the policy detail in this "
              "report — a judgement, not a measured index. The underlying rules are all sourced; "
              "the weighting is ours. 5 = best, 1 = worst.", max_w=150 * mm)]
story += [Paragraph(
    "Published August 2026 by Africa Global Forum · africaglobalforum.com/reports/open-door-countries-2026",
    small), PageBreak()]

# ================= 01 =================
story += [
    Paragraph("01 · Executive Summary", h2),
    Paragraph(
        "Most advice about moving abroad is organised around <i>desire</i> — which country you would "
        "like to live in. This report is organised around <i>policy</i>: which countries have written rules "
        "that a person leaving Lagos, Nairobi, Accra, Luanda or Casablanca can actually satisfy. Those are "
        "different questions, and the answers are not the ones the market pushes hardest.", body),
]
story += bullets([
    "<b>Germany is the strongest all-round option, and it is not close.</b> Public universities charge "
    "<b>€0 tuition</b> to African students in fifteen of sixteen states, the Opportunity Card lets a "
    "qualified person come to look for work <i>without a job offer</i>, and citizenship arrives in "
    "<b>five years — or three</b> with strong integration.",
    "<b>Ireland has the best terms for a graduate who wants to bring family.</b> The Critical Skills "
    "Employment Permit carries <b>no labour market test, family reunification from day one</b>, and a route "
    "to Stamp 4 in two years — at a graduate salary floor of <b>€36,848</b>.",
    "<b>Portugal has a route most eligible Africans have never used.</b> The CPLP agreement gives nationals "
    "of <b>Angola, Mozambique, Cabo Verde, Guinea-Bissau, São Tomé and Príncipe and Equatorial Guinea</b> "
    "a residence permit that requires no proof of employment or minimum income.",
    "<b>Canada is narrowing but has not closed.</b> Study permits are capped at 408,000 for 2026 and the "
    "student admissions target fell 49% — but master's and doctoral students at public institutions are "
    "now exempt from the cap entirely.",
    "<b>The UK is on a deadline.</b> The Graduate Route drops from 24 months to 18 for most graduates from "
    "<b>1 January 2027</b>; applications submitted before 31 December 2026 lock in the two-year version.",
    "<b>And Africa itself is 28.2% open</b> — the share of intra-African travel needing no visa. Benin, "
    "The Gambia, Rwanda and Seychelles are fully open to all Africans; Ghana joined in January 2025 and "
    "Kenya in January 2024.",
])
story += [Paragraph(
    "The countries that advertise hardest are rarely the countries whose rules are kindest. "
    "Read the statute, not the brochure.", pull)]

# ================= 02 =================
story += [
    Paragraph("02 · What “Open” Actually Means", h2),
    Paragraph(
        "“Good immigration policy” is not one thing. A country can be generous to students and brutal to "
        "their spouses. It can hand out work permits freely and never hand out passports. So this report "
        "scores five separate things, because a family moving abroad has to clear all five, not one: "
        "<b>cost of studying</b>; <b>getting hired</b> (the salary floor, the labour market test, and whether "
        "you may arrive before you have a job); <b>family rights</b>; <b>speed to permanence</b>; and "
        "<b>total fee burden</b>, covered in depth in our companion report, <i>The Visa Treadmill</i>.", body),
    Paragraph(
        "Two things Fig 1 makes visible immediately. <b>No country wins on everything.</b> France is one of "
        "the cheapest places on earth to get a degree and one of the harder places to get hired as a non-EU "
        "graduate. Ireland is superb once you have a job offer and expensive before you do. <b>And the UK — "
        "still the default destination in most African family conversations — scores worst overall</b>, "
        "driven by fee burden and the length of its settlement clock.", body),
]

# ================= 03 =================
story += [
    Paragraph("03 · The Africa Tax", h2),
    Paragraph(
        "Before any comparison of destination policy, there is a fact that applies to African applicants "
        "specifically and to almost nobody else at the same intensity: <b>you are far more likely to be "
        "refused, and you pay for the refusal.</b>", body),
    fig("schengen_refusal.png",
        "Fig 2 — Schengen short-stay refusal rates for selected African nationalities, against the "
        "global average (LAGO Collective analysis, via CNN)."),
    Paragraph(
        "The Schengen visa fee is <b>€90</b> and it is <b>non-refundable on refusal</b>. Put those two "
        "facts together and you get one of the most quietly extractive transfers in the global economy.", body),
    fig("lost_fees.png",
        "Fig 3 — Refused Schengen applications cost applicants €157.1m in 2025, up from €145.1m in "
        "2024 and €130m in 2023. Africa is 24% of applicants and 42% of the loss.", max_w=150 * mm),
    Paragraph(
        "In 2024 alone, African applicants lost roughly <b>€60 million (about $67.5m)</b> to refused "
        "Schengen applications. As LAGO Collective's Marta Foresti put it, the poorer the country of origin, "
        "the higher the refusal rate — which means the poorest applicants subsidise the system that "
        "rejects them.", body),
    Paragraph(
        "This is the single strongest argument for choosing your destination by <i>route</i>, not by "
        "preference. A long-stay study or work visa is assessed on documents you can control. A short-stay "
        "visitor visa is assessed on a suspicion you cannot.", pull),
]

# ================= 04 =================
story += [
    Paragraph("04 · If You Are a Student", h2),
    Paragraph(
        "Three things decide whether studying abroad is a viable plan rather than an expensive detour: what "
        "the degree costs, whether you can work while you study, and <b>how long you are allowed to stay "
        "afterwards to convert the degree into a job.</b> That last one is the whole ballgame, and it is the "
        "one most families never ask about.", body),
    Paragraph("Tuition: Germany and France are in a category of their own", h3),
    Paragraph(
        "Public universities across <b>fifteen of Germany's sixteen states charge no tuition at all</b>, to "
        "Germans and Africans alike. You pay only a semester contribution of roughly <b>€100–€300</b> "
        "— around €700 a year including administrative costs. The single exception is "
        "<b>Baden-Württemberg</b> (Stuttgart, Heidelberg, Freiburg, Karlsruhe, Mannheim), which charges "
        "non-EU students <b>€1,500 per semester</b> on top of the semester fee. PhD students are typically "
        "exempt even there.", body),
    Paragraph(
        "Read that again, because it inverts the usual assumption: <b>a Nigerian or Kenyan student can take "
        "a German master's degree for roughly the cost of the paperwork</b>, while the equivalent UK or "
        "Canadian degree runs into five figures a year. Germany also hosts thousands of English-taught "
        "programmes, so the language barrier is at the job stage, not the admission stage.", body),
    Paragraph("The post-study window is the number that matters", h3),
    Paragraph(
        "A degree you cannot convert into a work permit is a very expensive souvenir. What decides "
        "conversion is how many months you have to find an employer after graduating — while still "
        "lawfully resident, still able to interview locally, still on the ground.", body),
    fig("post_study.png",
        "Fig 4 — How long you may stay after graduating to look for work. Canada's PGWP length tracks "
        "programme length up to three years and is restricted to eligible fields of study."),
    Paragraph(
        "<b>The UK is on a deadline.</b> The Graduate Route currently gives bachelor's and master's "
        "graduates 24 months. From <b>1 January 2027 that drops to 18 months</b> (PhDs keep three years). "
        "Applications submitted before 31 December 2026 lock in the two-year version. If the UK is your plan "
        "and your timing is flexible, that date is worth six months of your life.", body),
    Paragraph(
        "<b>Germany's 18 months is more generous than it looks</b>, because it stacks with everything else "
        "Germany offers: you may work while searching, tuition was free, and the residence clock toward "
        "settlement has been running the whole time.", body),
]

# ================= 05 =================
story += [
    Paragraph("05 · If You Are a Worker", h2),
    Paragraph(
        "For someone applying from Africa with a degree and experience but no European or North American "
        "work history, three questions decide everything: <b>Can I come without a job offer? What salary "
        "must an employer promise? And does the employer have to prove no local could do the job?</b>", body),
    Paragraph("The rarest and most valuable feature: arriving without a job", h3),
    Paragraph(
        "Almost every skilled-migration system requires an offer before you may enter. Germany's "
        "<b>Opportunity Card (Chancenkarte)</b> is the significant exception, and it is badly under-used by "
        "African applicants. You qualify either by holding a recognised degree or vocational qualification, "
        "or by scoring at least <b>six points</b> on a grid covering qualifications, experience, language, "
        "age and prior ties to Germany. You need <b>German at A1 or English at B2</b>, and proof of about "
        "<b>€1,091 a month</b> to support yourself. Once there you may work <b>up to 20 hours a week in any "
        "sector</b> and take two-week trial placements with unlimited employers.", body),
    Paragraph(
        "English at B2 and a recognised degree is enough to legally enter Germany to look for work. "
        "Most people who qualify for this have never heard of it.", pull),
    Paragraph("The salary an employer must be willing to promise", h3),
    Paragraph(
        "Where an offer <i>is</i> required, the binding constraint is rarely the visa — it is the salary "
        "floor. This is the number that quietly disqualifies most applicants, and it varies enormously.", body),
    fig("salary_thresholds.png",
        "Fig 5 — The minimum salary an employer must offer, 2026 rates. Netherlands figures annualised "
        "from the monthly thresholds of €4,357 (under 30) and €5,942 (30+)."),
]
story += bullets([
    "<b>Ireland's graduate rate is the most reachable number on this chart.</b> A recent graduate of a "
    "recognised third-level institution — anywhere, at Level 8 or above, in an occupation on the Critical "
    "Skills list — needs an offer of just <b>€36,848</b>. Without a relevant degree the same permit "
    "demands €68,911, nearly double. The degree is doing almost all the work.",
    "<b>Germany's Blue Card splits the same way.</b> Standard threshold €50,700 from 1 January 2026; but "
    "shortage occupations, recent graduates, and qualifying IT specialists <i>without a degree</i> come in "
    "at <b>€45,934</b>. That IT carve-out is one of very few routes in Europe that admits self-taught or "
    "bootcamp-trained technologists on experience alone.",
    "<b>The Netherlands is the outlier, and the age cliff is severe.</b> Under 30 you need about €52,284; "
    "at 30 you need about €71,304 — a 36% jump on your birthday. For a mid-career African professional, "
    "the Dutch route is often the least reachable on this list despite the country's reputation.",
])
story += [
    Paragraph("The labour market test — the invisible obstacle", h3),
    Paragraph(
        "Some permits require the employer to advertise the role locally first and prove nobody suitable "
        "applied. That single requirement kills more African applications than any salary rule, because it "
        "makes hiring you administratively expensive for the employer. Ireland's Critical Skills Employment "
        "Permit carries <b>no labour market needs test</b>. Neither does the Dutch Highly Skilled Migrant "
        "route, provided the salary threshold is met. Germany's Blue Card generally does not either. When "
        "you are choosing which permit to target, this is worth as much as the salary number — it decides "
        "whether an employer will even engage.", body),
]

# ================= 06 =================
story += [
    Paragraph("06 · Family, and the Clock", h2),
    Paragraph(
        "Two questions get asked late and should be asked first. <b>Can my family come with me?</b> And "
        "<b>when does the renewing stop?</b>", body),
    Paragraph(
        "On family, <b>Ireland's Critical Skills permit is the standout: family reunification from day "
        "one</b>, with a route to Stamp 4 — which removes employment-permit conditions entirely — after "
        "two years. Canada's permanent residence routes bring the whole family in one application, and "
        "spouses of many permit-holders receive open work permits. Several other systems make dependants "
        "wait, or admit them on permits that do not allow work, which converts a two-income household into "
        "a one-income household at exactly the moment costs spike.", body),
    fig("citizenship_clock.png",
        "Fig 6 — Years of lawful residence before a citizenship application becomes possible on the "
        "standard route. Canada requires permanent residence first, then three years of physical presence "
        "within five; the UK figure includes the year between settlement and naturalisation."),
    Paragraph(
        "The spread here is the single largest difference between destinations in this entire report. "
        "<b>Germany's accelerated three years versus the UK's 10-year route is an eight-year gap in your "
        "life</b> — eight more years of renewals, of fees, of being deportable, of not being able to plan.", body),
    Paragraph(
        "Germany's 2024 citizenship reform cut the standard requirement from eight years to five, and to "
        "<b>three years with strong integration</b> (C1 German plus demonstrated integration). It also "
        "permitted dual citizenship, which removes the wrenching choice many African families faced between "
        "a German passport and their own.", body),
]

# ================= 07 =================
story += [
    Paragraph("07 · Your Passport May Have a Shortcut", h2),
    Paragraph(
        "Most migration advice treats all Africans as one applicant pool. The rules do not. Two shortcuts "
        "exist that depend entirely on which African passport you hold — and both are heavily "
        "under-used.", body),
    Paragraph("The Lusophone route: CPLP", h3),
    Paragraph(
        "If you are a national of <b>Angola, Mozambique, Cabo Verde, Guinea-Bissau, São Tomé and Príncipe, "
        "or Equatorial Guinea</b>, the Community of Portuguese Language Countries agreement gives you access "
        "to a Portuguese residence permit on terms nobody else gets. The permit is issued for <b>two years, "
        "renewable for three-year periods</b>, and — the remarkable part — <b>does not require proof of "
        "employment or minimum income</b>. Law 9/2025 upgraded it to the EU uniform residence card format, "
        "which carries the right to travel and work across the Schengen Area.", body),
    Paragraph(
        "<b>One critical 2026 change.</b> Under the new visa regime approved in 2025, you can no longer "
        "apply for the CPLP permit from inside Portugal on a tourist visa or visa waiver. <b>You must now "
        "obtain a consular residence visa before travelling.</b> Anyone working from pre-2025 advice — "
        "including a great deal of what is still circulating in WhatsApp groups — will get this wrong and "
        "lose the fee.", body),
    Paragraph("The Francophone route", h3),
    Paragraph(
        "For nationals of Senegal, Côte d'Ivoire, Cameroon, Mali, Burkina Faso, Benin, Togo, Niger, Guinea, "
        "Congo, DRC, Madagascar, Morocco, Tunisia and Algeria, France offers something structurally similar "
        "in effect if not in law: near-free public university tuition, degrees taught in a language you "
        "already hold, and dense professional and family networks already in place. France's "
        "<i>Passeport Talent</i> covers skilled workers, researchers and founders on multi-year permits.", body),
    Paragraph(
        "The trade-off is honest and worth stating: as <i>The Visa Treadmill</i> documented, France sharply "
        "raised its residence and naturalisation duties in 2026 — the naturalisation stamp alone went from "
        "€55 to €255. The fees are still low in absolute terms. The direction of travel is not favourable.", body),
]

# ================= 08 =================
story += [
    Paragraph("08 · The Country Profiles", h2),
    Paragraph("Germany — the strongest all-round option", h3),
    table([
        [Paragraph("Dimension", th), Paragraph("What the rules say", th)],
        [Paragraph("Studying", cell), Paragraph("€0 tuition at public universities in 15 of 16 states; "
                                                "~€700/yr in semester fees. Baden-Württemberg charges "
                                                "non-EU students €1,500/semester.", cell)],
        [Paragraph("After graduating", cell), Paragraph("18-month residence permit to seek work, with the "
                                                        "right to work while searching.", cell)],
        [Paragraph("Arriving without a job", cell), Paragraph("<b>Yes</b> — Opportunity Card. 6 points on "
                                                              "the grid, German A1 <i>or</i> English B2, "
                                                              "~€1,091/month funds. 20 hrs/week work "
                                                              "permitted.", cell)],
        [Paragraph("With a job", cell), Paragraph("EU Blue Card at €50,700, or €45,934 for shortage "
                                                  "occupations, recent graduates and qualifying IT "
                                                  "specialists without a degree.", cell)],
        [Paragraph("Citizenship", cell), Paragraph("5 years, or <b>3 with strong integration</b>. Dual "
                                                   "citizenship permitted since 2024.", cell)],
    ], [45 * mm, 125 * mm]),
    Spacer(1, 3 * mm),
    Paragraph(
        "<b>The catch:</b> German. You can be admitted and educated in English, but the graduate labour "
        "market outside tech and academia expects working German. Budget two years of language study as part "
        "of the plan, not as an afterthought.", body),

    Paragraph("Ireland — the best terms once you have an offer", h3),
    table([
        [Paragraph("Dimension", th), Paragraph("What the rules say", th)],
        [Paragraph("Studying", cell), Paragraph("Fees are high — the weakest part of the Irish case.", cell)],
        [Paragraph("After graduating", cell), Paragraph("Third Level Graduate Scheme: 24 months.", cell)],
        [Paragraph("With a job", cell), Paragraph("Critical Skills Employment Permit. <b>€36,848</b> for "
                                                  "graduates of the last 12 months in a listed occupation; "
                                                  "€40,904 standard with a relevant degree; €68,911 without "
                                                  "one.", cell)],
        [Paragraph("Labour market test", cell), Paragraph("<b>None</b> for Critical Skills roles.", cell)],
        [Paragraph("Family", cell), Paragraph("<b>Reunification from day one.</b>", cell)],
        [Paragraph("Permanence", cell), Paragraph("Stamp 4 after 2 years; citizenship at 5 years reckonable "
                                                  "residence.", cell)],
    ], [45 * mm, 125 * mm]),
    Spacer(1, 3 * mm),
    Paragraph(
        "Salary thresholds rose on 1 March 2026 and a published roadmap phases in further increases through "
        "2030 — so the €36,848 graduate floor is the <i>lowest it will be</i>. English-speaking, no language "
        "barrier, and a genuine two-year runway. For an African graduate in healthcare, tech or engineering, "
        "this is arguably the single most reachable high-quality destination on the list.", body),

    Paragraph("Canada — narrowing, but the graduate door widened", h3),
    Paragraph(
        "Canada spent 2024–25 tightening: study permits capped, PGWP field-of-study restrictions introduced, "
        "the 2026 student admissions target cut 49% to 155,000. General Express Entry draws have not run "
        "since April 2024 — every invitation now comes through provincial nominations, category-based draws, "
        "or the Canadian Experience Class.", body),
    Paragraph(
        "But read the detail, because it cuts the other way for one specific group: <b>from 1 January 2026, "
        "master's and doctoral students at public institutions are exempt from the study permit cap</b> and "
        "need no provincial attestation letter. And category-based draws — healthcare, STEM, trades, French "
        "language, and new 2026 categories for senior managers and researchers — often clear at lower CRS "
        "scores than general draws did. Canada has become materially harder for undergraduate and "
        "college-diploma applicants and slightly <i>easier</i> for graduate-degree applicants in targeted "
        "occupations. If you speak French, the francophone category draws are the most under-exploited "
        "advantage in Canadian immigration.", body),

    Paragraph("Netherlands — excellent, if you are under 30", h3),
    Paragraph(
        "The Highly Skilled Migrant route has no labour market test and fast processing through recognised "
        "sponsors. The 12-month Orientation Year lets graduates of Dutch universities stay and work freely. "
        "But the salary thresholds are the highest here, and the jump at 30 is brutal: €4,357/month becomes "
        "€5,942/month overnight.", body),

    Paragraph("United Kingdom — the honest assessment", h3),
    Paragraph(
        "The UK remains the default in most African family conversations, and on policy it is now among the "
        "weaker options. Fees are the highest of any country we have costed — £77,414 for a family of four "
        "on the 10-year route. The Graduate Route shortens in January 2027. The Immigration Health Surcharge "
        "adds £1,035 per adult per year, payable upfront. <b>What the UK still has</b> that nowhere else on "
        "this list matches: language, an enormous established African diaspora, degree recognition across "
        "Anglophone Africa, and the densest professional networks. Those are real advantages and they are "
        "why people keep choosing it. Just choose it with the price list in front of you.", body),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("09 · Africa's Own Open Doors", h2),
    Paragraph(
        "Every report like this assumes “abroad” means Europe or North America. For a growing number of "
        "African professionals it means Kigali, Accra, Nairobi, Port Louis or Casablanca — and the mobility "
        "picture within Africa is improving faster than the picture outside it.", body),
    fig("africa_openness.png",
        "Fig 7 — Intra-African visa openness at the end of 2025 (AfDB Africa Visa Openness Index)."),
    Paragraph(
        "<b>28.2% of intra-African travel is visa-free.</b> That is low, and it is also the highest it has "
        "ever been. <b>Benin, The Gambia, Rwanda and Seychelles</b> hold full openness scores. <b>Ghana</b> "
        "opened to all African passport holders on 1 January 2025; <b>Kenya</b> did so from January 2024. "
        "Namibia, Zambia, Zimbabwe and Malawi were among the most improved.", body),
    Paragraph(
        "The honest counterweight, and it is a serious one: <i>The Visa Treadmill</i> found that <b>Nigeria "
        "and Kenya are the two most expensive countries in Africa in which to hold long-term legal "
        "status</b> — roughly $122,000 and $53,700 respectively for a family of four to reach citizenship, "
        "driven by per-person annual work-permit levies with no family discount. Visa-free <i>entry</i> and "
        "affordable <i>residence</i> are completely different things, and African policy is currently much "
        "better at the first than the second.", body),
    Paragraph(
        "A continent can open its borders to visitors and still price out the people who want to stay and "
        "build. That gap is the next reform.", pull),

    Paragraph("10 · What's Closing", h2),
    Paragraph(
        "A report that only lists open doors would be dishonest. The direction of travel in 2025–26 has been "
        "toward restriction almost everywhere, and anyone planning a move over a five-year horizon should "
        "assume today's terms are the best terms.", body),
]
story += bullets([
    "<b>The UK Graduate Route</b> falls from 24 to 18 months on 1 January 2027.",
    "<b>Canada's study permits</b> are capped at 408,000 for 2026, down 7%; the student admissions target "
    "fell 49%.",
    "<b>Ireland's salary thresholds</b> rise on a published schedule through 2030.",
    "<b>Germany's Blue Card thresholds</b> rose on 1 January 2026 and are indexed to rise again.",
    "<b>The Netherlands</b> raised its thresholds about 4.5% for 2026.",
    "<b>France</b> raised residence and naturalisation duties sharply from 1 May 2026.",
    "<b>Portugal</b> closed the in-country CPLP application route and is reforming its nationality law.",
])
story += [Paragraph(
    "Only one significant change ran the other way: <b>Germany's 2024 citizenship reform</b>, cutting the "
    "residence requirement from eight years to five (three with strong integration) and permitting dual "
    "citizenship. That is a large exception, and it is a large part of why Germany tops this report.", body)]

# ================= 11 =================
story += [
    Paragraph("11 · The Decision Playbook", h2),
    Paragraph(
        "Not advice on immigration law — get that from a regulated adviser in the destination country. This "
        "is how to think about the choice.", body),
]
story += bullets([
    "<b>Check your passport for a shortcut before anything else.</b> If you hold an Angolan, Mozambican, "
    "Cabo Verdean, Bissau-Guinean, São Toméan or Equatorial Guinean passport, the CPLP route to Portugal "
    "asks less of you than any other route in Europe asks of anyone. If you are francophone, France and "
    "Canada's French-language category draws are structurally easier for you than for an equivalent "
    "anglophone applicant. Most people never check.",
    "<b>If money is the binding constraint, the answer is Germany.</b> Free tuition changes the arithmetic "
    "of the entire decision — it converts a debt-funded move into a savings-funded one, and it is the "
    "difference between going and not going for a large number of families.",
    "<b>If a job offer is the binding constraint, target Ireland's graduate CSEP.</b> €36,848, no labour "
    "market test, family from day one. Know the exact threshold and the Critical Skills Occupations List "
    "before you apply for anything, and tell prospective employers the number — most do not know how low "
    "it is.",
    "<b>If you have a degree but no offer, use the Opportunity Card.</b> It is the only major route that "
    "lets you legally arrive and search. English B2 is enough to enter.",
    "<b>Count the whole clock, not the first visa.</b> A cheap entry route attached to a 10-year settlement "
    "path costs more in money, risk and life than an expensive route attached to a 5-year one.",
    "<b>Ask about your spouse's work rights before you accept the offer.</b> A dependant visa without work "
    "rights halves household income at the exact moment your costs double.",
    "<b>Prefer long-stay national routes over short-stay visas.</b> Long-stay applications are decided "
    "against published criteria you can satisfy with documents. Short-stay visitor visas are decided "
    "against discretion — which is where the 45–60% African refusal rates live.",
    "<b>Move before the rule changes, where you can.</b> A UK Graduate Route application filed by "
    "31 December 2026 is worth six extra months. Ireland's graduate salary floor is the lowest it will be.",
    "<b>Consider Africa seriously.</b> Kigali, Accra and Nairobi are real options with genuine professional "
    "depth — but price the residence permits, not just the flight. Entry is cheap; staying is not.",
])

# ================= 12 =================
story += [
    Paragraph("12 · Method &amp; Limits", h2),
    Paragraph(
        "<b>What this report is:</b> a comparison of published immigration rules as at 11 August 2026, "
        "focused on the criteria that bind African applicants specifically — cost, salary floors, family "
        "rights, and time to permanence.", body),
    Paragraph(
        "<b>What it is not:</b> a ranking of countries as places to live. Nothing here scores wages, cost of "
        "living, racism, climate, healthcare quality or how it feels to be African in any of these "
        "societies. Those matter enormously and this report is silent on them.", body),
]
story += bullets([
    "<b>The scorecard in Fig 1 is AGF's own judgement</b>, not a measured index. The underlying rules are "
    "sourced; the 1–5 weighting is editorial. Reasonable people would score it differently.",
    "Salary thresholds, caps and permit lengths change frequently — several in this report changed within "
    "the last eight months. <b>Verify every number against the official source before you act on it.</b>",
    "Occupation lists (Ireland's Critical Skills list, Canada's category draws, Germany's shortage "
    "occupations) determine eligibility as much as salary does, and they are revised regularly.",
    "Refusal-rate data covers <i>short-stay Schengen visitor visas</i> and does not describe study or work "
    "visa outcomes, which are assessed differently.",
    "Portugal's nationality law is under reform; we have deliberately not quoted a residence requirement "
    "for citizenship there.",
    "Currency thresholds are quoted in the currency the rule is written in. No conversions are applied.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "German Opportunity Card and EU Blue Card guidance via Jobbatical and MyGermanUniversity; "
        "Baden-Württemberg tuition via MyGermanUniversity; Ireland's Department of Enterprise, Trade and "
        "Employment and Fragomen on the March 2026 thresholds; KPMG and Jobbatical on Dutch 2026 thresholds; "
        "CIC News and IRCC on Canadian study permits, PGWP and Express Entry; Lamares Capela and Apoio "
        "Jurídico Imigração on CPLP; CNN and EUobserver on LAGO Collective refusal-fee analysis; the AfDB "
        "Africa Visa Openness Index; and UK Home Office guidance on the Graduate Route. Full inline links in "
        "the web edition.", small),
    Spacer(1, 6 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=8),
]
story += [callout(
    "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit together, "
    "and bounce ideas. This research is part of an open library, free to read and share. The Forum itself "
    "is by application.<br/><br/>"
    "Read the web edition with live source links: africaglobalforum.com/reports/open-door-countries-2026<br/>"
    "Companion report: africaglobalforum.com/reports/visa-treadmill-2026<br/>"
    "Apply to join: africaglobalforum.com", bg=INK)]

doc.build(story)
print("wrote", OUT)
