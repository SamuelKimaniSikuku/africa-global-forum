#!/usr/bin/env python3
"""Generate the AGF Month 1 week-by-week launch checklist PDF (branded)."""

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

OUT = "/Users/kiman/africa-global-forum/reports/AGF-Month1-Checklist.pdf"
styles = getSampleStyleSheet()
def S(name, **kw): return ParagraphStyle(name, parent=styles["Normal"], **kw)

body  = S("body", fontName="Helvetica", fontSize=9.5, leading=14, textColor=INK, spaceAfter=6)
h1    = S("h1", fontName="Helvetica-Bold", fontSize=20, leading=23, textColor=INK, spaceAfter=4)
label = S("label", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=OCHRE, spaceAfter=2)
small = S("small", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MUTED)
wkh   = S("wkh", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=WHITE)
wksub = S("wksub", fontName="Helvetica-Oblique", fontSize=8.3, leading=11, textColor=colors.HexColor("#F4D9A0"))
task  = S("task", fontName="Helvetica", fontSize=9, leading=12.5, textColor=INK)
owncol= S("owncol", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=RUST)

def checkbox():
    """A small empty square drawn with a border (built-in fonts lack a ballot-box glyph)."""
    b = Table([[""]], colWidths=[3.4*mm], rowHeights=[3.4*mm])
    b.setStyle(TableStyle([
        ("BOX",(0,0),(-1,-1),0.8, TERRACOTTA),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))
    return b

def check_rows(items):
    """items = list of (task, tag). Returns table rows with a checkbox cell."""
    rows = []
    for t, tag in items:
        txt = Paragraph(t, task)
        tg  = Paragraph(tag, owncol)
        rows.append([checkbox(), txt, tg])
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

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER); canvas.rect(0,0,A4[0],A4[1],fill=1,stroke=0)
    canvas.setFillColor(INK); canvas.rect(0,A4[1]-16*mm,A4[0],16*mm,fill=1,stroke=0)
    canvas.setFillColor(OCHRE); canvas.rect(0,A4[1]-16.8*mm,A4[0],0.8*mm,fill=1,stroke=0)
    canvas.setFillColor(WHITE); canvas.setFont("Helvetica-Bold",9)
    canvas.drawString(18*mm,A4[1]-10.5*mm,"AFRICA GLOBAL FORUM")
    canvas.setFillColor(OCHRE); canvas.setFont("Helvetica",7.5)
    canvas.drawRightString(A4[0]-18*mm,A4[1]-10.5*mm,"Month 1 · Weekly Checklist")
    canvas.setFillColor(MUTED); canvas.setFont("Helvetica",7)
    canvas.drawString(18*mm,10*mm,"africaglobalforum.com  ·  Created among ourselves, first.")
    canvas.drawRightString(A4[0]-18*mm,10*mm,f"Page {doc.page}")
    canvas.restoreState()

story = []
story.append(Spacer(1, 4*mm))
story.append(Paragraph("MONTH 1 · JULY 2026", label))
story.append(Paragraph("Week-by-Week Launch Checklist", h1))
story.append(Paragraph("Goal for the month: open quietly and hand-pick your first 25&ndash;40 founding members. "
                       "Tick each box as you go. Tags show the focus area.", small))
story.append(Spacer(1, 3*mm))
story.append(HRFlowable(width="100%", thickness=1, color=OCHRE, spaceAfter=2))

# Week 1
story.append(Spacer(1, 3*mm))
story.append(week_header("Week 1 — Foundations", "Get the machine ready before anyone applies."))
story.append(check_rows([
    ("Finalise the Typeform &mdash; all questions, types, options, welcome &amp; ending screens", "PRODUCT"),
    ("Connect Typeform to Airtable (or Google Sheets) so applications auto-land", "OPS"),
    ("Replace the site&rsquo;s <font face='Courier'>#join</font> &ldquo;Coming soon&rdquo; block with the Typeform embed", "PRODUCT"),
    ("Write and publish the Code of Conduct; link it in the form&rsquo;s Legal field", "OPS"),
    ("Set up an application auto-reply email (&ldquo;we review within 2 weeks&rdquo;)", "OPS"),
    ("Create the WhatsApp Community / Telegram space + 3 pinned welcome messages", "COMMUNITY"),
    ("Draft your accept / fellowship review rubric (3&ndash;4 simple criteria)", "OPS"),
]))

# Week 2
story.append(Spacer(1, 3*mm))
story.append(week_header("Week 2 — First Invitations", "Reach out personally. Quality over volume."))
story.append(check_rows([
    ("List 40&ndash;60 people you trust across 3&ndash;4 corridors (e.g. KE&ndash;UK, NG&ndash;US, GH&ndash;CA)", "COMMUNITY"),
    ("Send personal invites (DM / voice note, not a mass blast) with the form link", "COMMUNITY"),
    ("Test the full form flow yourself on mobile, end to end", "PRODUCT"),
    ("Post your own first &ldquo;Help &amp; Be Helped&rdquo; message to model the tone", "ENGAGEMENT"),
    ("Track invites sent vs. applications received in Airtable", "OPS"),
]))

# Week 3
story.append(Spacer(1, 3*mm))
story.append(week_header("Week 3 — Review & Welcome", "Turn applicants into members who feel seen."))
story.append(check_rows([
    ("Review incoming applications against your rubric; flag fellowship cases", "OPS"),
    ("Accept the first ~20; send each a warm, personal welcome", "COMMUNITY"),
    ("Add accepted members to the channel; introduce each one by name", "COMMUNITY"),
    ("Build the member directory view in Airtable (corridor, sector, offer/ask)", "OPS"),
    ("Make your first 3&ndash;5 manual introductions between members", "ENGAGEMENT"),
]))

# Week 4
story.append(Spacer(1, 3*mm))
story.append(week_header("Week 4 — Rhythm & Review", "Set the heartbeat that carries into Month 2."))
story.append(check_rows([
    ("Launch the weekly &ldquo;Ask &amp; Offer&rdquo; thread (pick a fixed day)", "ENGAGEMENT"),
    ("Schedule your first Bounce Ideas talk for early August", "ENGAGEMENT"),
    ("Send a short check-in to all members &mdash; what do they want from AGF?", "COMMUNITY"),
    ("Review Month 1 numbers: invites, applications, accepts, channel activity", "OPS"),
    ("Pick 2&ndash;3 engaged members as potential chapter hosts for Month 2", "COMMUNITY"),
]))

# Month-1 success bar
story.append(Spacer(1, 4*mm))
done = Table([[Paragraph('<b>End of Month 1 &mdash; you&rsquo;ve made it if:</b>&nbsp; 25&ndash;40 applications in, '
                         '~20 members accepted and welcomed into an active channel, a weekly rhythm started, '
                         'and your first talk on the calendar.', S("d", fontName="Helvetica", fontSize=9, leading=13, textColor=WHITE))]],
              colWidths=[170*mm])
done.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), FOREST),
    ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
    ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
]))
story.append(done)
story.append(Spacer(1, 4*mm))
story.append(HRFlowable(width="100%", thickness=0.8, color=OCHRE, spaceAfter=5))
story.append(Paragraph("Africa Global Forum &mdash; a peer network for the African diaspora. "
                       "We create opportunity among ourselves first, then with the world.", small))

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                      topMargin=22*mm, bottomMargin=16*mm,
                      title="AGF Month 1 Weekly Checklist", author="Africa Global Forum")
frame = Frame(doc.leftMargin, doc.bottomMargin, A4[0]-doc.leftMargin-doc.rightMargin,
              A4[1]-doc.topMargin-doc.bottomMargin, id="main")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])
doc.build(story)
print("WROTE", OUT)
