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
IMG = os.path.join(HERE, "name-on-the-cv-2026", "img")
OUT = os.path.join(HERE, "name-on-the-cv-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Name on the CV · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 24 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Name on the CV (2026)",
                      author="Africa Global Forum",
                      subject="What the hiring experiments found about names, and what a candidate can do")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Name on the CV.", h1),
    Paragraph("What the experiments found.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "For thirty years, researchers have run the same experiment: send employers <b>identical "
        "CVs</b> with different names, and count who gets called. It is the closest thing social "
        "science has to a controlled trial of prejudice. This report is what those experiments "
        "found — and what a candidate can actually do with it.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("50%", big_num), Paragraph("0", big_num),
    Paragraph("3×", big_num), Paragraph("25v10", big_num),
], [
    Paragraph("more callbacks for the same<br/>CV with a white name", big_lbl),
    Paragraph("improvement in the US gap<br/>across 25 years of studies", big_lbl),
    Paragraph("worse in France than in<br/>Germany — country matters", big_lbl),
    Paragraph("callback rates for whitened<br/>vs transparent CVs (%)", big_lbl),
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
    fig("by_country.png",
        "Fig 3 — Extra applications a nonwhite candidate must send for the same callbacks, from the "
        "nine-country meta-analysis (Quillian et al., 2019) with the British GEMM figure added. See "
        "Section 05.", max_h=95 * mm),
    Paragraph("Published August 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/name-on-the-cv-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Every African abroad has wondered it, usually at 11pm after the fortieth silent "
        "application: <i>is it the CV, or is it my name?</i> This is one of the very few questions "
        "in this library where science has a direct, experimental answer.", body),
]
story += bullets([
    "<b>The name effect is real, large and causal.</b> In the founding experiment, identical CVs "
    "with white-sounding names received <b>50% more callbacks</b> than the same CVs with "
    "Black-sounding names. The CVs were fictional and the names randomly assigned, so nothing else "
    "can explain the gap.",
    "<b>It has not improved.</b> A meta-analysis of every US field experiment since 1989 — 28 "
    "studies, 55,842 applications — found <b>no change in discrimination against Black applicants "
    "over 25 years</b>. Whites receive on average <b>36% more callbacks</b>.",
    "<b>Where you apply matters enormously.</b> Across nine countries: in <b>France and Sweden</b>, "
    "a nonwhite candidate needs <b>70–94% more applications</b> for the same callbacks. In "
    "<b>Germany and the US, 25–40%</b>. The worst country is more than three times the best.",
    "<b>Britain measured it for Africans specifically.</b> In the GEMM experiment, minority "
    "applicants needed <b>60% more applications</b>; for <b>Black African</b> applicants, callback "
    "odds were <b>less than half</b> those of an identical white British applicant — including for "
    "candidates born and educated in Britain.",
    "<b>“Whitening” measurably works, which is its own indictment.</b> Black candidates who "
    "scrubbed racial cues got <b>25% callbacks against 10%</b> for the untouched version. Employers "
    "with pro-diversity statements discriminated <b>just as much</b>.",
    "<b>The name is only half the bill.</b> In 13,000 Canadian CVs, an English name beat an Asian "
    "name by ~40% — but <b>where the experience happened mattered even more</b>. Foreign-only "
    "experience roughly halved callbacks again.",
    "<b>And it is concentrated.</b> In 83,000 applications to 108 Fortune 500 firms, most showed "
    "small gaps — while <b>an identifiable subset accounted for most of the discrimination</b>. Bad "
    "news about those firms; useful news for a candidate.",
])
story += [
    Paragraph("You were never imagining it. The silence has been measured, in controlled "
              "experiments, for thirty years. The rest of this report is about what to do inside "
              "that fact.", pull),
]

# ================= 02 =================
story += [
    PageBreak(),
    Paragraph("02 · How We Know", h2),
    Paragraph(
        "A <b>correspondence study</b> works like this. Researchers write fictional CVs — "
        "realistic, matched in every detail. They send them to real job postings, randomly "
        "assigning names that signal race or origin: one employer receives “Emily Walsh,” the next "
        "receives the identical document as “Lakisha Washington” or “Adebayo Okonkwo.” Then they "
        "count callbacks.", body),
    Paragraph(
        "Because the applicants do not exist and the names are assigned by lottery, <b>nothing "
        "differs between the piles except the name.</b> Any gap in callbacks has exactly one "
        "available explanation.", body),
]
story += bullets([
    "<b>It is a true experiment</b>, with random assignment — the same design standard as a drug "
    "trial.",
    "<b>It measures behaviour, not attitudes.</b> No one is asked whether they discriminate. Their "
    "inbox answers.",
    "<b>It has been replicated for decades</b>, in dozens of countries, across hundreds of "
    "thousands of applications — and the direction of the finding has never reversed.",
])
story += [
    Paragraph(
        "One honest boundary: correspondence studies measure <b>the first screen only</b> — the "
        "decision to call. Everything in this report is about the doorway, not the room.", body),

    Paragraph("03 · The Founding Experiment", h2),
    fig("the_experiment.png",
        "Fig 1 — The design of Bertrand &amp; Mullainathan (2004): nearly 5,000 CVs answering real "
        "advertisements in Boston and Chicago."),
    Paragraph(
        "White names received <b>50% more callbacks for interviews.</b> The second finding is less "
        "quoted and, for this audience, more important: the researchers also varied CV quality. "
        "<b>Improving the CV helped white names substantially and Black names much less.</b> The "
        "market rewarded Emily for being excellent and largely ignored the same excellence from "
        "Lakisha.", body),
    Paragraph("Read that carefully, because it breaks the advice every immigrant parent gives: “be "
              "twice as good.” The experiment found that being twice as good is precisely what the "
              "screen fails to see.", pull),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · Twenty-Five Years, No Change", h2),
    fig("no_change.png",
        "Fig 2 — The trend that is not a trend. Quillian, Pager, Hexel &amp; Midtbøen, PNAS (2017)."),
    Paragraph(
        "In 2017 a team led by Lincoln Quillian gathered <b>every available US field experiment "
        "since 1989</b> — 28 studies, 55,842 applications — and asked whether hiring discrimination "
        "against Black applicants had declined. <b>It had not moved.</b> Whites received on average "
        "<b>36% more callbacks</b>, and the gap in 2015 was statistically indistinguishable from "
        "1989.", body),
]
story += bullets([
    "<b>Do not price in progress.</b> A generation of corporate diversity effort left the callback "
    "gap intact. Plan for the market as measured, not as advertised.",
    "<b>This is a structural constant, not a passing mood.</b> The useful question shifts from "
    "“when will it end?” to “where is it weakest, and how do I route around it?”",
])

# ================= 05 =================
story += [
    Paragraph("05 · Where It Is Worst", h2),
    Paragraph(
        "The most practically useful finding in the literature: <b>the same nonwhite candidate "
        "faces radically different screens in different countries.</b> Fig 3 on the cover has the "
        "chart. Across nine countries, discrimination was found everywhere — but in <b>France</b>, "
        "the worst measured market, the white-native advantage is <b>more than three times</b> what "
        "it is in <b>Germany</b>, the lowest. In France and Sweden a minority candidate must send "
        "<b>70–94% more applications</b>; in Germany and the US, <b>25–40%</b>.", body),
]
story += bullets([
    "<b>This belongs in your destination arithmetic.</b> A market with a slightly lower salary and "
    "a Germany-grade screen can beat one with a higher salary behind a France-grade screen.",
    "<b>It reframes the French paradox.</b> France hosts more African students than any other "
    "single country — and runs the most hostile measured CV screen in the West. Presence and "
    "access are different things.",
    "<b>Sweden is the surprise.</b> Reputation for progressive politics; screen measured alongside "
    "France's. Reputation is not data.",
    "<b>The caution:</b> country effects partly reflect application formats and which minorities "
    "were tested. Treat the ordering as robust and the exact figures as ranges.",
])
story += [
    Paragraph("06 · The British Numbers", h2),
    Paragraph(
        "The British <b>GEMM experiment</b> (2016–17) tested this network's situation directly: "
        "applications in the name of candidates of <b>Nigerian</b> and other specific origins, sent "
        "to real British vacancies. Ethnic minority applicants needed <b>60% more applications</b>; "
        "for a <b>Black African</b> applicant, callback odds were <b>less than half</b> those of an "
        "identical white British applicant. The penalty applied to candidates <b>born, raised and "
        "educated in Britain</b> — the document is read before the person exists.", body),
    Paragraph(
        "Our earnings-gap research found that most of the African pay penalty is about which jobs "
        "people get, not unequal pay within jobs — and this is the mechanism at the very front of "
        "that pipeline: <b>the gap begins before anyone has met you.</b>", body),
]

# ================= 07 =================
story += [
    Paragraph("07 · The Whitening Experiment", h2),
    fig("whitening.png",
        "Fig 4 — Kang, DeCelles, Tilcsik &amp; Jun, Administrative Science Quarterly (2016). Asian "
        "candidates showed the same pattern: 21% whitened, 11.5% transparent."),
    Paragraph(
        "<b>“Whitened” CVs</b> — name anglicised, racially identifiable associations reworded — "
        "received <b>25% callbacks</b>. The identical, racially transparent versions received "
        "<b>10%</b>. Two and a half times the response, for the same person, minus their identity.",
        body),
    Paragraph(
        "The study's second finding is bleak. Employers whose ads <b>advertised a commitment to "
        "diversity</b> punished transparent CVs <b>just as much</b>. Worse, candidates trusted the "
        "statements: they whitened <i>less</i> for pro-diversity employers, and so were exposed "
        "<i>more</i>. The researchers called it the diversity paradox.", body),
    Paragraph("The diversity statement is marketing, not measurement. On the evidence, it predicts "
              "nothing about how the screen will treat your name — except that you will trust it "
              "more than you should.", pull),

    PageBreak(),
    Paragraph("08 · The Foreign-Experience Discount", h2),
    fig("foreign_discount.png",
        "Fig 5 — Oreopoulos's Canadian field experiments. Figures are approximate rates across "
        "study waves; the ordering is the finding."),
    Paragraph(
        "<b>The name penalty:</b> with identical Canadian qualifications, English-sounding names "
        "were called back about <b>40% more often</b> than Chinese, Indian or Pakistani names "
        "(~16% vs ~11%). <b>The geography penalty:</b> keep the name and swap the experience — "
        "foreign-only work history fell to roughly <b>6%</b>, while adding Canadian experience "
        "pulled the same candidate back to ~11%.", body),
    Paragraph(
        "For a newly arrived professional this is the most actionable chart in the report, because "
        "<b>the geography penalty is the one you can retire.</b> One local contract, one recognised "
        "local credential converts the document from “foreign CV” to “local CV with extra depth.” "
        "It is also, mechanically, why the first job abroad is so much harder than the second.",
        body),
]

# ================= 09 =================
story += [
    PageBreak(),
    Paragraph("09 · It Is Concentrated", h2),
    fig("concentrated.png",
        "Fig 6 — Illustrative shape of the distribution in Kline, Rose &amp; Walters, QJE (2022). "
        "The bar heights are ours; the concentration is theirs."),
    Paragraph(
        "A Berkeley–Chicago team sent <b>83,000 fictional applications to 108 Fortune 500 "
        "companies</b> and measured each firm's gap separately. On average, distinctively Black "
        "names reduced employer contact by 2.1 percentage points — but the gaps varied enormously, "
        "and systemic discrimination was <b>concentrated in a specific, statistically identifiable "
        "subset of companies</b>, some later publicly named in a “discrimination report card.” "
        "Federal contractors, subject to audit, discriminated measurably less.", body),
]
story += bullets([
    "<b>The market is not uniformly hostile.</b> Most large firms showed small or undetectable "
    "gaps. “They are all the same” is measurably false, and strategically expensive if it stops "
    "you applying.",
    "<b>Where firms are accountable, the gap shrinks.</b> Large regulated employers, government "
    "and audited institutions are statistically safer doors.",
    "<b>The naming of firms matters.</b> Discrimination now carries firm-level reputational risk — "
    "worth checking before you spend your applications.",
])
story += [
    Paragraph("10 · What Does Not Work", h2),
    Paragraph(
        "France ran a large randomised trial of <b>anonymous CVs</b> with about a thousand firms. "
        "The measured result was the opposite of the intention: <b>participating firms became "
        "less likely to interview and hire minority candidates</b>, and the policy was abandoned in "
        "2015. The firms that volunteered were disproportionately those already favourable to "
        "minority candidates — and anonymisation stopped them favouring anyone. Hiding the name "
        "also hides <b>context that helps</b>: an employment gap that reads charitably for a known "
        "immigrant is, anonymised, just a gap.", body),
    Paragraph(
        "The lesson is not that nothing works. It is that <b>the screen cannot be tricked into "
        "fairness by deleting information</b> — what works is changing who screens, what they look "
        "for, and whether anyone audits the result.", body),
]

# ================= 11 =================
story += [
    PageBreak(),
    Paragraph("11 · The Toolbox", h2),
    fig("toolbox.png",
        "Fig 7 — What the evidence offers a candidate. None of it is fair. All of it is usable."),
]
story += bullets([
    "<b>Referrals do not fix the screen — they skip it.</b> Every result in this report happens at "
    "the anonymous first read of a document. A warm introduction moves you past the exact stage "
    "where the discrimination lives. This is the strongest single implication of the literature — "
    "and why a functioning network is not a nice-to-have but a documented counter-measure.",
    "<b>Spend applications where the odds are best.</b> Discrimination is three times worse in "
    "some countries than others and concentrated in identifiable firms. Sixty applications aimed "
    "well beat a hundred sprayed.",
    "<b>Kill the geography penalty first.</b> It is the largest penalty you can actually remove. "
    "Prioritise anything that puts a local employer's name on the document.",
    "<b>Put machine-readable proof above the fold.</b> Recognised local credentials give a "
    "hesitant screener a legible reason that overrides the name.",
    "<b>On whitening: we will not decide for you.</b> The evidence is that it works — 25% against "
    "10% — and that no diversity statement protects the transparent version. It is also a tax paid "
    "in identity, levied on people who did nothing wrong; and our language research shows the name "
    "is often the last inheritance a diaspora family keeps. Some initialise the first name and "
    "keep the surname; some refuse entirely; some cannot afford the filter this year. All three "
    "are rational. The only wrong move is not knowing the numbers when you choose.",
])
story += [
    Paragraph("12 · If You Are the One Hiring", h2),
]
story += bullets([
    "<b>Structure beats sentiment.</b> Discrimination lives in unstructured judgement calls. "
    "Defined criteria, set before CVs are opened and scored consistently, shrink the space where a "
    "name can operate.",
    "<b>Test work, not paper.</b> A short skills task moves the decision from “does this CV feel "
    "right?” to “can this person do the thing?”, where names cannot operate.",
    "<b>Audit your own funnel.</b> Count callbacks by name type in your own pipeline once a "
    "quarter. Firms that measure, behave.",
    "<b>Do not confuse your statement with your screen.</b> The whitening study's employers surely "
    "believed their diversity language. Their inboxes disagreed.",
    "<b>And check your own in-group.</b> An African founder's pile has its own gravity — toward "
    "kin, church, ethnicity, accent. The mechanism is human, not white. If the screen is "
    "unstructured, someone's name is paying for it, including in Lagos and Nairobi.",
])

# ================= 13 =================
story += [
    Paragraph("13 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First, every mitigation in this report taxes the victim.</b> Network harder, target "
        "smarter, re-credential locally, consider your own name — each is work assigned to the "
        "person who did nothing wrong. This report gives you the toolbox because you need it this "
        "year; it declines to pretend the toolbox is justice. The actual fix — audits, structured "
        "hiring, enforcement — belongs to employers and states, and the evidence shows it works "
        "when applied.", body),
    Paragraph(
        "<b>Second, the “be twice as good” covenant is broken, and we should say so.</b> The "
        "founding experiment found excellence under-rewarded for the wrong name; the British data "
        "found the penalty untouched by British birth and degrees. The generation that taught us to "
        "be twice as good was not wrong about the world; it was optimistic about which door the "
        "effort opens.", body),
    Paragraph(
        "<b>Third, the name is not the problem, and the framing matters.</b> Everything in this "
        "literature is a measurement of <i>employer behaviour</i>; it is routinely misread as "
        "advice that African names are liabilities to be managed. Our shame research described "
        "systems that punish people for what they are rather than what they did — this is one, "
        "industrialised. Whether you whiten a CV is a tactical question. Whether your name is a "
        "defect is not a question at all.", body),
    Paragraph("The experiments prove the bias sits in the reader, not the name. Plan for the reader "
              "you have — and refuse the conclusion that anything about your name needed "
              "forgiving.", pull),
]

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("14 · Method &amp; Limits", h2),
    Paragraph("This report reviews the published correspondence-study literature as at 24 August "
              "2026, selected for scale, replication and relevance to Africans abroad.", body),
]
story += bullets([
    "<b>Callbacks are not jobs.</b> Every result measures the first screen — the decision to make "
    "contact. Discrimination at interview, offer and salary stages is outside this method's reach, "
    "so these figures are a <i>floor</i> on the total penalty.",
    "<b>Most US studies test African-American names, not African ones.</b> “Lakisha” and “Adebayo” "
    "are different signals, and the US evidence transfers to African immigrants by inference. The "
    "studies that test this network's situation most directly are GEMM (Nigerian-origin applicants "
    "in Britain) and Oreopoulos (immigrant names and foreign credentials in Canada).",
    "<b>Fig 3 mixes sources and eras.</b> The nine-country figures are from the 2019 "
    "meta-analysis; the British 60% is from the single GEMM experiment; bars plot range midpoints. "
    "The ordering is robust; the decimals are not.",
    "<b>Fig 5's rates are approximate</b>, drawn from across Oreopoulos's study waves.",
    "<b>Fig 6 is an illustration.</b> The concentration finding is real and quantified in the "
    "papers; our bar chart depicts its shape, not their data.",
    "<b>Fictional applicants mean entry-level bias.</b> Senior hiring runs through networks and "
    "search firms, where the same forces are plausible but unmeasured by this method.",
    "<b>AI screening is the open frontier.</b> Most of this evidence predates algorithmic CV "
    "filtering at scale; early audits show name effects can persist or amplify, but the literature "
    "is young and we have not leaned on it.",
    "<b>Publication bias runs both ways.</b> The meta-analyses attempt corrections, and the "
    "headline gaps survive them. We cite meta-analyses over dramatic single studies wherever "
    "possible.",
    "<b>Nothing here is legal advice.</b> Name-based hiring discrimination is unlawful in the US, "
    "UK, EU and Canada. An employment lawyer, not this report, is the right reader of your "
    "specific case.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Bertrand &amp; Mullainathan, American Economic Review (2004); Quillian, Pager, Hexel &amp; "
        "Midtbøen, PNAS (2017); Quillian, Heath et al., Sociological Science (2019); Zwysen, Di "
        "Stasio &amp; Heath on the GEMM experiment, Sociology (2021); Kang, DeCelles, Tilcsik &amp; "
        "Jun, Administrative Science Quarterly (2016); Oreopoulos, NBER (2009/2011); Kline, Rose "
        "&amp; Walters, QJE (2022) and their Discrimination Report Card; Behaghel, Crépon &amp; Le "
        "Barbanchon on anonymous CVs in France (J-PAL). Full inline links in the web edition.",
        small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/name-on-the-cv-2026<br/>"
        "Companion reports: How Long Until It Was Worth It? · What Will People Say? · Three "
        "Generations to Silence<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
