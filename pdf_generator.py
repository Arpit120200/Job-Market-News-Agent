from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from datetime import datetime
import os
import re


def clean_text(text):
    """
    Strips any remaining markdown symbols from text
    before inserting into PDF.
    """
    text = re.sub(r'\*\*?(.*?)\*\*?', r'\1', text)
    text = re.sub(r'#{1,6}\s?', '', text)
    text = re.sub(r'`', '', text)
    return text.strip()


def generate_pdf(report_text, output_folder="reports"):
    os.makedirs(output_folder, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"job_market_report_{date_str}.pdf"
    filepath = os.path.join(output_folder, filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Normal"],
        fontSize=22,
        textColor=colors.HexColor("#0f1117"),
        fontName="Helvetica-Bold",
        leading=28,
        spaceAfter=12
    )

    date_style = ParagraphStyle(
        "DateStyle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#6b7280"),
        fontName="Helvetica",
        spaceAfter=24
    )

    section_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Normal"],
        fontSize=12,
        textColor=colors.HexColor("#0f1117"),
        fontName="Helvetica-Bold",
        spaceBefore=16,
        spaceAfter=8,
        leftIndent=0
    )

    body_style = ParagraphStyle(
        "BodyText",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#374151"),
        fontName="Helvetica",
        leading=16,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        "BulletText",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#374151"),
        fontName="Helvetica",
        leading=16,
        leftIndent=16,
        spaceAfter=3
    )

    content = []

    # Header
    content.append(Paragraph("Job Market Daily Report", title_style))
    content.append(Paragraph(
        datetime.now().strftime("%A, %B %d, %Y"),
        date_style
    ))
    content.append(HRFlowable(
        width="100%",
        thickness=1,
        color=colors.HexColor("#e5e7eb"),
        spaceAfter=12
    ))

    # Process report text line by line
    lines = report_text.split("\n")

    for line in lines:
        line = clean_text(line)

        if not line:
            content.append(Spacer(1, 0.15*cm))
            continue

        # Detect numbered section headers like "1. MARKET OVERVIEW"
        if re.match(r'^\d+\.\s+[A-Z][A-Z\s]+$', line) or re.match(r'^[A-Z][A-Z\s]{3,}$', line):
            content.append(Paragraph(line, section_style))
            content.append(HRFlowable(
                width="100%",
                thickness=0.5,
                color=colors.HexColor("#e5e7eb"),
                spaceAfter=6
            ))

        # Detect ALL CAPS section headers without numbers
        elif line.isupper() and len(line) > 3:
            content.append(Paragraph(line, section_style))
            content.append(HRFlowable(
                width="100%",
                thickness=0.5,
                color=colors.HexColor("#e5e7eb"),
                spaceAfter=6
            ))

        # Bullet points
        elif line.startswith("-") or line.startswith("•"):
            bullet_text = "• " + line.lstrip("-•").strip()
            content.append(Paragraph(bullet_text, bullet_style))

        # Regular body text
        else:
            content.append(Paragraph(line, body_style))

    # Footer
    content.append(Spacer(1, 0.5*cm))
    content.append(HRFlowable(
        width="100%",
        thickness=0.5,
        color=colors.HexColor("#e5e7eb"),
        spaceAfter=8
    ))
    content.append(Paragraph(
        f"Generated automatically by AI Job Market Agent on {datetime.now().strftime('%B %d, %Y at %H:%M')}",
        ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#9ca3af"),
            fontName="Helvetica"
        )
    ))

    doc.build(content)
    print(f"PDF saved: {filepath}")
    return filepath