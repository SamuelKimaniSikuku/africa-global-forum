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
IMG = os.path.join(HERE, "losing-the-language-2026", "img")
OUT = os.path.join(HERE, "losing-the-language-2026.pdf")

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
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10.5 * mm, "Losing the Language · 2026")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20 * mm, 10 * mm,
                      "africaglobalforum.com  ·  Data as at 19 August 2026  ·  Free to read and share")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=24 * mm, bottomMargin=18 * mm,
                      title="Three Generations to Silence (2026)",
                      author="Africa Global Forum",
                      subject="How the African diaspora loses its languages, and what actually keeps them")
frame = Frame(doc.leftMargin, doc.bottomMargin, CONTENT_W,
              A4[1] - doc.topMargin - doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=furniture)])


story = []

# ================= COVER =================
story += [
    Spacer(1, 4 * mm),
    Paragraph("AGF RESEARCH · FACT-CHECKED · 2026", label),
    Paragraph("Three Generations", h1),
    Paragraph("to silence.",
              S("sub", fontName="Helvetica-Oblique", fontSize=19, leading=23,
                textColor=TERRACOTTA, spaceAfter=8)),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=10),
    Paragraph(
        "Somewhere there is a grandmother who cannot have a conversation with her grandchildren. "
        "Nobody decided this. It happened one convenient English sentence at a time. The research "
        "says it takes <b>three generations</b> for a migrating family to lose its language — and "
        "that African families are losing theirs <b>faster than almost anyone else.</b>", lede),
    Spacer(1, 2 * mm),
]

kpi = Table([[
    Paragraph("3", big_num), Paragraph("25%", big_num),
    Paragraph("428", big_num), Paragraph("477k", big_num),
], [
    Paragraph("generations from fluency<br/>to silence", big_lbl),
    Paragraph("of African immigrants in the US<br/>speak only English at home<br/>(all immigrants: 16%)", big_lbl),
    Paragraph("threatened languages<br/>in Africa (UNESCO)", big_lbl),
    Paragraph("people learning Swahili<br/>on Duolingo", big_lbl),
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
    fig("three_generations.png",
        "Fig 1 — The three-generation pattern of heritage language loss, documented across "
        "immigrant groups. Bar heights are illustrative; the stages are from the research "
        "literature.", max_h=90 * mm),
    Paragraph("Published August 2026 by Africa Global Forum · "
              "africaglobalforum.com/reports/losing-the-language-2026", small),
    PageBreak(),
]

# ================= 01 =================
story += [
    Paragraph("01 · The Short Version", h2),
    Paragraph(
        "Every diaspora family knows the scene. The parents speak Yoruba, or Twi, or Amharic, or "
        "Somali to each other. They speak English to the children — for good reasons, at the time. "
        "The children understand the language but answer in English. The grandchildren get "
        "greetings, food words, and the songs. The conversation is gone.", body),
]
story += bullets([
    "<b>The pattern is documented and it is universal.</b> Across immigrant groups, the home "
    "language is fluent in the <b>first generation</b>, understood-but-not-spoken in the "
    "<b>second</b>, and gone by the <b>third</b>. The landmark study in <i>Demography</i> called it "
    "“only English by the third generation.”",
    "<b>African families are on the fast track.</b> <b>25%</b> of sub-Saharan African immigrants in "
    "the US speak <i>only English</i> at home — against <b>16%</b> of all immigrants. For Liberians "
    "it is <b>68%</b>; for South Africans, <b>56%</b>. The colonial language head start becomes a "
    "heritage language handicap.",
    "<b>The loss happens earlier than the folklore says.</b> The literature says the third "
    "generation loses the language, but <b>the shift happens in the second</b>: in a comparable UK "
    "study of second-generation children, most understood their heritage language, yet <b>fewer "
    "than a third spoke it with their own siblings</b>.",
    "<b>The languages are not safe at home either.</b> UNESCO counts roughly <b>428 threatened "
    "languages in Africa</b> and classifies <b>Igbo as endangered despite ~20 million speakers</b>. "
    "The diaspora is not losing something the homeland will keep for it.",
    "<b>The regret is measurable.</b> Over <b>477,000 people</b> are learning Swahili on Duolingo; "
    "apps like Nkenne exist purely to teach diaspora adults the languages their childhood homes "
    "stopped speaking.",
    "<b>And keeping the language costs almost nothing.</b> The practices that work — a stated "
    "home-language policy, grandparents as immersion, requiring children to <i>answer</i> in the "
    "language — are free. What they cost is consistency.",
])
story += [
    Paragraph("A language does not die in an argument. It dies in convenience — one "
              "answered-in-English question at a time, in homes full of love.", pull),
]

# ================= 02 =================
story += [
    PageBreak(),
    Paragraph("02 · The Rule of Three Generations", h2),
    Paragraph(
        "This is one of the most consistently replicated findings in the study of migration. The "
        "landmark analysis in <i>Demography</i> examined the grandchildren of immigrants to the "
        "United States and asked whether any group escaped the pattern. Essentially none did. The "
        "first generation speaks the mother tongue. The second is bilingual on paper — but tilted, "
        "using the heritage language with parents and the dominant language everywhere else. The "
        "third generation speaks English, full stop. Fig 1 on the cover shows the shape.", body),
]
story += bullets([
    "<b>It does not require anyone to reject anything.</b> No generation decides to abandon the "
    "language. Each makes locally sensible choices — English for school, English for friends, "
    "English because it is faster — and the sum of sensible choices is extinction in the home.",
    "<b>It survives love, pride and intention.</b> Families that treasure their culture lose the "
    "language on the same schedule as families that do not, unless they change specific behaviours. "
    "Sentiment is not transmission.",
    "<b>It is a default, not a destiny.</b> The same literature documents the exceptions — and the "
    "exceptions share practices, not feelings.",
])

# ================= 03 =================
story += [
    Paragraph("03 · The African Paradox", h2),
    fig("english_only.png",
        "Fig 2 — Share of immigrants speaking only English at home, from Migration Policy "
        "Institute analysis of US Census data."),
    Paragraph(
        "Here is the finding this report exists for. You would expect a diaspora as proudly "
        "cultural as Africa's to hold its languages at least as well as other groups. The census "
        "data says the opposite.", body),
    Paragraph(
        "<b>A quarter of sub-Saharan African immigrants in the US speak only English at home</b>, "
        "against 16% of all immigrants. Where English is an official language of the origin "
        "country, the numbers jump: <b>68% of Liberian</b> and <b>56% of South African</b> "
        "immigrants keep no other language in the house at all. Note what this measures — not the "
        "children's ability, but <i>the first generation's own choice of home language</i>. For "
        "many African families the three-generation clock starts a generation early, because "
        "generation one has already switched.", body),
    Paragraph(
        "The mechanism is colonial history doing quiet work. In most of anglophone Africa, English "
        "was already the language of school, exams, offices and status <i>before anyone "
        "emigrated</i>. Parents were educated in it, succeeded through it, and often associate the "
        "home language with the village and English with advancement. Emigration did not introduce "
        "that hierarchy. It just removed the last environments where the home language was "
        "necessary.", body),
    Paragraph("Other diasporas must learn the new country's language. African families often "
              "arrive already fluent in it — a huge advantage for the parents' careers, and "
              "quietly fatal for the grandmother's conversations.", pull),
]

# ================= 04 =================
story += [
    PageBreak(),
    Paragraph("04 · Where the Shift Actually Happens", h2),
    Paragraph(
        "The folklore says the third generation loses the language. The research is more precise, "
        "and more useful: <b>the third generation is where the loss becomes visible. The shift "
        "itself happens in the second — and inside the first generation's own home.</b>", body),
]
story += bullets([
    "<b>The gap is production, not comprehension.</b> In a UK study of second-generation South "
    "Asian children — the closest well-measured comparator — most understood their heritage "
    "language, yet <b>fewer than a third spoke it with their own siblings</b>. A child who "
    "understands but always answers in English is not bilingual. They are a fluent listener in a "
    "language they will not pass on.",
    "<b>Parents drive it, meaning well.</b> Research on immigrant families repeatedly finds parents "
    "switching to English with their children out of concern for school success — despite the "
    "evidence that the home language does not hold children back.",
    "<b>Siblings finish it.</b> Once children speak English to each other, the heritage language "
    "loses its last daily arena. Studies of African immigrant households find a child's English "
    "dominance rises with the number of other English-proficient children in the house.",
])
story += [
    Paragraph(
        "The practical conclusion is sharp: <b>by the time a family notices the loss — usually when "
        "a grandparent visits — the decisive years are already behind them.</b> The window is early "
        "childhood, and the lever is not whether children <i>hear</i> the language but whether they "
        "are required to <i>produce</i> it.", body),

    Paragraph("05 · Not Safe at Home Either", h2),
    fig("endangered_home.png",
        "Fig 3 — Language endangerment on the continent. UNESCO figures and Nigerian linguistic "
        "surveys; counts of this kind vary by methodology."),
    Paragraph(
        "UNESCO counts roughly <b>428 threatened languages in Africa</b> and warns that up to 10% "
        "of the continent's languages may vanish within a century. In Nigeria alone, around <b>400 "
        "minority dialects are considered endangered, 152 of them facing extinction</b>. And the "
        "headline case: <b>UNESCO classifies Igbo as endangered</b> — a language with roughly <b>20 "
        "million speakers</b> — because in urban Nigeria, English-medium schooling and status "
        "economics mean many Igbo children can no longer hold a conversation in it. The same force "
        "operating in Peckham operates in Lagos and Enugu.", body),
    Paragraph(
        "This changes what the diaspora's choice means. For the big languages — Swahili, Hausa, "
        "Amharic — the homeland reservoir may hold. For hundreds of others, <b>the diaspora is not "
        "losing its copy of something safely archived. It is losing one of the last copies.</b>",
        body),
]

# ================= 06 =================
story += [
    PageBreak(),
    Paragraph("06 · What Is Actually Lost", h2),
    fig("untranslatable.png",
        "Fig 4 — A language is a set of ideas, not a set of labels. Glosses are simplified — each "
        "of these words carries more than one line can hold."),
]
story += bullets([
    "<b>The grandparent relationship.</b> Where the grandparents' English is limited, the language "
    "is the relationship — and the child who loses one loses the other. No later app course "
    "restores a childhood of conversations that did not happen.",
    "<b>Concepts with no English container.</b> Our report on shame turned on exactly this: Hausa "
    "<i>kunya</i> names both a sanction and a virtue, and the English word “shame” cannot carry "
    "that. A child raised only in English does not just lack the word — they lack easy access to "
    "the idea.",
    "<b>The oral archive.</b> Proverbs, praise names, the grandmother's stories, the jokes that "
    "only land in the original. African cultures carried disproportionate amounts of their "
    "knowledge orally; each generation that cannot listen is a wing of the archive closing.",
    "<b>Standing in the homeland.</b> The diaspora child who returns without the language is "
    "legible to everyone as a visitor — including to themselves.",
])

# ================= 07 =================
story += [
    PageBreak(),
    Paragraph("07 · The Cognitive Question", h2),
    fig("bilingual_evidence.png",
        "Fig 5 — The state of the bilingual-advantage evidence, honestly divided."),
    Paragraph(
        "<b>What holds up:</b> a quantitative synthesis finds bilingual children outperform "
        "monolinguals on executive-function tasks <b>far more often than chance</b>, with the "
        "clearest effects on inhibition and cognitive flexibility. And the fear that drives the "
        "switch — that the home language will hold a child back in English — finds no support.",
        body),
    Paragraph(
        "<b>What is contested:</b> several studies find the advantage vanishes on working-memory "
        "measures; recent work reports null or mixed effects; and socioeconomic status confounds "
        "some of the classic results. The honest reading is that the cognitive bonus is <b>real but "
        "modest and inconsistent</b> — a tailwind, not a superpower.", body),
    Paragraph("Which is fine, because the case never rested on IQ points. The strongest facts are "
              "simpler: the second language costs a child nothing academically, and it buys a "
              "grandmother.", pull),
]

# ================= 08 =================
story += [
    PageBreak(),
    Paragraph("08 · The Regret Market", h2),
    fig("regret_market.png",
        "Fig 6 — Adults queuing to learn what childhood homes stopped teaching. Duolingo learner "
        "counts as reported; Nkenne's course list from the company."),
    Paragraph(
        "<b>Over 477,000 people are learning Swahili on Duolingo</b>, and over 30,000 are learning "
        "Zulu. Nkenne — an app built explicitly for the diaspora — teaches nine African languages, "
        "including Igbo, Yoruba, Twi, Hausa, Somali and Amharic. A market has formed around adult "
        "heritage learners: people in their twenties and thirties buying back, at app speed and "
        "subscription prices, what their households once had for free.", body),
    Paragraph(
        "Two readings, both true. The optimistic one: demand exists, tools exist, and revival is a "
        "real movement. The sober one: <b>the demand arrives one generation after the supply was "
        "cut</b>, and an app can deliver vocabulary but not the accent, the idiom, or the years of "
        "dinner-table repetition. The regret market is real precisely because the cheap window "
        "closed.", body),

    Paragraph("09 · Why African Languages Get No Help", h2),
    fig("why_it_happens.png",
        "Fig 7 — The mechanism, assembled from the transmission literature and community accounts."),
    Paragraph(
        "The deepest is the first: <b>the prestige hierarchy predates migration.</b> A Polish "
        "family in Chicago never regarded Polish as the low-status language of their own home. Many "
        "African families, schooled under systems where speaking the mother tongue in class was "
        "punished, did — and carried that ranking abroad intact.", body),
    Paragraph(
        "The most fixable is the third: <b>infrastructure.</b> Greek, Chinese, Polish and Tamil "
        "communities built Saturday-school systems that industrialise transmission. African "
        "languages largely lack the equivalent, partly because of the fourth problem: a “Nigerian "
        "community” of ten thousand people is a Yoruba community, an Igbo community, a Hausa "
        "community and a dozen smaller ones, none individually large enough to staff a school.",
        body),
    Paragraph(
        "And the fifth reason is our shame research wearing a smaller coat: the child who attempts "
        "the language and gets laughed at learns that <i>attempting it badly is more shameful than "
        "not attempting it</i>. A system that punishes visible imperfection produces silence here "
        "exactly as it produces silence in clinics.", body),
]

# ================= 10 =================
story += [
    Paragraph("10 · What Actually Works", h2),
    fig("what_works.png",
        "Fig 8 — The practices that recur among families who kept the language. "
        "Evidence-informed, not clinically tested."),
    Paragraph(
        "The research on families that beat the three-generation rule converges on something almost "
        "annoyingly simple: <b>they replaced drift with policy.</b> Say the rule out loud. Deploy "
        "the grandparents — a monolingual grandparent is the best language teacher a family will "
        "ever have, and video calls make this free across continents. Require production, not just "
        "exposure: when the child answers in English, the parent replies — kindly, boringly, "
        "forever — in the language. Use the media the diaspora already owns. And build tiny "
        "institutions: a Saturday class needs two families, one fluent adult and a room.", body),
    Paragraph(
        "Note what is absent from the list: money. Every item is free or nearly so. The binding "
        "constraint is not resources. It is the daily willingness to be the slightly awkward "
        "household that answers English questions in Yoruba.", body),

    Paragraph("11 · If You Are Raising Children Abroad", h2),
]
story += bullets([
    "<b>Start before it feels necessary.</b> The decisive window is early childhood, and the loss "
    "is invisible until a grandparent visit reveals it. If your child answers you in English "
    "today, the clock is already running.",
    "<b>Do not fear for their English.</b> Their English is guaranteed by the entire society "
    "around them. You are the only supplier of the other language they will ever have.",
    "<b>Protect the attempt.</b> The accent will be imperfect and the grammar will wobble. The "
    "child who is laughed at stops. One firm sentence to the laughing auntie is worth a year of "
    "lessons.",
    "<b>Understanding is not the goal — speaking is.</b> A house where children understand but "
    "answer in English feels bilingual and is one generation from silence.",
    "<b>If the language is small, write things down.</b> Record the grandparents — stories, "
    "proverbs, names, songs. A phone and an afternoon creates an archive that will otherwise not "
    "exist.",
    "<b>And if you are second-generation and it is already gone:</b> partial recovery — enough for "
    "the phone calls, enough for the visit — is a realistic goal. Fluency-or-nothing is the "
    "perfectionism that caused the problem.",
])

# ================= 12 =================
story += [
    PageBreak(),
    Paragraph("12 · The Uncomfortable Part", h2),
    Paragraph(
        "<b>First, the parents who switched were not careless.</b> They were often obeying the "
        "explicit advice of teachers and doctors, in decades when professionals wrongly told "
        "immigrant families that two languages would confuse a child. Others were protecting "
        "children from playground racism aimed at the accent. The generation that lost the language "
        "was, in most cases, trying to give its children the country. Blame is not just unkind "
        "here; it is inaccurate.", body),
    Paragraph(
        "<b>Second, the economics are genuinely against the language.</b> This library documents, "
        "report after report, that English is what the global economy pays for. A parent who "
        "prioritises English is reading the incentives correctly. The case for the home language is "
        "not economic and should not pretend to be. It is about who the child gets to be, and who "
        "they get to talk to.", body),
    Paragraph(
        "<b>Third, the child gets a vote.</b> Some second-generation adults do not mourn the "
        "language, and resent the suggestion that they are incomplete without it. Heritage is an "
        "inheritance, not an obligation — and a report like this walks close to the same “what will "
        "people say” machinery we criticised elsewhere. The honest position: the loss is real, the "
        "grief many feel is real, and so is the right to feel neither.", body),
    Paragraph("The window closes quietly, and it closes early. Whatever a family decides, it should "
              "be a decision — because the default has already been decided, and it is silence in "
              "three generations.", pull),
]

# ================= 13 =================
story += [
    PageBreak(),
    Paragraph("13 · Method &amp; Limits", h2),
    Paragraph("This report assembles published research as at 19 August 2026 on heritage language "
              "shift, applied to Africans abroad.", body),
]
story += bullets([
    "<b>Fig 1's bar heights are illustrative.</b> The three-generation pattern is robustly "
    "documented; the specific proportions surviving at each stage vary by group and study, and we "
    "have deliberately not invented precise numbers for them.",
    "<b>The “fewer than a third speak it with siblings” figure is from second-generation South "
    "Asian children in the UK</b>, used as the best-measured comparator. No equivalent large study "
    "of African-language transmission in the diaspora exists — which is itself a finding. Treat "
    "the number as indicative of the second-generation pattern, not as a measurement of African "
    "families.",
    "<b>The English-only-at-home figures measure household language use, not children's "
    "ability</b>, and they aggregate wildly different situations — a Liberian family for whom "
    "English genuinely is the mother tongue is counted alongside a Yoruba family that switched. "
    "The 25% average still sits far above the all-immigrant 16%.",
    "<b>Endangerment counts vary by source and method.</b> UNESCO's ~428, Nigeria's ~400 dialects "
    "and the 152 facing extinction come from different exercises with different definitions. Use "
    "them as orders of magnitude. The Igbo classification is UNESCO's and is contested by some "
    "Nigerian linguists.",
    "<b>The bilingual-advantage literature is presented divided because it is divided.</b> We have "
    "shown the contested column at the same size as the supported one deliberately.",
    "<b>Section 10 is evidence-informed, not trial-tested.</b> The practices come from the "
    "transmission literature and documented family strategies; no randomised study proves any "
    "specific bundle.",
    "<b>The four words in Fig 4 are simplified glosses</b> by non-speakers relying on published "
    "discussions. Speakers of these languages will have corrections — which we would genuinely "
    "welcome.",
    "<b>Duolingo learner counts</b> are platform-reported totals of course enrolments, not active "
    "or diaspora-specific learners.",
])
story += [
    Paragraph("Principal sources", h3),
    Paragraph(
        "Alba et al., Demography, on the three-generation pattern; Migration Policy Institute on "
        "home language use among sub-Saharan African immigrants; research on household context and "
        "English proficiency among children of African immigrants; University of Alberta and the "
        "International Journal of Bilingualism on second-generation speaking patterns; UNESCO "
        "endangerment figures and research on Igbo endangerment; quantitative synthesis of "
        "bilingual executive-function research and the PRISMA systematic review; Duolingo and "
        "reporting on African language courses; Nkenne's published course list. Full inline links "
        "in the web edition.", small),
    Spacer(1, 4 * mm),
    HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2),
    callout(
        "<b>Africa Global Forum</b> is a peer network for Africans abroad — help each other, sit "
        "together, and bounce ideas. This research is part of an open library, free to read and "
        "share. The Forum itself is by application.<br/><br/>"
        "Read the web edition with live source links: "
        "africaglobalforum.com/reports/losing-the-language-2026<br/>"
        "Companion reports: What Will People Say? · Navigating Cultural Identity · How Long Until "
        "It Was Worth It?<br/>"
        "Apply to join: africaglobalforum.com", bg=INK),
]

doc.build(story)
print("wrote", OUT)
