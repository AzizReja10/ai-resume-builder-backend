from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors


# ============================================================
# FONT CONFIGURATION
# ============================================================

# Times-Roman is very close to the font in your screenshot.
FONT = "Times-Roman"
FONT_BOLD = "Times-Bold"
FONT_ITALIC = "Times-Italic"

LINK_COLOR = "#1A56DB"


# ============================================================
# STYLES
# ============================================================

# ---------- HEADER ----------

name_style =  ParagraphStyle("Name", fontName=FONT_BOLD, fontSize=22, alignment=TA_CENTER, spaceAfter=2, leading=26)

contact_style = ParagraphStyle("Contact", fontName=FONT, fontSize=9.5, alignment=TA_CENTER, spaceAfter=10, leading=12)


# ---------- SECTION ----------

section_style = ParagraphStyle("Section", fontName=FONT_BOLD, fontSize=11, spaceBefore=8, spaceAfter=2)

# ---------- EDUCATION / PROJECT TITLES ----------

entry_title_style = ParagraphStyle("EntryTitle", fontName=FONT_BOLD, fontSize=10.5, leading=13)

entry_date_style = ParagraphStyle("EntryDate", fontName=FONT_BOLD, fontSize=10, alignment=2, leading=13)

entry_sub_italic_style = ParagraphStyle("EntrySubItalic", fontName=FONT_ITALIC, fontSize=10, leading=12)


# ---------- TECH STACK ----------

tech_line_style = ParagraphStyle(
    "TechLine",
    fontName=FONT,
    fontSize=9.3,
    leading=11.5,
    spaceAfter=2,
)


# ---------- BULLETS ----------

bullet_style = ParagraphStyle("Bullet", fontName=FONT, fontSize=9.7, leading=13,leftIndent=20)


# ---------- CODE / GITHUB ----------

code_line_style = ParagraphStyle(
    "CodeLine",
    fontName=FONT,
    fontSize=9.3,
    leading=11,
    spaceAfter=3,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def styled_link(url: str, label: str) -> str:
    """
    Creates a blue underlined hyperlink.
    """
    return (
        f'<link href="{url}">'
        f'<font color="{LINK_COLOR}"><u>{label}</u></font>'
        f'</link>'
    )


def section_header(story, title):
    """
    Creates section heading + thin horizontal line.
    Matches the screenshot.
    """

    story.append(
        Paragraph(title.upper(), section_style)
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.7,
            color=colors.black,
            spaceBefore=0,
            spaceAfter=4,
        )
    )


def two_col_row(
    left_text,
    right_text,
    left_style=entry_title_style,
    right_style=entry_date_style,
):
    """
    Left side = title
    Right side = date
    """

    table = Table(
        [
            [
                Paragraph(left_text, left_style),
                Paragraph(right_text, right_style),
            ]
        ],
        colWidths=[
            5.15 * inch,
            1.35 * inch,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),

                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),

                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    return table


def bullet_list(story, bullets):
    """
    Adds compact resume bullets.
    """

    for bullet in bullets:
        story.append(
            Paragraph(
                f"•&nbsp;&nbsp;{bullet}",
                bullet_style,
            )
        )


# ============================================================
# BUILD RESUME
# ============================================================

def build_resume_pdf(
    output_path: str,
    personal_info: dict,
    education: list,
    experience: list,
    projects: list,
    skills: list,
    extracurricular: list,
):

    # --------------------------------------------------------
    # PAGE SETTINGS
    # --------------------------------------------------------

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,

        # Screenshot has fairly narrow margins
        topMargin=0.40 * inch,
        bottomMargin=0.40 * inch,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,

        # Prevent ReportLab from adding unexpected spacing
        title="Resume",
        author=personal_info.get("name", ""),
    )

    story = []


    # ========================================================
    # HEADER
    # ========================================================

    name = personal_info.get("name", "")

    if name:
        story.append(
            Paragraph(
                name.upper(),
                name_style,
            )
        )


    # --------------------------------------------------------
    # CONTACT INFORMATION
    # --------------------------------------------------------

    contact_parts = []

    location = personal_info.get("location", "")
    phone = personal_info.get("phone", "")
    email = personal_info.get("email", "")

    if location:
        contact_parts.append(location)

    if phone:
        contact_parts.append(phone)

    if email:
        contact_parts.append(
            styled_link(
                f"mailto:{email}",
                email,
            )
        )

    # Additional links
    for link in personal_info.get("links", []):

        url = link.get("url", "")
        label = link.get("label", "")

        if url:

            # Remove https:// from displayed text
            display_label = label or url

            contact_parts.append(
                styled_link(
                    url,
                    display_label,
                )
            )

    if contact_parts:

        contact_line = " &nbsp;|&nbsp; ".join(contact_parts)

        story.append(
            Paragraph(
                contact_line,
                contact_style,
            )
        )


    # ========================================================
    # EDUCATION
    # ========================================================

    if education:

        section_header(
            story,
            "Education",
        )

        for item in education:

            # University + Date
            story.append(
                two_col_row(
                    item.get("institution", ""),
                    item.get("dates", ""),
                    entry_title_style,
                    entry_date_style,
                )
            )

            # Degree + CGPA
            degree_line = item.get(
                "degree",
                "",
            )

            detail = item.get(
                "detail",
                "",
            )

            if detail:
                degree_line += (
                    f" &nbsp;|&nbsp; {detail}"
                )

            story.append(
                Paragraph(
                    degree_line,
                    entry_sub_italic_style,
                )
            )

            story.append(
                Spacer(1, 3)
            )


    # ========================================================
    # PROJECTS
    # ========================================================

    if projects:

        section_header(
            story,
            "Projects",
        )

        for item in projects:

            project_block = []


            # ------------------------------------------------
            # PROJECT NAME + DATE
            # ------------------------------------------------

            project_block.append(
                two_col_row(
                    item.get("name", ""),
                    item.get("date", ""),
                    entry_title_style,
                    entry_date_style,
                )
            )


            # ------------------------------------------------
            # TECH STACK
            # ------------------------------------------------

            tags = item.get(
                "tags",
                "",
            )

            if tags:

                project_block.append(
                    Paragraph(
                        f"<b>Tech Stack:</b> "
                        f"<i>{tags}</i>",
                        tech_line_style,
                    )
                )


            # ------------------------------------------------
            # BULLETS
            # ------------------------------------------------

            for bullet in item.get(
                "bullets",
                [],
            ):

                project_block.append(
                    Paragraph(
                        f"•&nbsp;&nbsp;{bullet}",
                        bullet_style,
                    )
                )


            # ------------------------------------------------
            # GITHUB / CODE LINK
            # ------------------------------------------------

            live_url = item.get(
                "live_url",
                "",
            )

            if live_url:

                display_url = (
                    live_url
                    .replace("https://", "")
                    .replace("http://", "")
                )

                project_block.append(
                    Paragraph(
                        f"<b>Code:</b> "
                        f"{styled_link(live_url, display_url)}",
                        code_line_style,
                    )
                )


            # Keep project content together where possible
            story.append(
                KeepTogether(project_block)
            )

            # Small gap between projects
            story.append(
                Spacer(1, 3)
            )


    # ========================================================
    # EXPERIENCE
    # ========================================================

    if experience:

        section_header(
            story,
            "Experience",
        )

        for item in experience:

            title_line = (
                f'{item.get("role", "")}'
            )

            company = item.get(
                "company",
                "",
            )

            if company:
                title_line += (
                    f" — {company}"
                )


            story.append(
                two_col_row(
                    title_line,
                    item.get("dates", ""),
                    entry_title_style,
                    entry_date_style,
                )
            )


            bullet_list(
                story,
                item.get(
                    "bullets",
                    [],
                ),
            )

            story.append(
                Spacer(1, 3)
            )


    # ========================================================
    # TECHNICAL SKILLS
    # ========================================================

    if skills:

        section_header(
            story,
            "Technical Skills",
        )

        for group in skills:

            category = group.get(
                "category",
                "",
            )

            items = group.get(
                "items",
                [],
            )

            line = (
                f"<b>{category}:</b> "
                f"{', '.join(items)}"
            )

            story.append(
                Paragraph(
                    line,
                    tech_line_style,
                )
            )

        story.append(
            Spacer(1, 2)
        )


    # ========================================================
    # EXTRACURRICULAR
    # ========================================================

    if extracurricular:

        section_header(
            story,
            "Extracurricular",
        )

        bullet_list(
            story,
            extracurricular,
        )


    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(story)