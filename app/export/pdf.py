from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

FONT = "Times-Roman"
FONT_BOLD = "Times-Bold"
FONT_ITALIC = "Times-Italic"
LINK_COLOR = "#1a56db"

name_style = ParagraphStyle("Name", fontName=FONT_BOLD, fontSize=16, alignment=TA_CENTER, spaceAfter=2, leading=19)
contact_style = ParagraphStyle("Contact", fontName=FONT, fontSize=9.5, alignment=TA_CENTER, spaceAfter=10, leading=14)
section_style = ParagraphStyle("Section", fontName=FONT_BOLD, fontSize=10.5, spaceBefore=8, spaceAfter=2)
entry_title_style = ParagraphStyle("EntryTitle", fontName=FONT_BOLD, fontSize=10, leading=13)
entry_sub_italic_style = ParagraphStyle("EntrySubItalic", fontName=FONT_ITALIC, fontSize=9.5, leading=12)
entry_date_style = ParagraphStyle("EntryDate", fontName=FONT_BOLD, fontSize=9.5, alignment=2, leading=13)
entry_date_italic_style = ParagraphStyle("EntryDateItalic", fontName=FONT_ITALIC, fontSize=9.5, alignment=2, leading=12)
bullet_style = ParagraphStyle("Bullet", fontName=FONT, fontSize=9.5, leading=13, leftIndent=20, firstLineIndent=-10, spaceAfter=3)
tech_line_style = ParagraphStyle("TechLine", fontName=FONT, fontSize=9.5, leading=13, spaceAfter=3)
code_line_style = ParagraphStyle("CodeLine", fontName=FONT, fontSize=9.5, leading=13, spaceAfter=6)


def styled_link(url: str, label: str) -> str:
    return f'<link href="{url}"><font color="{LINK_COLOR}"><u>{label}</u></font></link>'


def section_header(story, title):
    story.append(Paragraph(title.upper(), section_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.black, spaceBefore=1, spaceAfter=6))


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
    for b in bullets:
        story.append(Paragraph(f'•&nbsp;&nbsp;{b}', bullet_style))


def build_resume_pdf(output_path: str, personal_info: dict, education: list,
                      experience: list, projects: list, skills: list, extracurricular: list):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                             topMargin=0.55 * inch, bottomMargin=0.55 * inch,
                             leftMargin=0.75 * inch, rightMargin=0.75 * inch)
    story = []

    # Header
    story.append(Paragraph(personal_info.get("name", "").upper(), name_style))

    contact_parts = [p for p in [
        personal_info.get("location", ""),
        personal_info.get("phone", ""),
    ] if p]

    email = personal_info.get("email", "")
    if email:
        contact_parts.append(styled_link(f"mailto:{email}", email))

    for link in personal_info.get("links", []):
        if link.get("url"):
            contact_parts.append(styled_link(link["url"], link.get("label", link["url"])))

    if contact_parts:
        story.append(Paragraph(" &nbsp;|&nbsp; ".join(contact_parts), contact_style))

    # Education
    if education:
        section_header(story, "Education")
        for item in education:
            story.append(two_col_row(
                item.get("institution", ""), item.get("dates", ""),
                entry_title_style, entry_date_style
            ))
            degree_line = item.get("degree", "")
            if item.get("detail"):
                degree_line += f' &nbsp;|&nbsp; {item.get("detail")}'
            story.append(Paragraph(degree_line, entry_sub_italic_style))
            story.append(Spacer(1, 8))

    # Projects
    if projects:
        section_header(story, "Projects")
        for item in projects:
            story.append(two_col_row(
                item.get("name", ""), item.get("date", ""),
                entry_title_style, entry_date_style
            ))
            if item.get("tags"):
                story.append(Paragraph(
                    f'<b>Tech Stack:</b> <i>{item.get("tags")}</i>', tech_line_style
                ))
            bullet_list(story, item.get("bullets", []))
            if item.get("live_url"):
                display_url = item["live_url"].replace("https://", "").replace("http://", "")
                story.append(Paragraph(
                    f'<b>Code:</b> {styled_link(item["live_url"], display_url)}', code_line_style
                ))
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
            story.append(Paragraph(line, tech_line_style))
        story.append(Spacer(1, 4))

    # Extracurricular
    if extracurricular:
        section_header(story, "Extracurricular")
        bullet_list(story, extracurricular)

    doc.build(story)