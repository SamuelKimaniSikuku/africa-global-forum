#!/usr/bin/env python3
"""Generate the AGF Months 2 & 3 week-by-week launch checklist PDF (branded)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)

INK       = colors.HexColor("#0E0B08")
PAPER     = colors.HexColor("#F4EFE6")
TERRACOTTA= colors.HexColor("#C8421A")
OCHRE     = colors.HexColor("#D89B2C")
RUST      = colors.HexColor("#7A2E12")
FOREST    = colors.HexColor("#2A3D2A")
MUTED     = colors.HexColor("#6B635A")
LIGHT     = colors.HexColor("#EAE2D4")
WHITE     = colors.white

OUT = "/Users/kiman/africa-global-forum/reports/AGF-Month2-3-Checklist.pdf"
styles = getSampleStyleSheet()
def S(name, **kw): return ParagraphStyle(name, parent=styles["Normal"], **kw)

h1    = S("h1", fontName="Helvetica-Bold", fontSize=20, leading=23, textColor=INK, spaceAfter=4)
label = S("label", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=OCHRE, spaceAfter=2)
small = S("small", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MUTED)
monthh= S("monthh", fontName="Helvetica-Bold", fontSize=13.5, leading=16, textColor=TERRACOTTA, spaceBefore=8, spaceAfter=4)
wkh   = S("wkh", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=WHITE)
wksub = S("wksub", fontName="Helvetica-Oblique", fontSize=8.3, leading=11, textColor=colors.HexColor("#F4D9A0"))
task  = S("task", fontName="Helvetica", fontSize=9, leading=12.5, textColor=INK)
owncol= S("owncol", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=RUST)

def checkbox():
    b = Table([[""]], colWidths=[3.4*mm], rowHeights=[3.4*mm])
    b.setStyle(TableStyle([
        ("BOX",(0,0),(-1,-1),0.8, TERRACOTTA),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))
    return b

def check_rows(items):
    rows = [[checkbox(), Paragraph(t, task), Paragraph(tag, owncol)] for t, tag in items]
    tbl = Table(rows, colWidths=[8*mm, 134*mm, 28*mm])
    tbl.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(0,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(1,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LINEBELOW",(0,0),(-1,-1),0.4, LIGHT),
        ("BACKGROUND",(0,0),(-1,-1), WHITE),
    ]))
    return tbl

def week_header(title, sub):
    t = Table([[Paragraph(title, wkh)],[Paragraph(sub, wksub)]], colWidths=[170*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), TERRACOTTA),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(0,0),7),("BOTTOMPADDING",(0,0),(0,0),0),
        ("TOPPADDING",(0,1),(0,1),0),("BOTTOMPADDING",(0,1),(0,1),7),
    ]))
    return t

def success_bar(text):
    d = Table([[Paragraph(text, S("d", fontName="Helvetica", fontSize=9, leading=13, textColor=WHITE))]], colWidths=[170*mm])
    d.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), FOREST),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
        ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9),
    ]))
    return d

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER); canvas.rect(0,0,A4[0],A4[1],fill=1,stroke=0)
    canvas.setFillColor(INK); canvas.rect(0,A4[1]-16*mm,A4[0],16*mm,fill=1,stroke=0)
    canvas.setFillColor(OCHRE); canvas.rect(0,A4[1]-16.8*mm,A4[0],0.8*mm,fill=1,stroke=0)
    canvas.setFillColor(WHITE); canvas.setFont("Helvetica-Bold",9)
    canvas.drawString(18*mm,A4[1]-10.5*mm,"AFRICA GLOBAL FORUM")
    canvas.setFillColor(OCHRE); canvas.setFont("Helvetica",7.5)
    canvas.drawRightString(A4[0]-18*mm,A4[1]-10.5*mm,"Months 2 & 3 · Weekly Checklist")
    canvas.setFillColor(MUTED); canvas.setFont("Helvetica",7)
    canvas.drawString(18*mm,10*mm,"africaglobalforum.com  ·  Created among ourselves, first.")
    canvas.drawRightString(A4[0]-18*mm,10*mm,f"Page {doc.page}")
    canvas.restoreState()

story = []
story.append(Spacer(1, 4*mm))
story.append(Paragraph("MONTHS 2 & 3 · AUGUST–SEPTEMBER 2026", label))
story.append(Paragraph("Week-by-Week Launch Checklist", h1))
story.append(Paragraph("Picks up where Month 1 ends. Month 2 activates the network and proves the three engagements; "
                       "Month 3 opens Season 01 publicly with proof behind it. Tick each box as you go.", small))
story.append(Spacer(1, 2*mm))
story.append(HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2))

# ---------------- MONTH 2 ----------------
story.append(Paragraph("Month 2 — Activate & Prove (August)", monthh))

story.append(week_header("Week 5 — First Talk", "Make the network do something visible."))
story.append(check_rows([
    ("Confirm a speaker (a member or you) and a topic for the first Bounce Ideas talk", "ENGAGEMENT"),
    ("Set date/time across time zones; send calendar invites to all members", "OPS"),
    ("Run the talk: 20 min + open Q&amp;A on Zoom/Meet &mdash; and record it", "ENGAGEMENT"),
    ("Share 2&ndash;3 highlights + the recording in the channel afterwards", "CONTENT"),
]))
story.append(Spacer(1, 2*mm))

story.append(week_header("Week 6 — Help & Be Helped", "Turn the channel into a marketplace."))
story.append(check_rows([
    ("Run the weekly &ldquo;Ask &amp; Offer&rdquo; thread; reply to every post yourself", "ENGAGEMENT"),
    ("Manually make 5&ndash;10 member-to-member introductions", "ENGAGEMENT"),
    ("Capture each intro in Airtable to track what people ask for / offer", "OPS"),
    ("Spotlight one member&rsquo;s win on LinkedIn (with their permission)", "CONTENT"),
]))
story.append(Spacer(1, 2*mm))

story.append(week_header("Week 7 — You Are Not Alone", "Open the space for the harder conversations."))
story.append(check_rows([
    ("Open the peer-support space; pin its purpose + simple ground rules", "ENGAGEMENT"),
    ("Go first &mdash; share something real to set the safety norm", "COMMUNITY"),
    ("Publish (or repurpose) one free report tied to a live corridor", "CONTENT"),
    ("Re-engage Lemfi / Founders Running Club about a member perk or co-hosted session", "PARTNERSHIPS"),
]))
story.append(Spacer(1, 2*mm))

story.append(week_header("Week 8 — Prep to Open", "Gather proof and get launch-ready."))
story.append(check_rows([
    ("Collect 2&ndash;3 founding-member testimonials / short quotes", "CONTENT"),
    ("Draft the public &ldquo;applications open&rdquo; announcement posts", "CONTENT"),
    ("Lock a partner perk live for members before launch", "PARTNERSHIPS"),
    ("Review Month 2 numbers: talk attendance, intros made, channel activity", "OPS"),
]))
story.append(Spacer(1, 2*mm))
story.append(success_bar("<b>End of Month 2 &mdash; you&rsquo;ve made it if:</b>&nbsp; first talk done (15+ live), 10+ real intros made, "
                         "the support channel has had its first honest conversation, and one partner perk is live."))

# ---------------- MONTH 3 ----------------
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Month 3 — Open & Scale (September)", monthh))

story.append(week_header("Week 9 — Public Launch", "Open Season 01 with proof behind it."))
story.append(check_rows([
    ("Publish the &ldquo;applications open&rdquo; posts on LinkedIn, Instagram &amp; X", "CONTENT"),
    ("Feature a founding-member testimonial in the launch post", "CONTENT"),
    ("Make sure the site form + auto-reply handle a higher volume", "PRODUCT"),
    ("Reply to and triage the first wave of new applications", "OPS"),
]))
story.append(Spacer(1, 2*mm))

story.append(week_header("Week 10 — Momentum", "Show the network runs &mdash; even without you."))
story.append(check_rows([
    ("Host the second Bounce Ideas talk", "ENGAGEMENT"),
    ("Hand one session to a member &mdash; the first member-led event", "COMMUNITY"),
    ("Keep the weekly Ask &amp; Offer + intros rhythm going", "ENGAGEMENT"),
    ("Welcome and onboard the new public applicants in batches", "COMMUNITY"),
]))
story.append(Spacer(1, 2*mm))

story.append(week_header("Week 11 — Growth Loop", "Make members your engine of growth."))
story.append(check_rows([
    ("Review &ldquo;How did you hear about us?&rdquo; data; double down on what works", "OPS"),
    ("Ask happy members to refer one person each", "COMMUNITY"),
    ("Review fellowship applicants and confirm awards", "OPS"),
    ("Set up a simple monthly newsletter from your member list", "OPS"),
]))
story.append(Spacer(1, 2*mm))

story.append(week_header("Week 12 — Credibility & Review", "Bank the proof and plan ahead."))
story.append(check_rows([
    ("Publish a short &ldquo;Season 01 so far&rdquo; recap &mdash; numbers + one story", "CONTENT"),
    ("Update the site&rsquo;s &ldquo;By the Numbers&rdquo; with real figures", "PRODUCT"),
    ("Confirm chapter hosts / volunteers to share the load", "COMMUNITY"),
    ("Review the full quarter vs. KPIs and sketch the next 90 days", "OPS"),
]))
story.append(Spacer(1, 2*mm))
story.append(success_bar("<b>End of Month 3 &mdash; you&rsquo;ve made it if:</b>&nbsp; public applications flowing weekly, 50&ndash;100 total "
                         "members, a second talk plus a member-led session done, and real numbers live on your site."))

story.append(Spacer(1, 4*mm))
story.append(HRFlowable(width="100%", thickness=0.8, color=OCHRE, spaceAfter=5))
story.append(Paragraph("Africa Global Forum &mdash; a peer network for the African diaspora. "
                       "We create opportunity among ourselves first, then with the world.", small))

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                      topMargin=22*mm, bottomMargin=16*mm,
                      title="AGF Months 2 & 3 Weekly Checklist", author="Africa Global Forum")
frame = Frame(doc.leftMargin, doc.bottomMargin, A4[0]-doc.leftMargin-doc.rightMargin,
              A4[1]-doc.topMargin-doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])
doc.build(story)
print("WROTE", OUT)
