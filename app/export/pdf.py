from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

styles = getSampleStyleSheet()

FONT = "Times-Roman"
FONT_BOLD = "Times-Bold"
FONT_ITALIC = "Times-Italic"

name_style = ParagraphStyle("Name", fontName=FONT_BOLD, fontSize=22, alignment=TA_CENTER, spaceAfter=2, leading=26)
contact_style = ParagraphStyle("Contact", fontName=FONT, fontSize=9.5, alignment=TA_CENTER, spaceAfter=10, leading=12)
section_style = ParagraphStyle("Section", fontName=FONT_BOLD, fontSize=11, spaceBefore=8, spaceAfter=2)
entry_title_style = ParagraphStyle("EntryTitle", fontName=FONT_BOLD, fontSize=10.5, leading=13)
entry_sub_italic_style = ParagraphStyle("EntrySubItalic", fontName=FONT_ITALIC, fontSize=10, leading=12)
entry_date_style = ParagraphStyle("EntryDate", fontName=FONT_BOLD, fontSize=10, alignment=2, leading=13)  # right aligned
entry_date_italic_style = ParagraphStyle("EntryDateItalic", fontName=FONT_ITALIC, fontSize=10, alignment=2, leading=12)
bullet_style = ParagraphStyle("Bullet", fontName=FONT, fontSize=9.7, leading=13,leftIndent=20)
coursework_style = ParagraphStyle("Coursework", fontName=FONT, fontSize=9.7, leading=15)


def section_header(story, title):
    story.append(Paragraph(title.upper(), section_style))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.black, spaceBefore=1, spaceAfter=6))

def project_title_line(item):
    title = f'<b>{item.get("name", "")}</b>'
    # if item.get("live_url"):
    #     title += f' <link href="{item.get("live_url")}"><u>Live</u></link>'  # external-link arrow

    tag_parts = []
    if item.get("live_url"):
        tag_parts.append(f' <link href="{item.get("live_url")}"><u>Github</u></link>')
    if item.get("group_label"):
        tag_parts.append(item.get("group_label"))
    if item.get("tags"):
        tag_parts.append(item.get("tags"))

    if tag_parts:
        title += f' &nbsp;|&nbsp; <i>{", ".join(tag_parts)}</i>'

    return title


def two_col_row(left_text, right_text, left_style, right_style):
    t = Table(
        [[Paragraph(left_text, left_style), Paragraph(right_text, right_style)]],
        colWidths=[4.6 * inch, 1.9 * inch],
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return t


def bullet_list(story, bullets):
    if not bullets:
        return
    items = [
        ListItem(Paragraph(b, bullet_style), leftIndent=0)
        for b in bullets
    ]
    story.append(ListFlowable(
        items,
        bulletType="bullet",
        start="•",
        leftIndent=-12,
        bulletFontName=FONT_BOLD,
        bulletFontSize=9,
        bulletOffsetY=-0.5,
        spaceBefore=1,
        spaceAfter=3,
    ))

def build_resume_pdf(output_path: str, personal_info: dict, education: list,
                      experience: list, projects: list, skills: list, extracurricular: list,
                      coursework: list = None):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                             topMargin=0.55 * inch, bottomMargin=0.55 * inch,
                             leftMargin=0.75 * inch, rightMargin=0.75 * inch)
    story = []

    # Header
    story.append(Paragraph(personal_info.get("name", "").upper(), name_style))
    contact_parts = [p for p in [personal_info.get("location", "")] if p]
    if contact_parts:
        story.append(Paragraph(contact_parts[0], contact_style))

    line2 = [p for p in [personal_info.get("phone", ""), personal_info.get("email", "")] if p]
    links = personal_info.get("links", [])
    link_parts = [f'<link href="{l.get("url", "")}"><u>{l.get("label", "")}</u></link>' for l in links]
    contact_line2 = " &nbsp;&nbsp; ".join(line2 + link_parts)
    if contact_line2:
        story.append(Paragraph(contact_line2, contact_style))

    # Education
    if education:
        section_header(story, "Education")
        for item in education:
            story.append(two_col_row(
                item.get("institution", ""), item.get("dates", ""),
                entry_title_style, entry_date_style
            ))
            story.append(two_col_row(
                item.get("degree", ""), item.get("detail", ""),
                entry_sub_italic_style, entry_date_italic_style
            ))
            story.append(Spacer(1, 6))

    # Coursework
    if coursework:
        section_header(story, "Coursework")
        rows = []
        for i in range(0, len(coursework), 3):
            row_items = coursework[i:i+3]
            rows.append(" &nbsp;&nbsp;&nbsp; ".join(f"• {c}" for c in row_items))
        story.append(Paragraph("<br/>".join(rows), coursework_style))
        story.append(Spacer(1, 4))

    # Projects
    if projects:
        section_header(story, "Projects")
        for item in projects:
            story.append(two_col_row(project_title_line(item), item.get("date", ""), entry_title_style, entry_date_style))
            bullet_list(story, item.get("bullets", []))
            story.append(Spacer(1, 4))

    # Experience
    if experience:
        section_header(story, "Experience")
        for item in experience:
            title_line = f'{item.get("role", "")} — {item.get("company", "")}'
            story.append(two_col_row(title_line, item.get("dates", ""), entry_title_style, entry_date_style))
            bullet_list(story, item.get("bullets", []))
            story.append(Spacer(1, 4))

    # Skills
    if skills:
        section_header(story, "Technical Skills")
        for group in skills:
            line = f'<b>{group.get("category", "")}:</b> {", ".join(group.get("items", []))}'
            story.append(Paragraph(line, bullet_style))
            story.append(Spacer(1, 3))

    # Extracurricular
    if extracurricular:
        section_header(story, "Extracurricular")
        bullet_list(story, extracurricular)

    doc.build(story)