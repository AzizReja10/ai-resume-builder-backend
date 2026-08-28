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
# EXACT PAGE GEOMETRY
# ============================================================

PAGE_WIDTH, PAGE_HEIGHT = A4

# The screenshot has a relatively narrow left/right margin.
LEFT_MARGIN = 0.52 * inch
RIGHT_MARGIN = 0.52 * inch

CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN


# ============================================================
# STYLES
# ============================================================

# ---------------- HEADER ----------------

name_style = ParagraphStyle(
    "Name",
    fontName=FONT_BOLD,
    fontSize=16,
    leading=17,
    alignment=TA_CENTER,
    spaceAfter=2,
)


contact_style = ParagraphStyle(
    "Contact",
    fontName=FONT,
    fontSize=9.1,
    leading=10.5,
    alignment=TA_CENTER,
    spaceAfter=7,
)


# ---------------- SECTION ----------------

section_style = ParagraphStyle(
    "Section",
    fontName=FONT_BOLD,
    fontSize=10.2,
    leading=11,
    spaceBefore=3,
    spaceAfter=1,
)


# ---------------- TITLES ----------------

entry_title_style = ParagraphStyle(
    "EntryTitle",
    fontName=FONT_BOLD,
    fontSize=9.8,
    leading=11.5,
    spaceBefore=0,
    spaceAfter=0,
)


# ---------------- DATES ----------------

date_style = ParagraphStyle(
    "Date",
    fontName=FONT_ITALIC,
    fontSize=9.4,
    leading=11.5,
    alignment=TA_RIGHT,
    spaceBefore=0,
    spaceAfter=0,
)


# ---------------- DEGREE / TECH STACK ----------------

italic_style = ParagraphStyle(
    "Italic",
    fontName=FONT_ITALIC,
    fontSize=9.2,
    leading=11,
    leftIndent=8,          # slightly right
    spaceBefore=0,
    spaceAfter=1,
)


tech_style = ParagraphStyle(
    "Tech",
    fontName=FONT,
    fontSize=9.2,
    leading=11.2,
    leftIndent=8,          # slightly right
    spaceBefore=0,
    spaceAfter=1,
)


# ---------------- BULLETS ----------------

bullet_style = ParagraphStyle(
    "Bullet",
    fontName=FONT,
    fontSize=9.15,
    leading=11.5,

    # Move entire bullet content slightly right
    leftIndent=25,

    # Keep bullet itself slightly to the left of text
    firstLineIndent=-9,

    spaceBefore=0,
    spaceAfter=0.5,
)


# ---------------- CODE ----------------

code_style = ParagraphStyle(
    "Code",
    fontName=FONT,
    fontSize=9.15,
    leading=11,

    # Align Code with the project description
    leftIndent=25,

    firstLineIndent=0,
    spaceBefore=0,
    spaceAfter=2,
)


# ============================================================
# LINK
# ============================================================

def styled_link(url, label):

    return (
        f'<link href="{url}">'
        f'<font color="{LINK_COLOR}"><u>{label}</u></font>'
        f'</link>'
    )


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(story, title):

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
# LEFT + RIGHT ALIGNMENT
# ============================================================

def two_col_row(
    left_text,
    right_text,
    left_style=entry_title_style,
    right_style=date_style,
):

    # IMPORTANT:
    #
    # The left column occupies almost all the width.
    # The right column is only used for the date.
    #
    # This makes the date stay on one fixed right edge,
    # exactly like the screenshot.

    DATE_WIDTH = 1.05 * inch

    LEFT_WIDTH = CONTENT_WIDTH - DATE_WIDTH

    table = Table(
        [
            [
                Paragraph(left_text, left_style),
                Paragraph(right_text, right_style),
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
                ("VALIGN", (0, 0), (-1, -1), "TOP"),

                # ZERO horizontal padding
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),

                # ZERO vertical padding
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
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
        add_bullet(story, bullet)


# ============================================================
# BUILD PDF
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

        # EXACT BODY MARGINS
        topMargin=0.38 * inch,
        bottomMargin=0.38 * inch,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,

        title="Resume",
        author=personal_info.get("name", ""),
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
    # CONTACT LINE
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


    if location:
        contact_parts.append(location)

    if phone:
        contact_parts.append(phone)

    if email:

        contact_parts.append(
            styled_link(
                f"mailto:{email}",
                email
            )
        )


    # Social links
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


    if contact_parts:

        story.append(
            Paragraph(
                " &nbsp;|&nbsp; ".join(contact_parts),
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

            # University ---------------- Date
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


            # Degree --------------------
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
        f"CGPA: {detail}"
    )


            story.append(
                Paragraph(
                    degree,
                    italic_style
                )
            )


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
                        f"{styled_link(live_url, display_url)}",
                        code_style
                    )
                )


            # ------------------------------------------------
            # KEEP PROJECT TOGETHER
            # ------------------------------------------------

            story.append(
                KeepTogether(
                    project_elements
                )
            )


            # Small gap before next project
            story.append(
                Spacer(
                    1,
                    4
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


            story.append(
                two_col_row(
                    title,
                    item.get(
                        "dates",
                        ""
                    )
                )
            )


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
                    3
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
                    tech_style
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
    # BUILD
    # ========================================================

    doc.build(story)