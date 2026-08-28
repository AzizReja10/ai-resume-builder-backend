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
# PAGE / FONT CONFIG
# ============================================================

FONT = "Times-Roman"
FONT_BOLD = "Times-Bold"
FONT_ITALIC = "Times-Italic"

LINK_COLOR = "#0563C1"


# ============================================================
# PAGE GEOMETRY
# ============================================================

PAGE_WIDTH, PAGE_HEIGHT = A4

LEFT_MARGIN = 0.52 * inch
RIGHT_MARGIN = 0.52 * inch

CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN


# ============================================================
# STYLES
# ============================================================

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

# ============================================================
# HEADER
# ============================================================

name_style = ParagraphStyle(
    "Name",
    fontName=FONT_BOLD,
    fontSize=18,
    leading=19,
    alignment=TA_CENTER,
    spaceBefore=0,
    spaceAfter=3,
)


contact_style = ParagraphStyle(
    "Contact",
    fontName=FONT,
    fontSize=10,
    leading=12,
    alignment=TA_CENTER,
    spaceBefore=0,
    spaceAfter=8,
)


# ============================================================
# SECTION HEADINGS
# ============================================================

section_style = ParagraphStyle(
    "Section",
    fontName=FONT_BOLD,
    fontSize=11,
    leading=13,
    spaceBefore=4,
    spaceAfter=1,
)


# ============================================================
# PROJECT / UNIVERSITY TITLE
# ============================================================

entry_title_style = ParagraphStyle(
    "EntryTitle",
    fontName=FONT_BOLD,
    fontSize=10.8,
    leading=13,
    spaceBefore=1,
    spaceAfter=2,
)


# ============================================================
# DATES
# ============================================================

date_style = ParagraphStyle(
    "Date",
    fontName=FONT_ITALIC,
    fontSize=10.2,
    leading=13,
    alignment=TA_RIGHT,
    spaceBefore=1,
    spaceAfter=0,
)


# ============================================================
# DEGREE
# ============================================================

italic_style = ParagraphStyle(
    "Italic",
    fontName=FONT_ITALIC,
    fontSize=10,
    leading=12.5,
    leftIndent=8,
    spaceBefore=1,
    spaceAfter=2,
)


# ============================================================
# TECH STACK
# ============================================================

tech_style = ParagraphStyle(
    "Tech",
    fontName=FONT,
    fontSize=10,
    leading=12.5,
    leftIndent=8,
    spaceBefore=1,
    spaceAfter=2,
)


# ============================================================
# PROJECT BULLETS
# ============================================================

bullet_style = ParagraphStyle(
    "Bullet",
    fontName=FONT,
    fontSize=9.8,
    leading=12.5,
    leftIndent=25,
    firstLineIndent=-9,
    spaceBefore=0.5,
    spaceAfter=1.5,
)


# ============================================================
# CODE / GITHUB
# ============================================================

code_style = ParagraphStyle(
    "Code",
    fontName=FONT,
    fontSize=9.8,
    leading=12,
    leftIndent=25,
    firstLineIndent=0,
    spaceBefore=2,
    spaceAfter=3,
)


# ============================================================
# TECHNICAL SKILLS
# ============================================================

technical_skill_style = ParagraphStyle(
    "TechnicalSkill",
    fontName=FONT,
    fontSize=10,
    leading=12.5,
    leftIndent=8,
    spaceBefore=0.5,
    spaceAfter=2,
)

# ============================================================
# LINK FUNCTION
# ============================================================

def styled_link(url, label):
    """
    Creates a blue underlined clickable link.
    """

    return (
        f'<link href="{url}">'
        f'<font color="{LINK_COLOR}">'
        f'<u>{label}</u>'
        f'</font>'
        f'</link>'
    )


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(story, title):
    """
    Creates:

    EDUCATION
    --------------------------------------------

    with the same alignment throughout the resume.
    """

    story.append(
        Paragraph(
            title.upper(),
            section_style
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.65,
            color=colors.black,
            spaceBefore=1,
            spaceAfter=4,
        )
    )


# ============================================================
# LEFT + RIGHT ROW
# ============================================================

def two_col_row(
    left_text,
    right_text,
    left_style=entry_title_style,
    right_style=date_style,
):
    """
    Creates a row like:

    Jadavpur University                         2024–2028
    Banking App                                      2026

    The date stays aligned to the same right edge.
    """

    # Small date column
    DATE_WIDTH = 1.05 * inch

    # Everything else belongs to the left
    LEFT_WIDTH = CONTENT_WIDTH - DATE_WIDTH

    table = Table(
        [
            [
                Paragraph(
                    left_text,
                    left_style
                ),

                Paragraph(
                    right_text,
                    right_style
                ),
            ]
        ],

        colWidths=[
            LEFT_WIDTH,
            DATE_WIDTH,
        ],

        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                # Vertical alignment
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),

                # No horizontal padding
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),

                # No vertical padding
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),
            ]
        )
    )

    return table


# ============================================================
# BULLET
# ============================================================

def add_bullet(story, text):

    story.append(
        Paragraph(
            f"•&nbsp;&nbsp;{text}",
            bullet_style
        )
    )


def bullet_list(story, bullets):

    for bullet in bullets:
        add_bullet(
            story,
            bullet
        )


# ============================================================
# BUILD RESUME PDF
# ============================================================

def build_resume_pdf(
    output_path,
    personal_info,
    education,
    experience,
    projects,
    skills,
    extracurricular,
):

    # ========================================================
    # DOCUMENT
    # ========================================================

    doc = SimpleDocTemplate(
        output_path,

        pagesize=A4,

        # Top and bottom
        topMargin=0.38 * inch,
        bottomMargin=0.38 * inch,

        # Left and right
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,

        title="Resume",

        author=personal_info.get(
            "name",
            ""
        ),
    )


    story = []


    # ========================================================
    # HEADER
    # ========================================================

    name = personal_info.get(
        "name",
        ""
    )

    if name:

        story.append(
            Paragraph(
                name.upper(),
                name_style
            )
        )


    # ========================================================
    # CONTACT INFORMATION
    # ========================================================

    contact_parts = []


    location = personal_info.get(
        "location",
        ""
    )

    phone = personal_info.get(
        "phone",
        ""
    )

    email = personal_info.get(
        "email",
        ""
    )


    # Location
    if location:

        contact_parts.append(
            location
        )


    # Phone
    if phone:

        contact_parts.append(
            phone
        )


    # Email
    if email:

        contact_parts.append(
            styled_link(
                f"mailto:{email}",
                email
            )
        )


    # GitHub / LinkedIn / LeetCode etc.
    for link in personal_info.get(
        "links",
        []
    ):

        url = link.get(
            "url",
            ""
        )

        label = link.get(
            "label",
            ""
        )

        if url:

            contact_parts.append(
                styled_link(
                    url,
                    label or url
                )
            )


    # Render contact line
    if contact_parts:

        story.append(
            Paragraph(
                " &nbsp;|&nbsp; ".join(
                    contact_parts
                ),

                contact_style
            )
        )


    # ========================================================
    # EDUCATION
    # ========================================================

    if education:

        section_header(
            story,
            "Education"
        )


        for item in education:

            # ------------------------------------------------
            # UNIVERSITY + DATE
            # ------------------------------------------------

            story.append(
                two_col_row(
                    item.get(
                        "institution",
                        ""
                    ),

                    item.get(
                        "dates",
                        ""
                    )
                )
            )


            # ------------------------------------------------
            # DEGREE + CGPA
            #
            # Example:
            #
            # B.E. Printing Engineering    8.1 CGPA
            # ------------------------------------------------

            degree = item.get(
                "degree",
                ""
            )

            detail = item.get(
                "detail",
                ""
            )


            if detail:

                degree += (
                    f" &nbsp;&nbsp; "
                    f"{detail} CGPA"
                )


            story.append(
                Paragraph(
                    degree,
                    italic_style
                )
            )


            # Small spacing after education
            story.append(
                Spacer(
                    1,
                    5
                )
            )


    # ========================================================
    # PROJECTS
    # ========================================================

    if projects:

        section_header(
            story,
            "Projects"
        )


        for project in projects:

            project_elements = []


            # ------------------------------------------------
            # PROJECT NAME + DATE
            # ------------------------------------------------

            project_elements.append(
                two_col_row(
                    project.get(
                        "name",
                        ""
                    ),

                    project.get(
                        "date",
                        ""
                    )
                )
            )


            # ------------------------------------------------
            # TECH STACK
            # ------------------------------------------------

            tags = project.get(
                "tags",
                ""
            )


            if tags:

                project_elements.append(
                    Paragraph(
                        f"<b>Tech Stack:</b> "
                        f"<i>{tags}</i>",

                        tech_style
                    )
                )


            # ------------------------------------------------
            # BULLETS
            # ------------------------------------------------

            for bullet in project.get(
                "bullets",
                []
            ):

                project_elements.append(
                    Paragraph(
                        f"•&nbsp;&nbsp;{bullet}",

                        bullet_style
                    )
                )


            # ------------------------------------------------
            # CODE
            # ------------------------------------------------

            live_url = project.get(
                "live_url",
                ""
            )


            if live_url:

                display_url = (
                    live_url
                    .replace(
                        "https://",
                        ""
                    )
                    .replace(
                        "http://",
                        ""
                    )
                )


                project_elements.append(
                    Paragraph(
                        f"<b>Code:</b>&nbsp;"
                        f"{styled_link(
                            live_url,
                            display_url
                        )}",

                        code_style
                    )
                )


            # ------------------------------------------------
            # KEEP PROJECT CONTENT TOGETHER
            # ------------------------------------------------

            story.append(
                KeepTogether(
                    project_elements
                )
            )


            # ------------------------------------------------
            # SPACE BETWEEN PROJECTS
            # ------------------------------------------------

            story.append(
                Spacer(
                    1,
                    8
                )
            )


    # ========================================================
    # EXPERIENCE
    # ========================================================

    if experience:

        section_header(
            story,
            "Experience"
        )


        for item in experience:

            role = item.get(
                "role",
                ""
            )

            company = item.get(
                "company",
                ""
            )


            title = role


            if company:

                title += (
                    f" — {company}"
                )


            # Role + date
            story.append(
                two_col_row(
                    title,

                    item.get(
                        "dates",
                        ""
                    )
                )
            )


            # Experience bullets
            bullet_list(
                story,

                item.get(
                    "bullets",
                    []
                )
            )


            story.append(
                Spacer(
                    1,
                    5
                )
            )


    # ========================================================
    # TECHNICAL SKILLS
    # ========================================================

    if skills:

        section_header(
            story,
            "Technical Skills"
        )


        for group in skills:

            category = group.get(
                "category",
                ""
            )

            items = group.get(
                "items",
                []
            )


            story.append(
                Paragraph(
                    f"<b>{category}:</b> "
                    f"{', '.join(items)}",

                    technical_skill_style
                )
            )


        story.append(
            Spacer(
                1,
                2
            )
        )


    # ========================================================
    # EXTRACURRICULAR
    # ========================================================

    if extracurricular:

        section_header(
            story,
            "Extracurricular"
        )


        bullet_list(
            story,

            extracurricular
        )


    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(
        story
    )