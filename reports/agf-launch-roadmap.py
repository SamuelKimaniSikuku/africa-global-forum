#!/usr/bin/env python3
"""Generate the AGF 90-Day Launch Roadmap PDF (branded)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, KeepTogether
)

# ---- AGF brand palette ----
INK       = colors.HexColor("#0E0B08")
PAPER     = colors.HexColor("#F4EFE6")
TERRACOTTA= colors.HexColor("#C8421A")
OCHRE     = colors.HexColor("#D89B2C")
RUST      = colors.HexColor("#7A2E12")
FOREST    = colors.HexColor("#2A3D2A")
MUTED     = colors.HexColor("#6B635A")
LIGHT     = colors.HexColor("#EAE2D4")
WHITE     = colors.white

OUT = "/Users/kiman/africa-global-forum/reports/AGF-Launch-Roadmap.pdf"

styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

body      = S("body", fontName="Helvetica", fontSize=9.5, leading=14, textColor=INK, spaceAfter=6)
body_w    = S("body_w", fontName="Helvetica", fontSize=8.7, leading=12.5, textColor=INK)
body_w_wh = S("body_w_wh", fontName="Helvetica", fontSize=8.7, leading=12.5, textColor=WHITE)
h1        = S("h1", fontName="Helvetica-Bold", fontSize=20, leading=23, textColor=INK, spaceBefore=6, spaceAfter=4)
h2        = S("h2", fontName="Helvetica-Bold", fontSize=13.5, leading=16, textColor=TERRACOTTA, spaceBefore=14, spaceAfter=4)
h3        = S("h3", fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=RUST, spaceBefore=8, spaceAfter=3)
label     = S("label", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=OCHRE, spaceAfter=2)
small     = S("small", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MUTED)
th        = S("th", fontName="Helvetica-Bold", fontSize=8.7, leading=11, textColor=WHITE)
cell      = S("cell", fontName="Helvetica", fontSize=8.7, leading=12, textColor=INK)
cell_b    = S("cell_b", fontName="Helvetica-Bold", fontSize=8.7, leading=12, textColor=INK)
kpi_num   = S("kpi_num", fontName="Helvetica-Bold", fontSize=15, leading=17, textColor=TERRACOTTA, alignment=TA_CENTER)
kpi_lbl   = S("kpi_lbl", fontName="Helvetica", fontSize=7.6, leading=9.5, textColor=INK, alignment=TA_CENTER)

def bullet_list(items, st=body):
    rows = []
    for it in items:
        rows.append(Paragraph(f'<font color="#C8421A">&bull;</font>&nbsp;&nbsp;{it}', st))
    return rows

# ---------- page furniture ----------
def header_footer(canvas, doc):
    canvas.saveState()
    # paper background
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # top band
    canvas.setFillColor(INK)
    canvas.rect(0, A4[1]-16*mm, A4[0], 16*mm, fill=1, stroke=0)
    canvas.setFillColor(OCHRE)
    canvas.rect(0, A4[1]-16.8*mm, A4[0], 0.8*mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(18*mm, A4[1]-10.5*mm, "AFRICA GLOBAL FORUM")
    canvas.setFillColor(OCHRE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(A4[0]-18*mm, A4[1]-10.5*mm, "90-Day Launch Roadmap")
    # footer
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(18*mm, 10*mm, "africaglobalforum.com  ·  Created among ourselves, first.")
    canvas.drawRightString(A4[0]-18*mm, 10*mm, f"Page {doc.page}")
    canvas.restoreState()

def make_table(data, col_widths, header=True, zebra=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    cmds = [
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LINEBELOW", (0,0), (-1,-1), 0.4, LIGHT),
    ]
    if header:
        cmds += [
            ("BACKGROUND", (0,0), (-1,0), TERRACOTTA),
            ("LINEBELOW", (0,0), (-1,0), 0, WHITE),
        ]
    if zebra:
        start = 1 if header else 0
        for r in range(start, len(data)):
            if (r-start) % 2 == 1:
                cmds.append(("BACKGROUND", (0,r), (-1,r), WHITE))
    t.setStyle(TableStyle(cmds))
    return t

# ---------- build story ----------
story = []

# Title block
story.append(Spacer(1, 6*mm))
story.append(Paragraph("SEASON 01 · LAUNCH PLAN", label))
story.append(Paragraph("90-Day Launch Roadmap", h1))
story.append(Paragraph("From a live site to an active diaspora network &mdash; late June to end of September 2026.", small))
story.append(Spacer(1, 3*mm))
story.append(HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=6))

# North star box
ns = Table([[
    Paragraph('<b>North-star goal.</b>&nbsp; Go from a live site with a "coming soon" form to an open, '
              'application-based network with an active founding cohort &mdash; proving all three engagements '
              '(<b>Help &amp; Be Helped</b>, <b>You Are Not Alone</b>, <b>Bounce Ideas</b>) actually work before you scale.<br/><br/>'
              '<b>Launch definition.</b>&nbsp; Season 01 publicly open, ~50&ndash;100 founding members onboarded, at least '
              'one of each engagement run successfully, and a repeatable weekly rhythm.', body_w_wh)
]], colWidths=[170*mm])
ns.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), FOREST),
    ("LEFTPADDING",(0,0),(-1,-1),12), ("RIGHTPADDING",(0,0),(-1,-1),12),
    ("TOPPADDING",(0,0),(-1,-1),10), ("BOTTOMPADDING",(0,0),(-1,-1),10),
]))
story.append(ns)

# Pre-flight
story.append(Paragraph("Pre-flight &mdash; this week (by ~June 30)", h2))
story.append(Paragraph("Before Month 1 begins, lock the foundations you are already mid-build on:", body))
for b in bullet_list([
    "<b>Finish the Typeform</b> &mdash; questions, types, options, welcome + ending (all drafted).",
    "<b>Pick where applications land</b> &mdash; connect Typeform to <b>Airtable</b> (becomes your directory + CRM in one) or Google Sheets to start.",
    "<b>Wire the form into the site</b> &mdash; replace the <font face='Courier'>#join</font> &ldquo;Coming soon&rdquo; placeholder with the Typeform embed.",
    "<b>Write the Code of Conduct</b> and link it from the form&rsquo;s Legal field.",
    "<b>Decide the home for &ldquo;You Are Not Alone&rdquo;</b> &mdash; WhatsApp Community or Telegram (diaspora-friendly, mobile-first).",
]):
    story.append(b)

# Month 1
story.append(Paragraph("Month 1 &mdash; Build &amp; Founding Members (July)", h2))
story.append(Paragraph("Goal: open quietly, hand-pick the first 25&ndash;40.", h3))
m1 = [
    [Paragraph("Workstream", th), Paragraph("What you do", th)],
    [Paragraph("Product / Form", cell_b), Paragraph("Form live on site; test the full flow on mobile; set up an auto-reply email (&ldquo;we review within 2 weeks&rdquo;).", cell)],
    [Paragraph("Community", cell_b), Paragraph("Personally invite 40&ndash;60 people you trust across 3&ndash;4 corridors (e.g. Kenya&ndash;UK, Nigeria&ndash;US, Ghana&ndash;Canada). Diversity of sector + city.", cell)],
    [Paragraph("Engagement setup", cell_b), Paragraph("Create the WhatsApp/Telegram space; write 3 pinned welcome messages; set the tone with your own first &ldquo;Help &amp; Be Helped&rdquo; post.", cell)],
    [Paragraph("Ops", cell_b), Paragraph("Build the Airtable member directory (auto-fed by Typeform); define your accept / fellowship review rubric.", cell)],
]
story.append(make_table(m1, [38*mm, 132*mm]))
story.append(Spacer(1, 3))
story.append(Paragraph('<b><font color="#2A3D2A">Month 1 success:</font></b> 25&ndash;40 applications in, ~20 accepted and in the channel, each one personally welcomed.', body))

# Month 2
story.append(Paragraph("Month 2 &mdash; Activate &amp; Prove (August)", h2))
story.append(Paragraph("Goal: make the network do something. A quiet group is a dead group.", h3))
m2 = [
    [Paragraph("Workstream", th), Paragraph("What you do", th)],
    [Paragraph("Bounce Ideas", cell_b), Paragraph("Host your <b>first talk</b> &mdash; a member or you, 20 min + open Q&amp;A, on Zoom/Meet. Record it.", cell)],
    [Paragraph("Help &amp; Be Helped", cell_b), Paragraph("Run a weekly &ldquo;Ask &amp; Offer&rdquo; thread; manually make 5&ndash;10 introductions to seed the habit.", cell)],
    [Paragraph("You Are Not Alone", cell_b), Paragraph("Open the peer-support space; you go first with something real to set the safety norm.", cell)],
    [Paragraph("Content", cell_b), Paragraph("Publish 1 free report (or repurpose one) tied to a corridor; share member wins on LinkedIn.", cell)],
    [Paragraph("Partnerships", cell_b), Paragraph("Re-engage Lemfi / Founders Running Club for a member perk or co-hosted session.", cell)],
]
story.append(make_table(m2, [38*mm, 132*mm]))
story.append(Spacer(1, 3))
story.append(Paragraph('<b><font color="#2A3D2A">Month 2 success:</font></b> First talk done (15+ live), 10+ real intros made, support channel has its first honest conversation, 1 partner perk live.', body))

# Month 3
story.append(Paragraph("Month 3 &mdash; Open &amp; Scale (September)", h2))
story.append(Paragraph("Goal: public launch of Season 01 with proof behind it.", h3))
m3 = [
    [Paragraph("Workstream", th), Paragraph("What you do", th)],
    [Paragraph("Public launch", cell_b), Paragraph("Announce on LinkedIn + Instagram + X; &ldquo;applications open&rdquo; post with the form link and a founding-member testimonial or two.", cell)],
    [Paragraph("Momentum", cell_b), Paragraph("Second Bounce Ideas talk; first <b>member-led</b> session &mdash; a sign the network runs without you.", cell)],
    [Paragraph("Growth loop", cell_b), Paragraph("Review &ldquo;How did you hear about us?&rdquo; data; ask happy members to refer 1 person each.", cell)],
    [Paragraph("Credibility", cell_b), Paragraph("Publish a short &ldquo;Season 01 so far&rdquo; recap (numbers + a story); update the site&rsquo;s &ldquo;By the Numbers&rdquo; with real figures.", cell)],
    [Paragraph("Ops", cell_b), Paragraph("Review fellowship applicants; set up a simple monthly newsletter from your member list.", cell)],
]
story.append(make_table(m3, [38*mm, 132*mm]))
story.append(Spacer(1, 3))
story.append(Paragraph('<b><font color="#2A3D2A">Month 3 success:</font></b> Public applications flowing weekly, 50&ndash;100 total members, a second talk + a member-led one, real numbers on your site.', body))

# KPIs
story.append(Paragraph("KPIs to watch the whole quarter", h2))
kpis = [
    ("100+", "Applications received"),
    ("50&ndash;100", "Members onboarded"),
    ("2&ndash;3", "Bounce Ideas talks"),
    ("25+", "Help &amp; Be Helped intros"),
    ("50%+", "In support channel"),
    ("5+", "Corridors represented"),
]
kcells = []
for num, lbl in kpis:
    inner = Table([[Paragraph(num, kpi_num)],[Paragraph(lbl, kpi_lbl)]], colWidths=[26*mm])
    inner.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), WHITE),
        ("BOX",(0,0),(-1,-1),0.6, LIGHT),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
    ]))
    kcells.append(inner)
krow = Table([kcells], colWidths=[28.3*mm]*6)
krow.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),1),("RIGHTPADDING",(0,0),(-1,-1),1),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
story.append(krow)

# Weekly rhythm
story.append(Paragraph("Weekly rhythm (set this early &mdash; it is what makes it stick)", h2))
for b in bullet_list([
    "<b>Mon</b> &mdash; &ldquo;Ask &amp; Offer&rdquo; thread + welcome new members.",
    "<b>Wed/Thu</b> &mdash; Bounce Ideas talk (bi-weekly) or member spotlight.",
    "<b>Fri</b> &mdash; review new applications, make 2&ndash;3 intros.",
    "<b>Monthly</b> &mdash; newsletter + numbers review.",
]):
    story.append(b)

# Risks
story.append(Paragraph("Biggest risks (and the fix)", h2))
risks = [
    [Paragraph("Risk", th), Paragraph("Fix", th)],
    [Paragraph("You are the only one doing everything", cell_b), Paragraph("Recruit 2&ndash;3 founding members as &ldquo;chapter hosts&rdquo; by Month 2 so it is not all on you.", cell)],
    [Paragraph("Silent channel", cell_b), Paragraph("Over-seed manually in Months 1&ndash;2; activity begets activity.", cell)],
    [Paragraph("Accepting too fast / loose", cell_b), Paragraph("The &ldquo;Why join&rdquo; + Code of Conduct questions are your gate &mdash; use them.", cell)],
]
story.append(make_table(risks, [60*mm, 110*mm]))

story.append(Spacer(1, 5*mm))
story.append(HRFlowable(width="100%", thickness=0.8, color=OCHRE, spaceAfter=5))
story.append(Paragraph("Africa Global Forum &mdash; a peer network for the African diaspora. "
                       "We create opportunity among ourselves first, then with the world.", small))

# ---------- doc ----------
doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=18*mm, rightMargin=18*mm,
                      topMargin=22*mm, bottomMargin=16*mm,
                      title="AGF 90-Day Launch Roadmap", author="Africa Global Forum")
frame = Frame(doc.leftMargin, doc.bottomMargin,
              A4[0]-doc.leftMargin-doc.rightMargin,
              A4[1]-doc.topMargin-doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])
doc.build(story)
print("WROTE", OUT)
