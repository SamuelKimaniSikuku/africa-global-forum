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
IMG = os.path.join(HERE, "algorithm-at-the-border-2026", "img")
OUT = os.path.join(HERE, "algorithm-at-the-border-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "The Algorithm at the Border · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 8 September 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="The Algorithm at the Border (2026)",
                      author="Africa Global Forum",
                      subject="How AI is changing the African journey abroad, and what future students should know")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("The Algorithm", h1),
    Paragraph("at the border.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "The journey abroad that built this diaspora — apply, fly, study, work, settle — is "
        "being rewritten at every stage by AI. The visa file's first reader is now a machine "
        "with a documented history of bias. The detectors policing “AI cheating” falsely flag "
        "61% of honest non-native English essays. The junior jobs the study-to-settlement path "
        "runs through are down 19% for young workers in AI-exposed fields. And the same "
        "technology hands an applicant in Kisumu the best counselor any African student has "
        "ever had. The new terrain — and the rules that survive it.", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("61.3%", big_num), Paragraph("−19%", big_num),
    Paragraph("+1,300%", big_num), Paragraph("10", big_num),
], [
    Paragraph("of honest non-native English<br/>essays falsely flagged as<br/>“AI-written” by detectors", big_lbl),
    Paragraph("employment gap for young<br/>workers in AI-exposed jobs<br/>— the eroding entry rung", big_lbl),
    Paragraph("rise in deepfake hiring fraud<br/>in one year — the scam<br/>industry upgraded first", big_lbl),
    Paragraph("rules for future students<br/>that survive every scenario<br/>this report can see", big_lbl),
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
    fig("bottom_rung.png",
        "Fig 1 — The first hard payroll evidence on generative AI and jobs (Stanford, ADP "
        "data): it lands on the young, through hiring — the rung is removed before you reach "
        "it.", max_h=92 * mm),
    Paragraph("Published September 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/algorithm-at-the-border-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Every family in this network runs the same project at least once a generation: get one "
        "promising person through the door — admission, visa, degree, first job, papers. That "
        "pipeline was engineered for a world of human readers, human recruiters and human "
        "gatekeepers. That world is ending mid-project.", body),
]
story += bullets([
    "<b>The border already reads by machine, and its record is not neutral.</b> The UK "
    "scrapped its visa-streaming algorithm in 2020 days before a court challenge — it carried "
    "a secret nationality red-list feeding on its own past refusals. Canada's Chinook triages "
    "visa files at scale amid documented bulk-refusal concerns. The lesson is preparation, not "
    "paranoia: your file's first reader is software, so machine-legibility is now part of the "
    "application.",
    "<b>The tools policing “AI cheating” misfire on exactly our writers.</b> Stanford found "
    "GPT detectors falsely flagged 61.3% of human-written TOEFL essays — 97.8% by at least one "
    "detector — while passing US students' work. African applicants face a double bind: use AI "
    "and risk misconduct; write honestly and risk being flagged anyway. The defence is a paper "
    "trail.",
    "<b>The ladder's bottom rung is measurably eroding.</b> Employment for workers aged 22–25 "
    "in the most AI-exposed occupations is down 13% relative to peers — a gap near 19% by "
    "mid-2026 — through reduced hiring, concentrated where AI substitutes for tasks. The "
    "classic migrant route — study, junior role, sponsorship — runs directly through that "
    "rung. The route is not closed. It has moved.",
    "<b>The same technology is the biggest access upgrade African applicants have ever had</b> "
    "— counselor, scholarship scout, interview coach and editor in every pocket, on a "
    "continent where most schools never had a counselor — and simultaneously the scam "
    "industry's best tool ever: deepfake hiring fraud up 1,300% in a year, half a billion "
    "dollars in job-scam losses, a quarter of candidate profiles projected fake by 2028. Both "
    "faces are real. Learn both.",
    "<b>The deepest change is to the question itself.</b> With $1,000–$2,000/month remote "
    "AI-economy roles reaching Nairobi and Lagos and credential arbitrage dying, “how do I get "
    "out?” gives way to “what exactly am I moving for?” — and staying to build with AI becomes "
    "a genuine third option on the family whiteboard.",
])
story += [
    Paragraph("AI did not close the door abroad. It changed the locks — and handed out the "
              "picks unevenly. This report is about ending up on the right side of that "
              "distribution.", pull),
]

# ================= 02 =================
story += [
    PageBreak(),
    Paragraph("02 · The Door Becomes an Algorithm", h2),
    fig("door.png",
        "Fig 2 — The algorithmic border: the UK case, Canada's Chinook, and what it means for "
        "an applicant.", max_h=100 * mm),
    Paragraph(
        "For years the UK Home Office streamed visa applications with an algorithm that "
        "assigned risk partly by <b>a secret list of nationalities</b>; past refusals fed the "
        "risk scores that produced future refusals — a feedback loop laundering old bias as new "
        "data — until legal pressure forced it to be scrapped in August 2020. Canada's "
        "<b>Chinook</b> is officially “just” a productivity tool — and immigration lawyers "
        "document surging boilerplate refusals and worry officers rubber-stamp what the triage "
        "flags. The algorithms did not invent the bias our visa research already measured. "
        "They industrialised its throughput.", body),
    Paragraph(
        "What a future applicant does with this: <b>write for two readers</b> — clean scans, "
        "name spellings consistent across every document, dates that reconcile, funds evidence "
        "complete; a file that parses cleanly never gifts the triage a reason. <b>Assume no "
        "benefit of the doubt</b> — automation punishes ambiguity hardest, so the gap year and "
        "the unusual bank movement each get one clear written sentence. And <b>know the appeal "
        "culture of your destination</b> — a refusal generated in thirty seconds can take a "
        "year to overturn; corridor choice is now part of choosing a country at all.", body),
]

# ================= 03 =================
story += [
    PageBreak(),
    Paragraph("03 · The Essay Nobody Believes", h2),
    fig("detectors.png",
        "Fig 3 — Liang et al. (2023): the detectors misfire on exactly the writers African "
        "applicants are.", max_h=90 * mm),
    Paragraph(
        "Stanford researchers ran seven widely used GPT detectors over <b>human-written</b> "
        "TOEFL essays and over essays by US eighth-graders. The American children's work "
        "passed cleanly. The non-native writers' honest work was flagged as AI-generated "
        "<b>61.3% of the time on average — and 97.8% of essays were flagged by at least one "
        "detector</b>. The mechanism: detectors read plainer vocabulary and predictable "
        "phrasing as machine writing, and disciplined second-language English is exactly that. "
        "International students are already facing misconduct hearings on this evidence.", body),
    Paragraph(
        "The African applicant sits in a double bind nobody designed: <b>submit AI-polished "
        "work and risk genuine misconduct; submit your honest voice and risk being flagged as "
        "a machine anyway.</b> The defence is the paper trail: write in tools that keep "
        "version history — an edit log is a forensic record of human authorship; keep early "
        "drafts; be ready to discuss your essay fluently, because the interview about it is "
        "the one detector that works. And the strategic note: specific, lived, unpolishable "
        "detail is now an authentication strategy. The story only you could tell is the "
        "watermark no detector questions.", body),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · The Ladder Loses Its Bottom Rung", h2),
    Paragraph(
        "The African journey abroad has one canonical shape: study → graduate job → "
        "sponsorship → settlement. That path physically consists of <b>entry-level knowledge "
        "work</b>. Now the data (Fig 1): since late 2022, employment for workers aged 22–25 in "
        "the most AI-exposed occupations has fallen <b>13% relative to peers</b>, a gap near "
        "<b>19% by mid-2026</b>. Three details matter more than the headline: it operates "
        "through <b>reduced hiring, not layoffs</b> — the rung is removed before you reach it; "
        "it concentrates where AI <b>substitutes</b> for tasks, while complement-occupations "
        "are flat or rising; and it barely touches experienced workers — whose expertise the "
        "junior years were supposed to build.", body),
    Paragraph(
        "Against the migrant's position, the stakes sharpen: the graduate visa gives a fixed "
        "window to convert a degree into a sponsored job; our graduate-market research already "
        "showed that window narrowing, and the name discount compounds at the same gate. The "
        "single most important planning fact in this report: <b>the path is not closed — but "
        "the degree-to-anywhere bet is over.</b> What replaces it is the fork.", body),

    Paragraph("05 · The Jobs That Still Move", h2),
    fig("jobs_move.png",
        "Fig 4 — The fork: does AI substitute for the task, or amplify the person? "
        "Directional, not destiny."),
    Paragraph(
        "Durable: nursing, care and allied health (hands, judgement, shortage lists that write "
        "visas); the skilled trades — AI has no arms; engineering with a physical edge; and "
        "every role where AI is the professional's power tool while a <b>human</b> carries the "
        "licence and liability. Exposed: junior office work of every flavour, routine coding "
        "without systems depth, and services sold purely on labour cost. Two nuances: "
        "<b>fields are not fates</b> — the fork selects task-mixes, not titles, and an "
        "“exposed” degree held by someone who builds real systems with AI is stronger than "
        "ever. And the exposed column erodes at the <i>entry</i> tier — so the strategic "
        "question is: <b>can I reach the experienced tier before the junior tier finishes "
        "disappearing, and what proof will carry me across?</b>", body),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · The Counselor in Your Pocket", h2),
    fig("counselor.png",
        "Fig 5 — The access revolution: the largest upgrade in application infrastructure "
        "African students have ever had.", max_h=105 * mm),
    Paragraph(
        "The historic disadvantage of the African applicant was never talent; it was "
        "<b>information asymmetry</b> — no counselor (most African secondary schools have "
        "none), no network abroad, nobody to say fee waivers exist or that the “agent” "
        "charging three months' salary is selling free forms. AI collapses it: a student in "
        "Kisumu can research programmes like a private-school applicant of 2015 with a paid "
        "consultant; rehearse the visa interview fifty times before the one that counts; get "
        "draft-by-draft feedback that raises work to international standard while the words "
        "stay theirs; and fact-check every agent claim in minutes. The rules for using it "
        "without triggering Section 03's trap: <b>AI for everything except your voice.</b> "
        "Research, deadlines, rehearsal, critique — maximum. The essay that carries your "
        "story, the answers you give an officer, the person the committee meets — yours, "
        "verifiably. And for a community trained not to ask: an advisor that costs nothing, "
        "judges nothing and tells nobody is the lowest-shame ask that has ever existed.", body),

    PageBreak(),
    Paragraph("07 · The Scam Industry Upgrades First", h2),
    fig("scams.png",
        "Fig 6 — The con, industrialised. New technology reaches predators before "
        "institutions — every time.", max_h=100 * mm),
    Paragraph(
        "Deepfake fraud attempts in hiring rose ~1,300% in a year; US job-scam losses passed "
        "half a billion dollars; a quarter of candidate profiles are projected fake by 2028. "
        "The kit is cheap: cloned “HR” voices, interview faces that do not exist, offer "
        "letters typeset better than the real company's. The aimed-at population is ours — "
        "hungry for sponsorship, unfamiliar with destination norms, and trained not to admit "
        "being fooled. The defence fits on a card: <b>no legitimate employer or university "
        "ever charges you to be considered; no documents before independent verification; "
        "every offer confirmed on the company's own site — and post it in the group chat "
        "<i>before</i> paying anything, not after.</b> A “is this real?” channel is the "
        "cheapest life-saving infrastructure a diaspora network can run.", body),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · Do You Still Need to Move?", h2),
    fig("still_move.png",
        "Fig 7 — The question changes shape. For the first time, staying-and-building is a "
        "real third option."),
    Paragraph(
        "Some classic drivers are weakening: the information advantage of being abroad now "
        "fits in a phone; remote AI-economy work reaches African cities — from $2/hour "
        "annotation labour (the exploitative half of the story) to structured $1,000–$2,000/"
        "month roles open to Kenya, Nigeria and Ghana — salaries beating many local graduate "
        "jobs without a visa queue; and the credential-arbitrage era is closing. But the case "
        "for moving has not dissolved — it has <b>specified</b>: institutions still live "
        "somewhere; licensed professions must be practised where the licence is; networks and "
        "luck surface-area do not videoconference; and the passport remains stubbornly "
        "geographic. <b>“Abroad” has stopped being a goal and become a tool</b> — the family "
        "whiteboard now has three honest options: go, stay-and-build, or sequence both.", body),

    Paragraph("09 · The Two Readers of Your Name", h2),
    Paragraph(
        "Our library measured the human version: identical CVs, African names, half the "
        "callbacks. Now the screening is increasingly algorithmic. The pessimistic case has "
        "receipts — models trained on biased hiring learn the bias as signal, and an algorithm "
        "rejecting at scale does in an afternoon what a thousand prejudiced screeners did in a "
        "year, with nothing to appeal. The optimistic case is also real: <b>a machine reads "
        "structure, not melanin</b> — a well-audited screen can be blinder than the humans it "
        "replaced. Practical consequences: format for the parser (standard headings, keywords "
        "from the posting, no CV-in-a-graphic); evidence every requirement explicitly; and "
        "treat referrals as the algorithm bypass they are — the human-vouched candidate skips "
        "the machine gate, which makes network-building <i>more</i> valuable in the AI era, "
        "not less. The old game was surviving one biased reader. The new game is being "
        "legible to two.", body),
]

# ================= 10 =================
story += [
    PageBreak(),
    Paragraph("10 · What Future Students Should Know", h2),
    fig("rules.png",
        "Fig 8 — The five rules that survive every scenario — and five more below.",
        max_h=105 * mm),
]
story += bullets([
    "<b>6. Aim past the entry rung.</b> Graduate <i>above</i> junior: internships, research "
    "assistantships, shipped projects, a portfolio proving you already do the work "
    "AI-assisted. In a market that under-hires the inexperienced, arrive pre-experienced.",
    "<b>7. Put licensing on the durable path.</b> If your field has a licence (health, "
    "engineering, trades, teaching), it is the moat AI cannot cross and the visa list loves — "
    "start the credential-recognition maze <i>before</i> you fly. The two-week rule applies "
    "to the conversion paperwork from day one.",
    "<b>8. Choose corridors, not just countries.</b> Weigh automation-and-appeal culture, the "
    "post-study window against the rung erosion, and the shortage lists.",
    "<b>9. Keep your African network warm — it is now an asset, not a fallback.</b> With "
    "stay-and-build real and return migration rising, the classmates in Nairobi and Accra are "
    "future co-founders and clients. The next decade's advantage is being bilingual in both "
    "economies.",
    "<b>10. Own the story AI cannot write.</b> Your specific life is your essay's watermark, "
    "your interview's spine, and the one input to your career no model has in training data. "
    "Guard it, tell it yourself, never outsource it.",
])

# ================= 11 & 12 =================
story += [
    PageBreak(),
    Paragraph("11 · What Parents and Sponsors Should Know", h2),
    Paragraph(
        "<b>The investment logic has inverted: field now beats destination.</b> A decade ago, "
        "“any university abroad” was a rational bet; today a nursing or engineering path at a "
        "modest institution beats a generic business degree at a famous one, because the rung "
        "the generic degree fed into is the one AI is eating. Before the family funds "
        "anything, ask the fork question of the intended career — substitute or amplify? "
        "<b>Budget for the licence, not just the degree</b> — the conversion exams and "
        "registration fees that turn a qualification into employability are the tranche "
        "families most often fail to plan. <b>Assume the payback horizon has lengthened</b> — "
        "expecting remittances in year one puts the student in the exact vice our black-tax "
        "research priced. And take stay-and-build seriously enough to price it: the same "
        "tuition sum behind a determined young person with AI leverage in Nairobi or Kigali "
        "is no longer an obviously worse bet. That sentence would have been irresponsible in "
        "2015. It is due diligence now.", body),

    Paragraph("12 · The African Advantage", h2),
    Paragraph(
        "Africa is the youngest continent on earth — median age about nineteen — entering the "
        "AI era with the fewest legacy systems to defend and the deepest bench of the "
        "demographic that adopts new tools fastest. We have run this play before: the "
        "continent that skipped landlines for M-Pesa and desktop for the phone-first internet "
        "is structurally practised at leapfrogging — and AI is the most leapfroggable "
        "technology yet, because its capital requirement is a connection and its interface is "
        "language.", body),
    Paragraph(
        "The diaspora's position is the closing reframe: the person who studies abroad in the "
        "AI era and stays bilingual in both economies is not a brain drained — they are <b>a "
        "bridge with compound interest</b>: the nurse who trains in Manchester and "
        "teleconsults for Mombasa; the engineer who ships for Berlin and co-founds in Kigali; "
        "the student who arrives with the counselor-in-pocket and becomes the counselor for "
        "fifty cousins. Every previous technology wave reached Africa last, priced for "
        "others. This one is in a phone in Kisumu on launch day, speaks Swahili, and answers "
        "questions at 2 a.m. for free.", body),
]

# ================= 13 =================
story += [
    PageBreak(),
    Paragraph("13 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First: the era of the credential shortcut is over, and some of the family "
        "playbook dies with it.</b> For two generations, “a degree from abroad” was itself "
        "the asset. That arbitrage is closing from both ends: AI erodes the jobs generic "
        "credentials fed, and employers price proof over paper. Families still selling land "
        "for a master's-any-master's are buying the previous war's weapon. The sacrifice "
        "logic survives; the target must move.", body),
    Paragraph(
        "<b>Second: our own shortcuts feed the machine that flags our honest kids.</b> Every "
        "AI-fabricated application and ghost-written SOP from our corridors trains the "
        "suspicion systems — and Section 03 showed who those systems then misfire on: the "
        "honest non-native writer. The agent industry's pivot to “AI application packages” is "
        "borrowing against the credibility of every applicant who shares your passport. The "
        "community that polices its own scammers is doing border policy for its own "
        "children.", body),
    Paragraph(
        "<b>Third: AI changes the odds, not the politics.</b> No prompt fixes a visa quota, a "
        "red list, or the name discount; the algorithms encode the politics that built them, "
        "and the counselor in your pocket does not sit on the appeals board. The failure "
        "modes are symmetrical — despair that ignores the new tools, and hype that ignores "
        "the old walls. The strategy that survives both: <b>use every tool fully, count every "
        "cost honestly, and build with witnesses.</b> Which is, not coincidentally, what a "
        "Forum is for.", body),
]

# ================= 14 =================
story += [
    PageBreak(),
    Paragraph("14 · Method &amp; Limits", h2),
    Paragraph("This report combines documented migration automation, the first payroll-data "
              "studies of generative AI's employment effects, AI-detection research and fraud "
              "statistics, as at 8 September 2026 — with a larger-than-usual caution flag, "
              "because it is partly a futures report.", body),
]
story += bullets([
    "<b>This is the most forward-looking report in this library, and it will age fastest.</b> "
    "Directional claims are marked directional; the advice is limited to rules that survive "
    "multiple scenarios.",
    "<b>The border-automation cases are documented</b> (the UK tool's 2020 withdrawal under "
    "legal challenge; Chinook and the immigration bar's recorded concerns), but governments "
    "disclose little; the “spreading everywhere” claim rests on procurement records and legal "
    "commentary, not a comprehensive audit.",
    "<b>The detector findings</b> (61.3% average false-positive on TOEFL essays; 97.8% by at "
    "least one of seven detectors) are Liang et al. (2023), Patterns. Detectors have iterated "
    "since; the structural mechanism (low perplexity) is unchanged. Turnitin specifically was "
    "not in the study.",
    "<b>The employment findings</b> are Brynjolfsson, Chandar &amp; Chen (Stanford; ADP "
    "payroll data): US data, one large provider, relative not absolute decline; European "
    "graduate markets are assumed to rhyme rather than measured here.",
    "<b>The scam figures</b> come from industry and regulator reporting of varying rigour; we "
    "use them for scale and direction. The three defence rules do not depend on the numbers.",
    "<b>Sections 09–12 are interpretive syntheses</b> connecting this data to our library's "
    "measured findings, labelled as argument. The ten rules are judgement built on cited "
    "evidence, not study findings.",
    "<b>Disclosure, in this report above all: AI was used in its production</b> — for search, "
    "drafting and chart generation — under this library's editorial, source-verification and "
    "honest-limits standards. We hold the position we recommend: maximum tool, human voice, "
    "receipts kept.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Foxglove/JCWI and contemporary reporting on the UK visa-streaming algorithm; the "
        "International Bar Association on Chinook; Liang et al. (2023) on GPT-detector bias "
        "and The Markup on accused international students; Brynjolfsson, Chandar &amp; Chen, "
        "“Canaries in the Coal Mine” (Stanford Digital Economy Lab) and its 2026 update; FTC "
        "job-scam data and Gartner projections via industry reporting; Qhala on African data "
        "workers; and this library's prior measurement in the CV, visa, student-cost, "
        "graduate-market and AI-landscape reports. Full inline links in the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, "
        "sit together, and bounce ideas. This research is part of an open library, free to "
        "read and share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/algorithm-at-the-border-2026<br/>"
        "Companion reports: The Name on the CV · The Visa Treadmill · Best Countries for "
        "African Students · How Long Until It Was Worth It?<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
